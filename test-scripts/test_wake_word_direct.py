#!/usr/bin/env python3
"""
Direct test of wake word detection with improved settings
"""

from src.voice.speech_recognition import VoiceRecognizer
import time

def test_wake_word():
    """Test wake word detection directly"""
    print("🎯 DIRECT WAKE WORD TEST")
    print("=" * 30)
    
    # Create voice recognizer with improved settings
    recognizer = VoiceRecognizer(wake_word="totoro")
    
    print(f"🎤 Microphone initialized: {recognizer.microphone is not None}")
    print(f"🔊 Energy threshold: {recognizer.recognizer.energy_threshold}")
    
    # Test wake word detection
    print(f"\n👂 Listening for wake word 'totoro' for 15 seconds...")
    print(f"🗣️ Say 'TOTORO' clearly and loudly!")
    
    start_time = time.time()
    success = recognizer.listen_for_wake_word(timeout=15)
    end_time = time.time()
    
    if success:
        print(f"🎉 SUCCESS! Wake word detected in {end_time - start_time:.1f} seconds")
        return True
    else:
        print(f"❌ Wake word not detected in {end_time - start_time:.1f} seconds")
        return False

if __name__ == "__main__":
    print("🧪 TOTORO WAKE WORD DIRECT TEST")
    print("=" * 50)
    
    try:
        success = test_wake_word()
        
        if success:
            print(f"\n✅ WAKE WORD DETECTION WORKING!")
            print(f"🎯 You can now use the frontend voice controls")
        else:
            print(f"\n❌ WAKE WORD DETECTION STILL HAS ISSUES")
            print(f"🔧 Troubleshooting:")
            print(f"   1. Speak louder and more clearly")
            print(f"   2. Get closer to the microphone")
            print(f"   3. Ensure stable internet connection")
            print(f"   4. Try pronunciation: 'TOH-TOH-ROH'")
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}") 