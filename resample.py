import librosa
import soundfile as sf
import noisereduce as nr

# Load audio and resample to 16 kHz
audio, sr = librosa.load("raw_audio.wav", sr=16000)

# Filter background noise
clean_audio = nr.reduce_noise(y=audio, sr=16000)

# Save the standardized file
sf.write("clean_audio.wav", clean_audio, 16000)