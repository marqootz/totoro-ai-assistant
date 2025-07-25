#!/usr/bin/env python3
"""
Debug audio capture and format issues
"""

import speech_recognition as sr
import wave
import time
import os

def debug_audio_capture():
    """Capture audio and save to file for inspection"""
    print("🔍 AUDIO DEBUG TEST")
    print("=" * 30)
    
    r = sr.Recognizer()
    r.energy_threshold = 300  # Low threshold
    
    # Use iPhone microphone (index 0)
    mic = sr.Microphone(device_index=0)
    
    print("🎤 Using iPhone microphone...")
    
    # Adjust for ambient noise
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print(f"🔊 Energy threshold: {r.energy_threshold}")
    
    print("👂 Recording 3 seconds - speak CLEARLY:")
    print("🗣️ Say 'HELLO TOTORO' loudly and clearly...")
    
    try:
        with mic as source:
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            print("✅ Audio captured")
        
        # Save audio to file for inspection
        audio_filename = "debug_audio.wav"
        with open(audio_filename, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"💾 Audio saved to: {audio_filename}")
        
        # Try multiple speech recognition engines
        print("\n🧪 Testing different speech engines:")
        
        # 1. Google (original)
        try:
            text = r.recognize_google(audio, language='en-US')
            print(f"🌐 Google: '{text}' ✅")
        except Exception as e:
            print(f"🌐 Google: Failed - {e}")
        
        # 2. Try with different language hints
        try:
            text = r.recognize_google(audio, language='en-US', show_all=False)
            print(f"🌐 Google (strict): '{text}' ✅")
        except Exception as e:
            print(f"🌐 Google (strict): Failed - {e}")
        
        # 3. Check audio properties
        print(f"\n📊 Audio Properties:")
        print(f"   Sample rate: {mic.SAMPLE_RATE}")
        print(f"   Sample width: {mic.SAMPLE_WIDTH}")
        print(f"   Chunk size: {mic.CHUNK}")
        print(f"   Audio data length: {len(audio.frame_data)} bytes")
        
        # 4. Try very simple phrases
        print(f"\n💡 Try saying just 'HELLO' very clearly...")
        
        return True
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_words():
    """Test with very simple, clear words"""
    print(f"\n🗣️ SIMPLE WORD TEST")
    print("=" * 25)
    
    r = sr.Recognizer()
    r.energy_threshold = 200  # Even lower
    
    mic = sr.Microphone(device_index=0)  # iPhone mic
    
    simple_tests = [
        "HELLO",
        "YES", 
        "ONE TWO THREE",
        "TOTORO"
    ]
    
    for word in simple_tests:
        print(f"\n🎯 Say '{word}' clearly:")
        try:
            with mic as source:
                audio = r.listen(source, timeout=4, phrase_time_limit=2)
            
            text = r.recognize_google(audio)
            print(f"✅ Heard: '{text}'")
            
            if word.lower() in text.lower():
                print(f"🎉 MATCH! Wake word detection should work")
                return True
                
        except Exception as e:
            print(f"❌ Failed: {e}")
            continue
    
    return False

if __name__ == "__main__":
    print("🔍 TOTORO AUDIO DEBUG")
    print("=" * 40)
    
    success1 = debug_audio_capture()
    success2 = test_simple_words()
    
    if success1 or success2:
        print(f"\n🎉 AUDIO WORKING!")
        print(f"💡 The issue might be with your specific pronunciation")
        print(f"🗣️ Try speaking more clearly and loudly")
    else:
        print(f"\n❌ AUDIO ISSUES PERSIST")
        print(f"🔧 Possible solutions:")
        print(f"   1. Check macOS microphone permissions")
        print(f"   2. Try using a headset/external microphone")
        print(f"   3. Test with other apps (Voice Memos, etc.)")
        print(f"   4. Check internet connection stability") 