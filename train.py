import os
from functools import partial
from dataclasses import dataclass
from typing import Any, Dict, List, Union
from collections import defaultdict

import torch
from datasets import load_dataset, Audio
from transformers import (
    SpeechT5Processor,
    SpeechT5ForTextToSpeech,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)
from peft import LoraConfig, get_peft_model
from speechbrain.pretrained import EncoderClassifier

# ---------------------------------------------------------------------------
# 1. Hardware & Environment Setup
# ---------------------------------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
checkpoint = "microsoft/speecht5_tts"

processor = SpeechT5Processor.from_pretrained(checkpoint)
tokenizer = processor.tokenizer

# ---------------------------------------------------------------------------
# 2. Dataset Loading & Audio Hygiene
# ---------------------------------------------------------------------------
dataset = load_dataset("qmeeus/voxpopuli", "nl", split="train")
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

# ---------------------------------------------------------------------------
# 3. Text Preprocessing & Tokenizer Alignment
# ---------------------------------------------------------------------------
replacements = [
    ("à", "a"),
    ("ç", "c"),
    ("è", "e"),
    ("ë", "e"),
    ("í", "i"),
    ("ï", "i"),
    ("ö", "o"),
    ("ü", "u"),
]

def cleanup_text(inputs):
    for src, dst in replacements:
        inputs["text"] = inputs["text"].replace(src, dst)
    return inputs

dataset = dataset.map(cleanup_text)

# ---------------------------------------------------------------------------
# 4. Speaker Distribution Balancing
# ---------------------------------------------------------------------------
speaker_counts = defaultdict(int)
for speaker_id in dataset["speaker_id"]:
    speaker_counts[speaker_id] += 1

def select_speaker(speaker_id):
    return 100 <= speaker_counts[speaker_id] <= 400

dataset = dataset.filter(select_speaker, input_columns=["speaker_id"])

# ---------------------------------------------------------------------------
# 5. Speaker Embedding Extraction (SpeechBrain X-vectors)
# ---------------------------------------------------------------------------
spk_model_name = "speechbrain/spkrec-xvect-voxceleb"
speaker_model = EncoderClassifier.from_hparams(
    source=spk_model_name,
    run_opts={"device": device},
    savedir=os.path.join("./checkpoints", "speechbrain_xvect"),
)

def create_speaker_embedding(waveform):
    with torch.no_grad():
        speaker_embeddings = speaker_model.encode_batch(torch.tensor(waveform))
        speaker_embeddings = torch.nn.functional.normalize(speaker_embeddings, dim=2)
        speaker_embeddings = speaker_embeddings.squeeze().cpu().numpy()
    return speaker_embeddings 

def prepare_dataset(example):
    audio = example["audio"]
    processed = processor(
        text=example["text"],
        audio_target=audio["array"],
        sampling_rate=audio["sampling_rate"],
        return_attention_mask=False,
    )
    processed["labels"] = processed["labels"][0]
    processed["speaker_embeddings"] = create_speaker_embedding(audio["array"])
    return processed

dataset = dataset.map(prepare_dataset, remove_columns=dataset.column_names)

def is_not_too_long(input_ids):
    return len(input_ids) < 200

dataset = dataset.filter(is_not_too_long, input_columns=["input_ids"])
dataset = dataset.train_test_split(test_size=0.1)

# ---------------------------------------------------------------------------
# 6. Model Initialization & LoRA Adaptation
# ---------------------------------------------------------------------------
model = SpeechT5ForTextToSpeech.from_pretrained(checkpoint)

model.config.reduction_factor = 1
model.config.use_cache = False
model.generate = partial(model.generate, use_cache=True)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "out_proj"],
    lora_dropout=0.05,
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ---------------------------------------------------------------------------
# 7. Custom Data Collator with Padding & Loss Masking
# ---------------------------------------------------------------------------
@dataclass
class TTSDataCollatorWithPadding:
    processor: Any
    reduction_factor: int = 1

    def __call__(
        self, features: List[Dict[str, Union[List[int], torch.Tensor]]]
    ) -> Dict[str, torch.Tensor]:
        input_ids = [{"input_ids": feature["input_ids"]} for feature in features]
        label_features = [{"input_values": feature["labels"]} for feature in features]
        speaker_features = [feature["speaker_embeddings"] for feature in features]

        batch = self.processor.pad(
            input_ids=input_ids,
            labels=label_features,
            return_tensors="pt",
        )

        batch["labels"] = batch["labels"].masked_fill(
            batch.decoder_attention_mask.unsqueeze(-1).ne(1), -100
        )
        del batch["decoder_attention_mask"]

        if self.reduction_factor > 1:
            target_lengths = torch.tensor([len(f["input_values"]) for f in label_features])
            target_lengths = target_lengths.new(
                [length - length % self.reduction_factor for length in target_lengths]
            )
            batch["labels"] = batch["labels"][:, :max(target_lengths)]

        batch["speaker_embeddings"] = torch.tensor(speaker_features)
        return batch

data_collator = TTSDataCollatorWithPadding(
    processor=processor,
    reduction_factor=model.config.reduction_factor,
)

# ---------------------------------------------------------------------------
# 8. Training Pipeline Configuration & Execution
# ---------------------------------------------------------------------------
training_args = Seq2SeqTrainingArguments(
    output_dir="./checkpoints/speecht5_lora",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,
    warmup_steps=300,
    max_steps=4000,
    gradient_checkpointing=True,
    fp16=torch.cuda.is_available(),
    eval_strategy="steps",
    per_device_eval_batch_size=2,
    save_steps=500,
    eval_steps=500,
    logging_steps=25,
    report_to=["tensorboard"],
    load_best_model_at_end=True,
    greater_is_better=False,
    label_names=["labels"],
    save_total_limit=2,
)

trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    data_collator=data_collator,
    tokenizer=processor,
)

if __name__ == "__main__":
    os.makedirs("./checkpoints", exist_ok=True)
    print("Starting fine-tuning...")
    trainer.train()

    trainer.save_model("./checkpoints/speecht5_lora_final")
    processor.save_pretrained("./checkpoints/speecht5_lora_final")
    print("Training finished. Checkpoints saved to ./checkpoints/speecht5_lora_final")