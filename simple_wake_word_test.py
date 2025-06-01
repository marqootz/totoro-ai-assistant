#!/usr/bin/env python3
"""
Simplified wake word test to isolate Google API issues
"""

import speech_recognition as sr
import time

def simple_test():
    """Very simple test"""
    print("🔍 SIMPLE WAKE WORD TEST")
    print("=" * 30)
    
    r = sr.Recognizer()
    
    # Use very low threshold
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False  # Disable auto-adjustment
    
    print(f"🔊 Energy threshold fixed at: {r.energy_threshold}")
    
    # Use default microphone
    mic = sr.Microphone()
    
    print("👂 Listening for 10 seconds...")
    print("🗣️ Say 'HELLO' very clearly and loudly...")
    
    try:
        with mic as source:
            # Very short ambient noise adjustment
            r.adjust_for_ambient_noise(source, duration=0.1)
            print(f"🔊 After adjustment: {r.energy_threshold}")
            
            # Force threshold back down if it increased
            r.energy_threshold = 50
            print(f"🔊 Reset to: {r.energy_threshold}")
            
            # Listen
            audio = r.listen(source, timeout=10, phrase_time_limit=3)
            print("✅ Audio captured")
        
        # Try recognition
        print("🌐 Trying Google Speech Recognition...")
        
        try:
            text = r.recognize_google(audio, language='en-US')
            print(f"🎉 SUCCESS! Google heard: '{text}'")
            
            if 'hello' in text.lower():
                print("✅ Basic speech recognition working!")
                
                # Now try totoro
                print("\n🎯 Now say 'TOTORO'...")
                with mic as source:
                    audio2 = r.listen(source, timeout=5, phrase_time_limit=2)
                
                text2 = r.recognize_google(audio2, language='en-US')
                print(f"👂 Heard: '{text2}'")
                
                if 'totoro' in text2.lower() or 'toto' in text2.lower():
                    print("🎉 TOTORO WAKE WORD WORKING!")
                    return True
                    
            return False
            
        except sr.UnknownValueError:
            print("❓ Google could not understand the audio")
            return False
        except sr.RequestError as e:
            print(f"❌ Google API request failed: {e}")
            print("🔧 This suggests an internet/API connectivity issue")
            return False
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected - try speaking louder")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 SIMPLIFIED TOTORO TEST")
    print("=" * 40)
    
    success = simple_test()
    
    if success:
        print("\n🎉 WAKE WORD DETECTION IS WORKING!")
        print("✅ The frontend voice controls should work")
    else:
        print("\n❌ STILL NOT WORKING")
        print("🔧 Possible issues:")
        print("   1. Internet connection problems")
        print("   2. Google Speech API rate limiting")
        print("   3. Microphone audio quality")
        print("   4. Need to speak much louder/clearer")
        print("\n💡 Alternative: Try using a headset microphone") 