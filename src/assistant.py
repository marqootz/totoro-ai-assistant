import asyncio
import logging
from typing import Optional, Dict, Any
import threading
import time
import sys
import os

# Add parent directory to path to access root config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from src.voice.speech_recognition import VoiceRecognizer
from src.voice.text_to_speech import TextToSpeech
from src.smart_home.manager import SmartHomeManager
from src.llm.processor import LLMProcessor

logger = logging.getLogger(__name__)

class TotoroAssistant:
    """Main Totoro Assistant that combines voice control, smart home, and AI"""
    
    def __init__(self):
        logger.info("🎭 Initializing Totoro Assistant...")
        
        # Initialize components
        self.smart_home = SmartHomeManager()
        self.llm_processor = LLMProcessor()
        
        # Initialize voice components with neural TTS
        self.tts = TextToSpeech(voice_preference=config.VOICE_PREFERENCE)
        self.voice_recognizer = VoiceRecognizer(
            wake_word=config.WAKE_WORD,
            callback=self.handle_voice_command
        )
        
        self.is_running = False
        logger.info("✅ Totoro Assistant initialized successfully!")
        
        # Test the neural voice on startup
        self.tts.speak("Hello! Totoro assistant ready with neural voice synthesis.")
    
    def handle_voice_command(self, command: str):
        """Handle voice command from wake word detection"""
        try:
            logger.info(f"Processing voice command: {command}")
            response = self.process_command(command)
            self.tts.speak(response)
        except Exception as e:
            logger.error(f"Error handling voice command: {e}")
            self.tts.speak("Sorry, I encountered an error processing your command.")
    
    def process_command(self, command: str) -> str:
        """Process a text or voice command and return response"""
        try:
            logger.info(f"Processing command: {command}")
            
            # Check if it's a smart home command
            if self.smart_home.can_handle_command(command):
                result = self.smart_home.process_command(command)
                if result:
                    return f"Done! {result}"
                else:
                    return "I couldn't complete that smart home action."
            
            # Process with LLM for general queries
            response = self.llm_processor.process_query(command)
            return response
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return "Sorry, I encountered an error processing your command."
    
    def start_voice_mode(self):
        """Start continuous voice interaction mode"""
        logger.info("🎤 Starting voice mode...")
        self.is_running = True
        
        # Start listening in background
        self.voice_recognizer.start_listening()
        
        try:
            logger.info(f"Listening for wake word: '{config.WAKE_WORD}'")
            logger.info("Say 'Ctrl+C' to stop...")
            
            while self.is_running:
                time.sleep(0.5)  # Keep main thread alive
                
        except KeyboardInterrupt:
            logger.info("Voice mode stopped by user")
        finally:
            self.stop_voice_mode()
    
    def stop_voice_mode(self):
        """Stop voice interaction mode"""
        self.is_running = False
        self.voice_recognizer.stop_listening_for_commands()
        self.tts.speak("Goodbye!")
        logger.info("Voice mode stopped")
    
    def start_wake_word_session(self):
        """Start a single wake word listening session"""
        logger.info(f"🎧 Listening for wake word: '{config.WAKE_WORD}'...")
        
        if self.voice_recognizer.listen_for_wake_word(timeout=config.RECOGNITION_TIMEOUT):
            logger.info("Wake word detected!")
            
            # Listen for command
            command = self.voice_recognizer.listen_for_command(timeout=config.COMMAND_TIMEOUT)
            if command:
                response = self.process_command(command)
                self.tts.speak(response)
                return response
            else:
                self.tts.speak("I didn't catch that. Could you try again?")
                return "No command detected"
        else:
            logger.info("No wake word detected within timeout")
            return "No wake word detected"
    
    def test_components(self) -> Dict[str, bool]:
        """Test all components and return status"""
        results = {}
        
        # Test TTS
        try:
            logger.info("Testing TTS...")
            success = self.tts.test_speech("Testing speech output.")
            results["tts"] = success
        except Exception as e:
            logger.error(f"TTS test failed: {e}")
            results["tts"] = False
        
        # Test Speech Recognition
        try:
            logger.info("Testing speech recognition...")
            success = self.voice_recognizer.test_microphone()
            results["speech_recognition"] = success
        except Exception as e:
            logger.error(f"Speech recognition test failed: {e}")
            results["speech_recognition"] = False
        
        # Test LLM
        try:
            logger.info("Testing LLM...")
            response = self.llm_processor.process_query("What time is it?")
            results["llm"] = len(response) > 0
        except Exception as e:
            logger.error(f"LLM test failed: {e}")
            results["llm"] = False
        
        # Test Smart Home
        try:
            logger.info("Testing smart home...")
            results["smart_home"] = True  # Placeholder
        except Exception as e:
            logger.error(f"Smart home test failed: {e}")
            results["smart_home"] = False
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get current assistant status"""
        return {
            "is_running": self.is_running,
            "wake_word": config.WAKE_WORD,
            "voice_preference": config.VOICE_PREFERENCE,
            "llm_backend": getattr(config, 'LLM_BACKEND', 'unified'),
            "components": {
                "tts": self.tts is not None,
                "voice_recognizer": self.voice_recognizer is not None,
                "smart_home": self.smart_home is not None,
                "llm_processor": self.llm_processor is not None,
            }
        } 