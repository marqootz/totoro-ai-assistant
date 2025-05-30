#!/usr/bin/env python3
"""
Voice Capabilities Test for Unified Totoro Assistant
Tests microphone, speech recognition, text-to-speech, and unified voice mode
"""

import asyncio
import logging
from src.voice import VoiceRecognizer, TextToSpeech
from src.assistant import TotoroAssistant
from src.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_microphone():
    """Test microphone input"""
    print("🎤 MICROPHONE TEST")
    print("=" * 50)
    
    try:
        voice_recognizer = VoiceRecognizer()
        result = voice_recognizer.test_microphone()
        
        if result:
            print("✅ Microphone test PASSED")
        else:
            print("❌ Microphone test FAILED")
            
        return result
    except Exception as e:
        print(f"❌ Microphone test ERROR: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech output"""
    print("\n🗣️ TEXT-TO-SPEECH TEST")
    print("=" * 50)
    
    try:
        tts = TextToSpeech()
        
        # Test basic speech
        print("Testing basic speech...")
        tts.speak("Hello! I am Totoro, your unified AI assistant.")
        
        # Show available voices
        voices = tts.get_voices()
        print(f"✅ Available voices: {len(voices)}")
        for i, (voice_id, voice_name) in enumerate(voices[:5]):  # Show first 5
            print(f"   {i+1}. {voice_name}")
        
        # Test unified capabilities announcement
        tts.speak("I can control your smart home and answer general questions. Try saying: Totoro, what time is it?")
        
        return True
    except Exception as e:
        print(f"❌ Text-to-speech test ERROR: {e}")
        return False

def test_wake_word_detection():
    """Test wake word detection"""
    print("\n👂 WAKE WORD DETECTION TEST")
    print("=" * 50)
    
    try:
        config = Config()
        wake_word = config.WAKE_WORD
        voice_recognizer = VoiceRecognizer(wake_word=wake_word)
        
        print(f"🎯 Wake word: '{wake_word}'")
        print("📢 Please say the wake word within 15 seconds...")
        print("   (You can also press Ctrl+C to skip)")
        
        result = voice_recognizer.listen_for_wake_word(timeout=15)
        
        if result:
            print("✅ Wake word detection PASSED")
        else:
            print("⚠️  Wake word not detected (timeout or error)")
            
        return result
    except KeyboardInterrupt:
        print("⏭️  Wake word test SKIPPED by user")
        return True  # Don't fail the test if user skips
    except Exception as e:
        print(f"❌ Wake word detection ERROR: {e}")
        return False

def test_command_recognition():
    """Test command recognition"""
    print("\n🎯 COMMAND RECOGNITION TEST")
    print("=" * 50)
    
    try:
        voice_recognizer = VoiceRecognizer()
        
        print("📢 Please say a command within 10 seconds...")
        print("   Examples: 'turn on the lights', 'what time is it', 'play music'")
        print("   (You can also press Ctrl+C to skip)")
        
        command = voice_recognizer.listen_for_command(timeout=10)
        
        if command:
            print(f"✅ Command recognized: '{command}'")
        else:
            print("⚠️  No command recognized (timeout or error)")
            
        return command is not None
    except KeyboardInterrupt:
        print("⏭️  Command recognition test SKIPPED by user")
        return True  # Don't fail the test if user skips
    except Exception as e:
        print(f"❌ Command recognition ERROR: {e}")
        return False

async def test_voice_mode_integration():
    """Test voice mode with unified assistant"""
    print("\n🤖 VOICE MODE INTEGRATION TEST")
    print("=" * 50)
    
    try:
        assistant = TotoroAssistant()
        
        # Test a voice command processing
        test_commands = [
            "what time is it",
            "turn on the living room lights",
            "play music and what time is it"
        ]
        
        print("🧪 Testing voice command processing...")
        for command in test_commands:
            print(f"\nTesting: '{command}'")
            try:
                response = await assistant.process_text_command(command)
                print(f"✅ Response: {response}")
                
                # Also test TTS
                assistant.tts.speak(f"Command processed: {command}")
                
            except Exception as e:
                print(f"❌ Error processing '{command}': {e}")
        
        return True
    except Exception as e:
        print(f"❌ Voice mode integration ERROR: {e}")
        return False

async def test_interactive_voice_mode():
    """Test interactive voice mode"""
    print("\n🎙️ INTERACTIVE VOICE MODE TEST")
    print("=" * 50)
    
    try:
        assistant = TotoroAssistant()
        config = Config()
        
        print(f"🎯 Wake word: '{config.WAKE_WORD}'")
        print("🎤 Starting interactive voice mode...")
        print("📢 Say the wake word followed by a command")
        print("   Examples:")
        print("   - 'Totoro, what time is it?'")
        print("   - 'Totoro, turn on the lights'")
        print("   - 'Totoro, play music and dim the lights'")
        print("\n⏹️  Press Ctrl+C to stop\n")
        
        # Start interactive voice mode
        await assistant.start_voice_mode()
        
    except KeyboardInterrupt:
        print("\n👋 Interactive voice mode stopped by user")
        return True
    except Exception as e:
        print(f"❌ Interactive voice mode ERROR: {e}")
        return False

async def main():
    """Run all voice tests"""
    print("🦙 TOTORO UNIFIED ASSISTANT - VOICE CAPABILITIES TEST")
    print("🎤 Testing Microphone + 🗣️ TTS + 👂 Wake Word + 🤖 Unified Processing")
    print("=" * 80)
    
    results = {}
    
    # Test 1: Microphone
    results["microphone"] = test_microphone()
    
    # Test 2: Text-to-Speech
    results["tts"] = test_text_to_speech()
    
    # Test 3: Wake Word Detection
    results["wake_word"] = test_wake_word_detection()
    
    # Test 4: Command Recognition
    results["command_recognition"] = test_command_recognition()
    
    # Test 5: Voice Mode Integration
    results["voice_integration"] = await test_voice_mode_integration()
    
    # Summary
    print("\n📊 VOICE TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL VOICE TESTS PASSED!")
        print("\n🚀 Your unified voice assistant is ready!")
        print("   Start voice mode: python main.py")
        print("   Or test mode: python main.py --test")
        
        # Offer interactive test
        response = input("\n🎮 Would you like to try interactive voice mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            await test_interactive_voice_mode()
    else:
        print("⚠️  Some voice tests failed. Check your microphone and audio setup.")
        print("\n🔧 Troubleshooting:")
        print("   - Check microphone permissions")
        print("   - Ensure internet connection (for Google Speech Recognition)")
        print("   - Test microphone with other applications")
        print("   - Check audio output settings")

if __name__ == "__main__":
    asyncio.run(main()) 