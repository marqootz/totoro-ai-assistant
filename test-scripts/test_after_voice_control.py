#!/usr/bin/env python3
"""
Test speech recognition after enabling Voice Control
"""

import speech_recognition as sr
import time

def test_post_voice_control():
    """Test after Voice Control is enabled"""
    print("🎯 POST-VOICE CONTROL TEST")
    print("=" * 35)
    print("⚠️  Make sure you've enabled:")
    print("   1. System Preferences → Accessibility → Voice Control")
    print("   2. System Preferences → Security & Privacy → Microphone permissions")
    print()
    
    r = sr.Recognizer()
    r.energy_threshold = 100  # Conservative threshold
    
    # Use default microphone
    mic = sr.Microphone()
    
    print("🎤 Testing with Voice Control enabled...")
    print("👂 Say 'HELLO TOTORO' clearly:")
    
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print(f"🔊 Energy threshold: {r.energy_threshold}")
            
            # Listen for speech
            audio = r.listen(source, timeout=8, phrase_time_limit=4)
            print("✅ Audio captured")
        
        # Try Google Speech Recognition
        print("🌐 Processing with Google Speech API...")
        text = r.recognize_google(audio, language='en-US')
        print(f"🎉 SUCCESS! Heard: '{text}'")
        
        # Check for wake words
        text_lower = text.lower()
        if any(word in text_lower for word in ['totoro', 'toto', 'hello']):
            print("🎯 WAKE WORD DETECTION WORKING!")
            return True
        else:
            print("✅ Speech recognition working, but try saying 'totoro' more clearly")
            return True
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected - try speaking louder")
        return False
    except sr.UnknownValueError:
        print("❓ Could not understand - Voice Control might still need setup")
        return False
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 VOICE CONTROL VERIFICATION TEST")
    print("=" * 50)
    
    input("Press Enter AFTER you've enabled Voice Control...")
    
    success = test_post_voice_control()
    
    if success:
        print("\n🎉 SPEECH RECOGNITION WORKING!")
        print("✅ Wake word detection should now work in the frontend")
        print("🌐 Visit: http://localhost:5002")
    else:
        print("\n❌ Still having issues")
        print("🔧 Additional steps:")
        print("   1. Restart Terminal after enabling Voice Control")
        print("   2. Test with Voice Memos app first")
        print("   3. Try 'Hey Siri' to test system speech recognition") 