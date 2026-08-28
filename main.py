from vieneu import Vieneu
import os

# Initialize the TTS model.
# By default, it uses the fast int8 backbone on CPU (ONNX), or auto-detects GPU (PyTorch).
tts = Vieneu()
os.makedirs("outputs", exist_ok=True)

def test_preset_voice():
    print("🎙️ Testing preset voice (Trúc Ly)...")
    text = "Tại báo cáo trình cổ đông cuối tháng 6/2026, ông Nguyễn Thừa Nhật - Quyền chủ tịch Hội đồng quản trị Tập đoàn Bảo Việt (mã chứng khoán BVH) cho biết, Tập đoàn sẽ ưu tiên nguồn lực để tăng vốn cho các công ty thành viên, đáp ứng yêu cầu phát triển hoạt động kinh doanh cốt lõi."

    audio = tts.infer(text, voice="Trúc Ly")
    
    # Save to file
    out_path = "outputs/preset_voice.wav"
    tts.save(audio, out_path)
    print(f"✅ Saved preset voice to: {out_path}\n")

if __name__ == "__main__":
    test_preset_voice()