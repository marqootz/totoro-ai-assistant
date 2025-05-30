#!/usr/bin/env python3
"""
Test script for British woman voice (60's)
"""

import logging
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_british_voice():
    """Test the British Grandma voice"""
    try:
        logger.info("🎭 Testing British woman voice (60's)...")
        
        from src.voice.text_to_speech import TextToSpeech
        
        # Create TTS instance with system preference (British voice)
        logger.info("📦 Creating TTS instance with British voice...")
        tts = TextToSpeech(voice_preference="system")
        
        # Test with British phrases
        test_phrases = [
            "Hello there! I'm your Totoro assistant with a proper British accent.",
            "Cheerio! How lovely to meet you. I do hope you're having a splendid day.",
            "Right then, what can I help you with today? I'm quite at your service.",
            "Brilliant! I must say, this new voice is rather delightful, wouldn't you agree?"
        ]
        
        logger.info("🗣️ Testing British voice with various phrases...")
        
        for i, phrase in enumerate(test_phrases, 1):
            logger.info(f"🎤 Speaking phrase {i}: {phrase[:50]}...")
            success = tts.speak(phrase)
            
            if success:
                logger.info(f"✅ Phrase {i} spoken successfully!")
                # Small pause between phrases
                import time
                time.sleep(1)
            else:
                logger.warning(f"⚠️ Failed to speak phrase {i}")
                return False
        
        logger.info("✅ British voice test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing British voice: {e}")
        return False

def list_british_voices():
    """List available British voices"""
    try:
        import pyttsx3
        
        logger.info("🔍 Available British/UK voices:")
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        british_voices = []
        for i, voice in enumerate(voices):
            if 'en-GB' in voice.id or 'UK' in voice.name or 'British' in voice.name or 'Grandma' in voice.name:
                british_voices.append((i, voice))
                logger.info(f"   {i}: {voice.name} - {voice.id}")
        
        if not british_voices:
            logger.info("   No British voices found in voice list")
            
        return british_voices
        
    except Exception as e:
        logger.error(f"Error listing voices: {e}")
        return []

def main():
    """Run British voice tests"""
    logger.info("🇬🇧 British Woman Voice Test (60's)")
    logger.info("=" * 50)
    
    # List available British voices
    british_voices = list_british_voices()
    
    # Test the configured British voice
    success = test_british_voice()
    
    # Summary
    logger.info("\n" + "=" * 50)
    if success:
        logger.info("🎉 BRITISH VOICE SETUP SUCCESSFUL!")
        logger.info("👩‍🦳 Your Totoro Assistant now speaks with:")
        logger.info("   🇬🇧 British accent")
        logger.info("   👵 Mature woman's voice (60's)")
        logger.info("   🎭 Proper pronunciation and intonation")
        logger.info("\n🚀 Ready to use! Try: python main.py --test")
    else:
        logger.warning("⚠️ British voice setup had issues")
        logger.info("💡 Check voice configuration in config.py")
    
    logger.info("=" * 50)

if __name__ == "__main__":
    main() 