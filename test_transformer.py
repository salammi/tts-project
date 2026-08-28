import torch
import soundfile as sf
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset

device = "cuda" if torch.cuda.is_available() else "cpu"
printf("Executing baseline on device: {device}")

# Load SpeechT5 acoustic model and HiFi-GAN vocoder
checkpoint = "microsoft/speecht5_tts"
processor = SpeechT5Processor.from_pretrained(checkpoint)
model = SpeechT5ForTextToSpeech.from_pretrained(checkpoint).to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

# Load sample X-Vector speaker embedding
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0).to(device)

# Process test prompt
inputs = processor(text="Text to speech environment verification completed.", return_tensors="pt").to(device)

with torch.no_grad():
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

sf.write("outputs/test_speecht5.wav", speech.cpu().numpy(), samplerate=16000)
print("✅ Transformer pipeline operational -> outputs/test_speecht5.wav")