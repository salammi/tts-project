import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech
from peft import LoraConfig, get_peft_model

# 1. Load processor and base model
checkpoint = "microsoft/speecht5_tts"
processor = SpeechT5Processor.from_pretrained(checkpoint)
model = SpeechT5ForTextToSpeech.from_pretrained(checkpoint)

# Maximize output resolution by forcing the decoder to predict every acoustic frame[cite: 12]
model.config.reduction_factor = 1

# Disable KV cache during training to ensure gradient checkpointing compatibility[cite: 12]
model.config.use_cache = False

# 2. Configure LoRA parameters
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "out_proj"],
    lora_dropout=0.05,
    bias="none",
)

# 3. Wrap the base model with the LoRA adapter
model = get_peft_model(model, lora_config)

# Verify the ratio of frozen base weights to trainable adapter parameters
model.print_trainable_parameters()