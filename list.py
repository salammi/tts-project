from vieneu import Vieneu

# Initialize the model (it will load the config instantly)
tts = Vieneu()

# Fetch and print the available voices
voices = tts.list_preset_voices()

print(f"\n🎙️ {len(voices)} built-in voices available:")
for description, voice_name in voices:
    print(f" - {description} (Name to use: '{voice_name}')")