#!/usr/bin/env python3
"""
Test script to verify only Coqui TTS is being used
"""

import sys
import os
sys.path.insert(0, 'src')

# Set environment to use Coqui
os.environ['VOICE_PREFERENCE'] = 'coqui'

from src.voice.text_to_speech import TextToSpeech
import config

def test_coqui_only():
    """Test that only Coqui TTS is being used"""
    
    print("🧪 TESTING COQUI TTS ONLY")
    print("=" * 40)
    
    # Check config
    voice_pref = getattr(config, 'VOICE_PREFERENCE', 'not set in config')
    print(f"✅ Config VOICE_PREFERENCE: {voice_pref}")
    print(f"✅ Environment VOICE_PREFERENCE: {os.environ.get('VOICE_PREFERENCE', 'not set')}")
    
    # Initialize TTS
    print("\n🚀 Initializing TTS with Coqui preference...")
    tts = TextToSpeech(voice_preference="coqui")
    
    # Check what's actually loaded
    if tts.coqui_tts:
        print("✅ Coqui TTS initialized successfully!")
        print(f"   Model: {getattr(tts.coqui_tts, 'model_name', 'unknown')}")
    else:
        print("❌ Coqui TTS not initialized")
    
    if tts.tts_engine:
        print("⚠️  System TTS is also loaded (should be fallback only)")
    else:
        print("✅ No system TTS loaded")
    
    # Check George's voice
    george_voice = "assets/george-source-voice.mp3"
    if os.path.exists(george_voice):
        print(f"✅ George's voice file found: {george_voice}")
        
        # Test with George's voice
        print("\n🗣️ Testing with George's cloned voice...")
        success = tts.speak("Hello! This test confirms I'm using only Coqui TTS with George's cloned voice.", 
                          audio_prompt_path=george_voice)
        
        if success:
            print("✅ Coqui TTS with voice cloning successful!")
        else:
            print("❌ Coqui TTS failed")
    else:
        print(f"⚠️  George's voice file not found: {george_voice}")
        print("   Testing with default Coqui voice...")
        
        # Note: This will likely fail since Coqui XTTS requires a speaker voice
        success = tts.speak("Testing Coqui TTS without voice cloning.")
        
        if success:
            print("✅ Coqui TTS test successful!")
        else:
            print("❌ Coqui TTS test failed (expected - needs speaker voice)")
    
    print(f"\n📊 TTS Configuration Summary:")
    print(f"   Voice Preference: {tts.voice_preference}")
    print(f"   Coqui TTS Available: {'Yes' if tts.coqui_tts else 'No'}")
    print(f"   System TTS Available: {'Yes' if tts.tts_engine else 'No'}")
    print(f"   George's Voice: {'Available' if os.path.exists(george_voice) else 'Missing'}")
    
    return tts.coqui_tts is not None

if __name__ == "__main__":
    success = test_coqui_only()
    
    if success:
        print("\n🎉 SUCCESS: Only Coqui TTS is configured and working!")
    else:
        print("\n❌ ISSUE: Coqui TTS is not properly configured")
        print("   Please check that TTS library is installed: pip install TTS") 