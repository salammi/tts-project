# Vietnamese Text-to-Speech (TTS) & Fine-Tuning Lab

A comprehensive sandbox and development pipeline for Vietnamese speech synthesis and voice adaptation. This repository supports preset voice synthesis, zero-shot voice cloning, real-time chunked streaming via **VieNeu-TTS**, and Transformer fine-tuning pipelines using **Hugging Face SpeechT5**[cite: 1, 2].

---

## 📌 Features

- **Preset Voice Synthesis:** Generate natural Vietnamese speech using built-in high-quality presets (e.g., `Trúc Ly`, `Minh Đức`, `Phạm Tuyên`).
- **Zero-Shot Voice Cloning:** Clone target voices using short 3–5 second reference audio clips (`.wav`) via neural codecs and speaker embeddings.
- **Real-Time Audio Streaming:** Low-latency chunked synthesis via ONNX Runtime and PyAudio streaming.
- **Transformer Fine-Tuning Pipeline:** Architecture for sequence-to-sequence fine-tuning with SpeechT5, X-vectors (SpeechBrain), and HiFi-GAN vocoders[cite: 2, 5].
- **Automated Environment Verification:** Built-in auditing script to test CUDA acceleration, audio libraries, and package versions.

---

## 📋 Prerequisites & System Requirements

- **OS:** Windows 10/11, Ubuntu 20.04+, or WSL2
- **Python:** **Python 3.10, 3.11, or 3.12** *(Python 3.9 or older is not supported)*
- **PyTorch:** **PyTorch >= 2.6.0** (required for secure weight loading)
- **C/C++ & Audio Tools:** FFmpeg and PortAudio

### Virtual Environment Setup:
- **PyTorch:**
  ```bash
    pip install torch torchvision torchaudio

- **Hugging Face core and distributed training toolkits:**
  ```bash
    pip install transformers datasets accelerate huggingface_hub

- **Audio processing & Speaker Embedding libraries:**
  ```bash
    pip install soundfile librosa speechbrain scipy

- **Parameter-Efficient Fine-Tuning & Quantization:**
  ```bash
    pip install peft onnxruntime optimum

- **VieNeu-TTS SDK and audio streaming utilities:**
  ```bash
    pip install vieneu pyaudio
