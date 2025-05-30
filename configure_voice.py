#!/usr/bin/env python3
"""
Voice Configuration Tool for Totoro Assistant
Test and select the most natural voice for your assistant
"""

import logging
from src.voice import TextToSpeech, VoiceRecognizer

logging.basicConfig(level=logging.INFO)

def test_voice(voice_name, voice_id):
    """Test a specific voice"""
    print(f"\n🎭 Testing: {voice_name}")
    try:
        tts = TextToSpeech()
        tts.set_voice(voice_id)
        tts.speak(f"Hello! This is {voice_name}. I am your Totoro assistant with natural speech.")
        return True
    except Exception as e:
        print(f"❌ Error testing {voice_name}: {e}")
        return False

def test_microphone():
    """Test microphone setup"""
    print("\n🎤 MICROPHONE TEST")
    print("=" * 50)
    
    try:
        vr = VoiceRecognizer()
        print("\n📋 Available microphones:")
        vr.list_microphones()
        
        print("\n🎙️ Testing microphone input...")
        print("Say something within 5 seconds...")
        
        command = vr.listen_for_command(timeout=5)
        if command:
            print(f"✅ Successfully heard: '{command}'")
            return True
        else:
            print("⚠️ No speech detected")
            return False
            
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def main():
    print("🎭 TOTORO VOICE CONFIGURATION TOOL")
    print("=" * 60)
    
    # Test microphone first
    print("\n🔧 Step 1: Testing Microphone Setup")
    mic_working = test_microphone()
    
    if not mic_working:
        print("\n⚠️ Microphone Issues Detected")
        print("Troubleshooting tips:")
        print("- Check System Preferences > Security & Privacy > Microphone")
        print("- Ensure Terminal/Python has microphone access")
        print("- Try unplugging and reconnecting external microphones")
        print("- Use 'Logitech BRIO' for best quality if available")
    
    # Test natural voices
    print("\n🎭 Step 2: Testing Natural Voices")
    
    # Best natural voices to test
    voices_to_test = [
        ("Samantha (US) - Most Natural", "com.apple.voice.compact.en-US.Samantha"),
        ("Moira (Irish) - Sophisticated", "com.apple.voice.compact.en-IE.Moira"),
        ("Karen (Australian) - Clear", "com.apple.voice.compact.en-AU.Karen"),
        ("Tessa (South African) - Professional", "com.apple.voice.compact.en-ZA.Tessa"),
    ]
    
    working_voices = []
    for voice_name, voice_id in voices_to_test:
        if test_voice(voice_name, voice_id):
            working_voices.append((voice_name, voice_id))
    
    print(f"\n✅ Found {len(working_voices)} working natural voices")
    
    # Recommendations
    print("\n🌟 RECOMMENDATIONS")
    print("=" * 50)
    
    if working_voices:
        print("🏆 Best voices for natural speech:")
        for i, (name, _) in enumerate(working_voices[:3], 1):
            print(f"  {i}. {name}")
    
    print("\n🔧 To use the most natural voice:")
    print("export VOICE_PREFERENCE=natural")
    print("python main.py")
    
    print("\n🎤 For voice input:")
    if mic_working:
        print("✅ Microphone working! Use: python main.py (voice mode)")
    else:
        print("⚠️ Use text mode: python main.py --test")
    
    print("\n🎯 Test your setup:")
    print("python main.py --command 'what time is it'")

if __name__ == "__main__":
    main() 