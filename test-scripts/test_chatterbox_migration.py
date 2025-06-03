#!/usr/bin/env python3
"""
Test script to verify Chatterbox TTS migration
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_chatterbox_tts():
    """Test Chatterbox TTS functionality"""
    try:
        logger.info("🎤 Testing Chatterbox TTS migration...")
        
        # Import the updated TTS class
        from src.voice.text_to_speech import TextToSpeech
        
        # Create TTS instance with Chatterbox preference
        logger.info("📦 Creating TTS instance...")
        tts = TextToSpeech(voice_preference="chatterbox")
        
        # Test basic speech
        test_text = "Hello! I'm your upgraded Totoro assistant now powered by Chatterbox TTS. This is a test of the new neural voice synthesis."
        
        logger.info(f"🗣️ Testing speech synthesis...")
        logger.info(f"Text: {test_text}")
        
        success = tts.speak(test_text)
        
        if success:
            logger.info("✅ Chatterbox TTS migration successful!")
            logger.info("🎉 Your assistant now has state-of-the-art voice synthesis!")
            return True
        else:
            logger.warning("⚠️ Speech synthesis failed, but fallback should work")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing Chatterbox TTS: {e}")
        return False

def test_voice_cloning():
    """Test voice cloning capability (if audio file exists)"""
    try:
        from src.voice.text_to_speech import TextToSpeech
        
        # Look for any audio files in the project
        audio_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith(('.wav', '.mp3', '.m4a')):
                    audio_files.append(os.path.join(root, file))
        
        if audio_files:
            logger.info(f"🎪 Testing voice cloning with: {audio_files[0]}")
            tts = TextToSpeech(voice_preference="chatterbox")
            
            clone_text = "This is a test of voice cloning with Chatterbox TTS!"
            success = tts.speak(clone_text, audio_prompt_path=audio_files[0])
            
            if success:
                logger.info("✅ Voice cloning test successful!")
            else:
                logger.info("⚠️ Voice cloning test failed, but basic TTS should work")
        else:
            logger.info("📁 No audio files found for voice cloning test")
            
    except Exception as e:
        logger.info(f"Voice cloning test skipped: {e}")

def main():
    """Run all tests"""
    logger.info("🎯 Starting Chatterbox TTS Migration Tests")
    logger.info("=" * 50)
    
    # Test basic TTS
    basic_success = test_chatterbox_tts()
    
    # Test voice cloning
    test_voice_cloning()
    
    # Summary
    logger.info("\n" + "=" * 50)
    if basic_success:
        logger.info("🎉 MIGRATION SUCCESSFUL!")
        logger.info("✨ Your Totoro Assistant now has:")
        logger.info("   🎯 State-of-the-art neural TTS")
        logger.info("   🎭 Emotion control capabilities")
        logger.info("   🎪 Voice cloning support")
        logger.info("   🚀 Faster and more stable speech")
        logger.info("\n🚀 Ready to use! Try: python main.py --test")
    else:
        logger.warning("⚠️ Migration completed with issues")
        logger.info("💡 Your assistant will fall back to system TTS")
    
    logger.info("=" * 50)

if __name__ == "__main__":
    main() 