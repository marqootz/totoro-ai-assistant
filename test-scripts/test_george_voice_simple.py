#!/usr/bin/env python3
"""
Simple test of George's voice cloning
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def test_george_voice():
    print("🎭 Testing George's Voice Cloning")
    print("=" * 40)
    
    # Check if source audio exists
    source_audio = "assets/george-source-voice.mp3"
    if not os.path.exists(source_audio):
        print(f"❌ Source audio not found: {source_audio}")
        return False
    
    print(f"✅ Found source audio: {source_audio}")
    
    # Initialize TTS
    print("🚀 Initializing Chatterbox TTS...")
    tts = TextToSpeech(voice_preference="chatterbox")
    
    if not tts.chatterbox_model:
        print("❌ Chatterbox TTS not available")
        return False
    
    print("✅ Chatterbox TTS ready!")
    
    # Test voice cloning
    test_text = "Hello! This is George speaking with my cloned voice. Pretty cool, right?"
    print(f"\n🗣️ Speaking: '{test_text}'")
    
    success = tts.speak(test_text, audio_prompt_path=source_audio)
    
    if success:
        print("✅ George's voice cloning successful!")
        return True
    else:
        print("❌ Voice cloning failed")
        return False

if __name__ == "__main__":
    test_george_voice() 