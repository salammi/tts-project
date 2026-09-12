from vieneu import Vieneu
import os

# Initialize the TTS model.
# By default, it uses the fast int8 backbone on CPU (ONNX), or auto-detects GPU (PyTorch).
tts = Vieneu()
os.makedirs("outputs", exist_ok=True)

def test_preset_voice():
    print("🎙️ Testing preset voice (Trúc Ly)...")
    text = "Xin chào, đây là một dự án thử nghiệm sử dụng VieNeu TTS."
    
    # Generate audio
    audio = tts.infer(text, voice="Trúc Ly")
    
    # Save to file
    out_path = "outputs/preset_voice.wav"
    tts.save(audio, out_path)
    print(f"✅ Saved preset voice to: {out_path}\n")

def test_voice_cloning():
    print("🧬 Testing instant voice cloning...")
    # Make sure you have a short 3-5 second audio clip named 'my_voice.wav' in the same folder.
    ref_audio_path = "my_voice.wav"
    
    if not os.path.exists(ref_audio_path):
        print(f"⚠️ Skipping voice cloning: Please add a '{ref_audio_path}' file to test this feature.\n")
        return

    text = "Chào bạn, hệ thống vừa sao chép thành công giọng nói của tôi từ một tệp âm thanh ngắn."
    
    # Clone and generate
    audio = tts.infer(text, ref_audio=ref_audio_path, denoise=True)
    
    out_path = "outputs/cloned_voice.wav"
    tts.save(audio, out_path)
    print(f"✅ Saved cloned voice to: {out_path}\n")

def test_streaming():
    print("🌊 Testing real-time streaming...")
    
    # Streaming requires pinning the backend to ONNX
    stream_tts = Vieneu(backend="onnx")
    
    text = "Xin chào các bạn! Đây là tính năng phát âm thanh theo thời gian thực."
    
    try:
        # Pyaudio is great for streaming playback (pip install pyaudio)
        import pyaudio
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=48000,
                        output=True)
        
        # Iterate over the generator to get audio chunks as they are synthesized
        for chunk in stream_tts.infer_stream(text, voice="Trúc Ly"):
            stream.write(chunk.tobytes())
            
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("✅ Streaming completed.\n")
        
    except ImportError:
        print("⚠️ To hear the real-time stream, install PyAudio: pip install pyaudio")

if __name__ == "__main__":
    test_preset_voice()
    test_voice_cloning()
    test_streaming()