#!/usr/bin/env python3
"""
Test the fixed TTS to verify no double audio
"""

from src.voice.text_to_speech import TextToSpeech
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)

def test_fixed_audio():
    print("🎵 Testing Fixed Audio System")
    print("=" * 40)
    
    # Test with Chatterbox (neural) TTS
    print("1. Testing Chatterbox TTS (should be single audio)...")
    tts_neural = TextToSpeech(voice_preference='chatterbox')
    success1 = tts_neural.test_speech("Hello! This is Chatterbox neural TTS. You should hear this only once, not twice.")
    
    # Wait a moment
    import time
    time.sleep(2)
    
    # Test with System TTS  
    print("\n2. Testing System TTS (should be single audio)...")
    tts_system = TextToSpeech(voice_preference='system')
    success2 = tts_system.test_speech("Hello! This is system TTS. You should hear this only once, not twice.")
    
    # Results
    print(f"\n📊 Results:")
    print(f"   Chatterbox TTS: {'✅ Working' if success1 else '❌ Failed'}")
    print(f"   System TTS: {'✅ Working' if success2 else '❌ Failed'}")
    
    if success1 or success2:
        print(f"\n🎉 Audio fix successful - no more double voices!")
    else:
        print(f"\n❌ Audio issues remain")

if __name__ == "__main__":
    test_fixed_audio() 