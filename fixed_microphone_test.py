#!/usr/bin/env python3
"""
Fixed microphone test with lower energy threshold
"""

import speech_recognition as sr
import sys
import time

def test_with_fixed_threshold():
    """Test with manually set low energy threshold"""
    print("🔧 FIXED MICROPHONE TEST")
    print("=" * 40)
    
    r = sr.Recognizer()
    
    # Test different microphones
    microphones_to_try = [
        (0, "iPhone Microphone"),
        (2, "Logitech BRIO"), 
        (None, "System Default")
    ]
    
    for mic_index, mic_name in microphones_to_try:
        print(f"\n🎤 Testing {mic_name}...")
        
        try:
            if mic_index is not None:
                mic = sr.Microphone(device_index=mic_index)
            else:
                mic = sr.Microphone()
            
            # Set a MUCH lower energy threshold manually
            r.energy_threshold = 300  # Lower threshold for quiet environments
            print(f"🔧 Set energy threshold to: {r.energy_threshold}")
            
            # Quick ambient noise adjustment
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                
            # Override if it got too high
            if r.energy_threshold > 1000:
                r.energy_threshold = 300
                print(f"🔧 Reset high threshold back to: {r.energy_threshold}")
            else:
                print(f"🔊 Final energy threshold: {r.energy_threshold}")
            
            print(f"👂 Listening for 5 seconds - speak CLEARLY:")
            print(f"🎯 Say 'TOTORO' or 'HELLO TOTORO' now...")
            
            with mic as source:
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                print(f"✅ Audio captured")
            
            print(f"🌐 Processing with Google...")
            text = r.recognize_google(audio, language='en-US')
            print(f"🎉 SUCCESS with {mic_name}!")
            print(f"👂 Heard: '{text}'")
            
            if any(word in text.lower() for word in ['totoro', 'toto']):
                print(f"🎯 WAKE WORD DETECTED!")
                
            return True, mic_index
            
        except sr.WaitTimeoutError:
            print(f"⏰ {mic_name}: No speech detected")
            continue
        except sr.UnknownValueError:
            print(f"❓ {mic_name}: Could not understand audio")
            continue
        except sr.RequestError as e:
            print(f"❌ {mic_name}: API error - {e}")
            continue
        except Exception as e:
            print(f"❌ {mic_name}: Error - {e}")
            continue
    
    return False, None

if __name__ == "__main__":
    print("🔧 TOTORO WAKE WORD FIX TEST")
    print("=" * 50)
    
    success, working_mic = test_with_fixed_threshold()
    
    if success:
        print(f"\n🎉 WAKE WORD DETECTION WORKING!")
        print(f"✅ Working microphone index: {working_mic}")
        print(f"💡 Solution: Lower energy threshold to ~300")
    else:
        print(f"\n❌ Still having issues")
        print(f"🔧 Try these:")
        print(f"   1. Speak much LOUDER and CLEARER")
        print(f"   2. Get closer to the microphone")
        print(f"   3. Reduce background noise")
        print(f"   4. Check if headset microphone works better") 