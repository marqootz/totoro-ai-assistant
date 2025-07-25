#!/usr/bin/env python3
"""
Debug microphone and speech recognition issues
"""

import speech_recognition as sr
import sys
import time

def simple_microphone_test():
    """Simple test with detailed debugging"""
    print("🔍 DEBUG: Simple Microphone Test")
    print("=" * 40)
    
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        print(f"✅ Speech recognizer initialized")
        
        # List microphones
        mics = sr.Microphone.list_microphone_names()
        print(f"📋 Found {len(mics)} microphones:")
        for i, name in enumerate(mics):
            print(f"  {i}: {name}")
        
        # Try default microphone first
        print(f"\n🎤 Testing DEFAULT microphone...")
        mic = sr.Microphone()
        
        print(f"🔧 Adjusting for ambient noise...")
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"🔊 Energy threshold set to: {r.energy_threshold}")
        
        print(f"👂 Listening for 3 seconds - please speak clearly:")
        print(f"🔴 Say 'totoro' or 'hello' now...")
        
        try:
            with mic as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                print(f"✅ Audio captured successfully")
                print(f"📏 Audio duration: ~{len(audio.frame_data) / 16000:.1f} seconds")
            
            print(f"🌐 Sending to Google Speech Recognition...")
            text = r.recognize_google(audio, language='en-US')
            print(f"🎉 SUCCESS! Heard: '{text}'")
            
            # Check for wake word
            if 'totoro' in text.lower():
                print(f"🎯 WAKE WORD DETECTED!")
            
            return True
            
        except sr.WaitTimeoutError:
            print(f"⏰ TIMEOUT: No speech detected in 3 seconds")
            print(f"💡 Possible issues:")
            print(f"   - Microphone permissions not granted")
            print(f"   - Speaking too quietly")
            print(f"   - Wrong microphone selected")
            return False
            
        except sr.UnknownValueError:
            print(f"❓ SPEECH NOT UNDERSTOOD")
            print(f"💡 Possible issues:")
            print(f"   - Audio quality too poor")
            print(f"   - Background noise too loud") 
            print(f"   - Speaking too fast/unclear")
            print(f"   - Energy threshold too high: {r.energy_threshold}")
            return False
            
        except sr.RequestError as e:
            print(f"❌ GOOGLE API ERROR: {e}")
            print(f"💡 Possible issues:")
            print(f"   - Internet connectivity")
            print(f"   - Google API rate limits")
            print(f"   - API key issues")
            return False
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return False

def test_microphone_permissions():
    """Test if microphone permissions are granted"""
    print(f"\n🔐 Testing microphone permissions...")
    
    try:
        import subprocess
        # Check macOS microphone permissions
        result = subprocess.run([
            'system_profiler', 'SPAudioDataType'
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print(f"✅ System audio info accessible")
        else:
            print(f"⚠️ Cannot access system audio info")
            
    except Exception as e:
        print(f"⚠️ Permission check failed: {e}")

if __name__ == "__main__":
    print("🧪 TOTORO MICROPHONE DEBUG")
    print("=" * 50)
    
    test_microphone_permissions()
    success = simple_microphone_test()
    
    if success:
        print(f"\n🎉 Microphone and speech recognition working!")
        print(f"✅ Wake word detection should work")
    else:
        print(f"\n❌ Issues found with microphone/speech recognition")
        print(f"🔧 Troubleshooting steps:")
        print(f"   1. Check System Preferences > Security & Privacy > Microphone")
        print(f"   2. Ensure Python/Terminal has microphone access")
        print(f"   3. Try speaking louder and clearer")
        print(f"   4. Check internet connection")
        print(f"   5. Try a different microphone") 