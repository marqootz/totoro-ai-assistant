#!/usr/bin/env python3
"""
Quick K2-SO Voice Test - Simple verification of voice cloning
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def test_k2so_voice():
    """Quick test of K2-SO voice cloning"""
    
    print("🤖 K2-SO VOICE TEST")
    print("=" * 30)
    
    # Check if source audio file exists
    source_audio = "assets/k2so-voice-samples.mp3"
    if not os.path.exists(source_audio):
        print(f"❌ Source audio file not found: {source_audio}")
        return False
    
    print(f"✅ Found source audio: {source_audio}")
    
    # Initialize TTS
    tts = TextToSpeech(voice_preference="coqui")
    
    if not tts.coqui_tts:
        print("❌ Coqui TTS not available.")
        return False
    
    print("✅ Coqui TTS ready!")
    
    # Short test phrases
    test_phrases = [
        "I am K2-SO.",
        "Congratulations, you are being rescued.",
        "I have a bad feeling about this."
    ]
    
    print(f"\n🎤 Testing K2-SO voice cloning:\n")
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"🤖 Test {i}: '{phrase}'")
        
        # Use voice cloning
        success = tts.speak(phrase, audio_prompt_path=source_audio)
        
        if success:
            print(f"✅ Test {i} completed!")
        else:
            print(f"❌ Test {i} failed!")
        
        print()
    
    print("🎉 K2-SO voice test complete!")
    return True

if __name__ == "__main__":
    test_k2so_voice() 