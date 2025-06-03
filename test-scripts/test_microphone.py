#!/usr/bin/env python3
"""
Simple microphone test for Totoro
"""

import speech_recognition as sr
import sys
import time

def test_microphone():
    """Test microphone access and speech recognition"""
    print("🎤 MICROPHONE TEST")
    print("=" * 30)
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # List available microphones
    print("\n📋 Available microphones:")
    mics = sr.Microphone.list_microphone_names()
    for i, name in enumerate(mics):
        print(f"  {i}: {name}")
    
    # Try different microphones
    microphones_to_try = [
        (2, "Logitech BRIO"),  # Usually best for speech
        (None, "Default"),      # System default
        (1, "Odyssey G95NC"),   # Another option
    ]
    
    for mic_index, mic_name in microphones_to_try:
        print(f"\n🔄 Trying {mic_name} microphone...")
        
        try:
            if mic_index is not None:
                mic = sr.Microphone(device_index=mic_index)
            else:
                mic = sr.Microphone()
            
            print(f"✅ Initialized {mic_name} microphone")
            
            # Adjust for ambient noise
            print("🔧 Adjusting for ambient noise... (1 second)")
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print(f"🔊 Energy threshold: {r.energy_threshold}")
            
            print("✅ Ambient noise adjustment complete")
            
            # Test basic speech recognition
            print("\n👂 Testing speech recognition...")
            print("📢 Please say something CLEARLY in the next 5 seconds:")
            
            try:
                with mic as source:
                    print("🔴 Listening...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=4)
                    print("🔄 Audio captured, processing...")
                
                print("🌐 Sending to Google Speech API...")
                text = r.recognize_google(audio)
                print(f"✅ SUCCESS with {mic_name}! I heard: '{text}'")
                return True, mic_index
                
            except sr.WaitTimeoutError:
                print(f"⏰ Timeout with {mic_name} - no speech detected")
                continue
            except sr.UnknownValueError:
                print(f"❓ {mic_name} could not understand audio")
                continue
            except sr.RequestError as e:
                print(f"❌ {mic_name} speech recognition service error: {e}")
                continue
                
        except Exception as e:
            print(f"❌ {mic_name} microphone error: {e}")
            continue
    
    print("❌ All microphones failed")
    return False, None

def test_wake_word_detection(mic_index=None):
    """Test wake word detection specifically"""
    print("\n\n🎯 WAKE WORD TEST")
    print("=" * 30)
    
    r = sr.Recognizer()
    if mic_index is not None:
        mic = sr.Microphone(device_index=mic_index)
        print(f"✅ Using working microphone (index {mic_index})")
    else:
        mic = sr.Microphone()
        print("✅ Using default microphone")
    
    wake_word = "totoro"
    
    # Adjust for ambient noise
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
    
    print(f"👂 Listening for wake word: '{wake_word}'")
    print("📢 Say 'totoro' clearly in the next 10 seconds:")
    
    try:
        with mic as source:
            print("🔴 Listening...")
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
        
        print("🔄 Processing audio...")
        text = r.recognize_google(audio).lower()
        print(f"👂 I heard: '{text}'")
        
        if wake_word in text:
            print(f"🎉 SUCCESS! Wake word '{wake_word}' detected!")
            return True
        else:
            print(f"❌ Wake word '{wake_word}' not found in: '{text}'")
            return False
            
    except sr.WaitTimeoutError:
        print("⏰ Timeout - no speech detected")
        return False
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return False
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TOTORO MICROPHONE & WAKE WORD TEST")
    print("=" * 50)
    
    # Test microphone
    mic_success, mic_index = test_microphone()
    
    if mic_success:
        # Test wake word detection with the working microphone
        wake_success = test_wake_word_detection(mic_index)
        
        if wake_success:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Microphone is working")
            print("✅ Speech recognition is working") 
            print("✅ Wake word detection is working")
        else:
            print("\n⚠️ PARTIAL SUCCESS")
            print("✅ Microphone is working")
            print("❌ Wake word detection needs attention")
    else:
        print("\n❌ TESTS FAILED")
        print("❌ Microphone issues detected")
    
    print("\n📝 If tests pass but frontend doesn't work, the issue is in the integration.") 