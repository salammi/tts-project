from vieneu import Vieneu
import os

# Initialize the TTS model.
# By default, it uses the fast int8 backbone on CPU (ONNX), or auto-detects GPU (PyTorch).
tts = Vieneu()
os.makedirs("outputs", exist_ok=True)

def test_preset_voice():
    print("🎙️ Testing preset voice (Trúc Ly)...")
    text = "áo Dân Trí đưa tin, Ngày 26/8, Công an phường Bà Rịa đang xác minh vụ việc bắt người trái pháp luật xảy ra ngày 19/8 trước số nhà 176 đường Cách Mạng Tháng Tám (phường Bà Rịa).Theo thông tin ban đầu, tối 19/8, sau trận thắng 2-0 của đội tuyển Việt Nam trước Malaysia trong bán kết lượt về ASEAN Cup 2026, nhiều người dân tại phường Bà Rịa đổ ra đường đi bão"

    audio = tts.infer(text, voice="Minh Triết")
    
    # Save to file
    out_path = "outputs/preset_voice.wav"
    tts.save(audio, out_path)
    print(f"✅ Saved preset voice to: {out_path}\n")

if __name__ == "__main__":
    test_preset_voice()