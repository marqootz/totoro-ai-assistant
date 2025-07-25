#!/usr/bin/env python3
"""
Test Woman's Voice Setup
Demonstrates how to use a woman's voice sample for WAV file creation
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def test_woman_voice_setup():
    """Test the woman's voice setup process"""
    
    print("🎤 Woman's Voice Setup Test")
    print("=" * 50)
    
    # Check for available voice samples
    voice_samples = [
        # ElevenLabs voices (new additions)
        "assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
        "assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3",
        # Custom voice samples
        "woman_voice_sample.mp3",
        "woman_voice_sample.wav", 
        "assets/woman_voice_sample.mp3",
        "assets/woman_voice_sample.wav",
        # Existing voices
        "assets/george-source-voice-clean.mp3",
        "assets/k2so-voice-samples.mp3"
    ]
    
    available_samples = []
    for sample in voice_samples:
        if os.path.exists(sample):
            available_samples.append(sample)
            print(f"✅ Found voice sample: {sample}")
    
    if not available_samples:
        print("❌ No voice samples found!")
        print("\n📝 To use a woman's voice, you need to:")
        print("1. Record a woman speaking clearly for 10-20 seconds")
        print("2. Save as MP3 or WAV file (e.g., 'woman_voice_sample.mp3')")
        print("3. Place the file in your project directory")
        print("4. Run this script again")
        return False
    
    # Initialize TTS
    print("\n🤖 Initializing TTS system...")
    tts = TextToSpeech(voice_preference="coqui")
    
    if not tts.coqui_tts:
        print("❌ Coqui TTS not available")
        return False
    
    print("✅ TTS system ready!")
    
    # Test with first available sample
    voice_sample = available_samples[0]
    test_text = "Hello! This is a test of the voice synthesis system."
    output_file = "voice_test.wav"
    
    print(f"\n🎵 Testing with voice sample: {voice_sample}")
    print(f"📝 Text: '{test_text}'")
    print(f"📁 Output: {output_file}")
    
    try:
        # Generate audio with voice cloning
        tts.coqui_tts.tts_to_file(
            text=test_text,
            speaker_wav=voice_sample,
            language="en",
            file_path=output_file,
            speed=1.0
        )
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ Successfully created: {output_file} ({file_size:,} bytes)")
            print(f"🎉 Voice test completed successfully!")
            return True
        else:
            print("❌ Failed to create output file")
            return False
            
    except Exception as e:
        print(f"❌ Error during voice synthesis: {e}")
        return False

def show_available_voices():
    """Show all available voice options"""
    
    print("\n" + "=" * 50)
    print("AVAILABLE VOICE OPTIONS")
    print("=" * 50)
    
    voice_options = {
        "Julia (ElevenLabs)": "assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
        "Sarah (ElevenLabs)": "assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3",
        "George (Human)": "assets/george-source-voice-clean.mp3",
        "K2-SO (Robot)": "assets/k2so-voice-samples.mp3"
    }
    
    available_voices = {}
    for name, path in voice_options.items():
        if os.path.exists(path):
            available_voices[name] = path
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (not found)")
    
    return available_voices

def show_usage_examples():
    """Show usage examples for woman's voice"""
    
    print("\n" + "=" * 50)
    print("USAGE EXAMPLES")
    print("=" * 50)
    
    print("\n1. Command Line Usage:")
    print("   # Using Julia voice")
    print("   python create_woman_voice.py \"Hello! This is a test.\" output.wav assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3")
    print("   # Using Sarah voice")
    print("   python create_woman_voice.py \"Hello! This is a test.\" output.wav assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3")
    
    print("\n2. Python Code:")
    print("""
from src.voice.text_to_speech import TextToSpeech

tts = TextToSpeech(voice_preference="coqui")

# Using Julia voice
tts.coqui_tts.tts_to_file(
    text="Hello! This is a test of the Julia voice.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
    language="en",
    file_path="julia_output.wav",
    speed=1.0
)

# Using Sarah voice
tts.coqui_tts.tts_to_file(
    text="Hello! This is a test of the Sarah voice.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3",
    language="en",
    file_path="sarah_output.wav",
    speed=1.0
)
""")
    
    print("\n3. Batch Processing with Different Voices:")
    print("""
phrases = [
    "Hello, welcome to our system!",
    "I'm here to help you with any questions.",
    "Thank you for using our service today."
]

voices = [
    "assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
    "assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3"
]

for i, phrase in enumerate(phrases):
    for j, voice in enumerate(voices):
        voice_name = "julia" if "Julia" in voice else "sarah"
        output_file = f"{voice_name}_phrase_{i+1}.wav"
        tts.coqui_tts.tts_to_file(
            text=phrase,
            speaker_wav=voice,
            language="en",
            file_path=output_file,
            speed=1.0
        )
""")

def main():
    """Main test function"""
    
    # Show available voices
    available_voices = show_available_voices()
    
    if not available_voices:
        print("\n⚠️  No voice samples found!")
        print("Please add voice samples to the assets directory.")
        return
    
    # Test voice synthesis
    success = test_woman_voice_setup()
    
    if success:
        print("\n🎉 Voice synthesis is working correctly!")
        print("You can now create WAV files using the available voice samples.")
    else:
        print("\n⚠️  Voice synthesis needs attention.")
        print("Please check the TTS system setup.")
    
    show_usage_examples()

if __name__ == "__main__":
    main() 