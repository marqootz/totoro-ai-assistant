#!/usr/bin/env python3
"""
Test script for Coqui TTS implementation
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, 'src')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_coqui_direct():
    """Test Coqui TTS directly"""
    
    print("🧪 TESTING COQUI TTS DIRECTLY")
    print("=" * 40)
    
    try:
        from voice.coqui_tts import CoquiTTS
        
        # Create Coqui TTS instance
        coqui = CoquiTTS()
        
        if coqui.tts:
            print("✅ Coqui TTS initialized successfully!")
            
            # Check for George's voice
            george_voice = "assets/george-source-voice.mp3"
            if os.path.exists(george_voice):
                coqui.set_george_voice(george_voice)
                
                # Test speech
                print("🗣️ Testing speech generation...")
                success = coqui.speak("Hello! This is a test of Coqui TTS with voice cloning.")
                
                if success:
                    print("🎉 Direct Coqui TTS test successful!")
                    return True
                else:
                    print("❌ Speech generation failed")
                    return False
            else:
                print(f"⚠️ George's voice file not found: {george_voice}")
                return False
        else:
            print("❌ Coqui TTS initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        return False

def test_integrated_tts():
    """Test integrated TTS system"""
    
    print("\n🧪 TESTING INTEGRATED TTS SYSTEM")
    print("=" * 40)
    
    try:
        from voice.text_to_speech import TextToSpeech
        
        # Create TTS instance with Coqui preference
        tts = TextToSpeech(voice_preference="coqui")
        
        if tts.coqui_tts:
            print("✅ Integrated Coqui TTS initialized!")
            
            # Test speech
            print("🗣️ Testing integrated speech...")
            success = tts.speak("Hello! This is a test of the integrated Coqui TTS system.")
            
            if success:
                print("🎉 Integrated TTS test successful!")
                return True
            else:
                print("❌ Integrated speech failed")
                return False
        else:
            print("⚠️ Coqui TTS not available, testing fallback...")
            
            # Test fallback to system TTS
            success = tts.speak("Testing system TTS fallback.")
            
            if success:
                print("✅ System TTS fallback working!")
                return True
            else:
                print("❌ All TTS methods failed")
                return False
                
    except Exception as e:
        print(f"❌ Integrated test failed: {e}")
        return False

def test_assistant_integration():
    """Test TTS integration with main assistant"""
    
    print("\n🧪 TESTING ASSISTANT INTEGRATION")
    print("=" * 40)
    
    try:
        from assistant import TotoroAssistant
        
        print("📦 Creating assistant instance...")
        # This will test TTS during initialization
        assistant = TotoroAssistant()
        
        print("✅ Assistant created successfully!")
        
        # Test speaking method
        print("🗣️ Testing assistant speak method...")
        success = assistant.speak("Assistant integration test successful!")
        
        if success:
            print("🎉 Assistant integration test successful!")
            return True
        else:
            print("❌ Assistant speak method failed")
            return False
            
    except Exception as e:
        print(f"❌ Assistant integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🔬 COQUI TTS COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Direct Coqui TTS", test_coqui_direct),
        ("Integrated TTS System", test_integrated_tts),
        ("Assistant Integration", test_assistant_integration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("Coqui TTS is working correctly!")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Check the logs above for details")
        
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Ensure TTS is installed: pip install TTS")
        print("2. Check George's voice file exists: assets/george-source-voice.mp3")
        print("3. Verify audio system is working")

if __name__ == "__main__":
    main() 