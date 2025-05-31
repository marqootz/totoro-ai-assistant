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
        self.is_running = False
        self.visual_state = 'idle'
        self.state_lock = threading.Lock()
        self.state_callbacks = []
        
        # Session management
        self.wake_session_active = False
        self.session_lock = threading.Lock()
        
        # Initialize components
        logger.info("Initializing Totoro Assistant...")
        self.initialize_components()
        
        # Test startup with George's voice if configured
        self.george_voice_path = config.GEORGE_VOICE_PATH
        if self.george_voice_path:
            logger.info("✨ Using George's cloned voice")
            self.speak("Hello! Totoro assistant ready with George's cloned voice.")
        else:
            self.tts.speak("Hello! Totoro assistant ready with Coqui neural voice synthesis.")
        
        self.set_visual_state('idle')
    
    def initialize_components(self):
        """Initialize all assistant components"""
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
        
        # Check for George's voice configuration
        if hasattr(config, 'USE_GEORGE_VOICE') and config.USE_GEORGE_VOICE:
            if hasattr(config, 'GEORGE_VOICE_PATH') and os.path.exists(config.GEORGE_VOICE_PATH):
                self.george_voice_path = config.GEORGE_VOICE_PATH
                logger.info(f"🎭 George's voice enabled: {self.george_voice_path}")
            else:
                logger.warning("George voice enabled in config but audio file not found")
        
        logger.info("✅ Totoro Assistant initialized successfully!")
    
    def set_visual_state(self, state: str):
        """Set the current visual state for the frontend"""
        valid_states = ['idle', 'awake', 'thinking', 'speaking']
        if state not in valid_states:
            logger.warning(f"Invalid visual state: {state}")
            return
            
        with self.state_lock:
            if self.visual_state != state:
                self.visual_state = state
                logger.debug(f"Visual state changed to: {state}")
                
                # Notify any registered callbacks
                for callback in self.state_callbacks:
                    try:
                        callback(state)
                    except Exception as e:
                        logger.error(f"Error in state callback: {e}")
    
    def get_visual_state(self) -> str:
        """Get the current visual state"""
        with self.state_lock:
            return self.visual_state
    
    def register_state_callback(self, callback):
        """Register a callback to be called when state changes"""
        self.state_callbacks.append(callback)
    
    def handle_voice_command(self, command: str):
        """Handle voice command from wake word detection"""
        try:
            logger.info(f"Processing voice command: {command}")
            self.set_visual_state('awake')
            time.sleep(0.5)  # Brief awake moment
            
            self.set_visual_state('thinking')
            response = self.process_command(command)
            
            self.set_visual_state('speaking')
            self.speak(response)
            
            self.set_visual_state('idle')
        except Exception as e:
            logger.error(f"Error handling voice command: {e}")
            self.set_visual_state('speaking')
            self.speak("Sorry, I encountered an error processing your command.")
            self.set_visual_state('idle')
    
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
        self.set_visual_state('idle')
        
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
        
        self.set_visual_state('speaking')
        self.speak("Goodbye!")
        self.set_visual_state('idle')
        
        logger.info("Voice mode stopped")
    
    def start_wake_word_session(self):
        """Start a single wake word listening session"""
        # Check if a session is already active
        with self.session_lock:
            if self.wake_session_active:
                logger.warning("Wake word session already active, skipping new session")
                return "Session already active"
            
            # Mark session as active
            self.wake_session_active = True
        
        try:
            logger.info(f"🎧 Listening for wake word: '{config.WAKE_WORD}'...")
            self.set_visual_state('idle')
            
            if self.voice_recognizer.listen_for_wake_word(timeout=config.RECOGNITION_TIMEOUT):
                logger.info("Wake word detected!")
                self.set_visual_state('awake')
                time.sleep(0.5)
                
                # Listen for command
                command = self.voice_recognizer.listen_for_command(timeout=config.COMMAND_TIMEOUT)
                if command:
                    self.set_visual_state('thinking')
                    response = self.process_command(command)
                    
                    self.set_visual_state('speaking')
                    self.speak(response)
                    self.set_visual_state('idle')
                    return response
                else:
                    self.set_visual_state('speaking')
                    self.speak("I didn't catch that. Could you try again?")
                    self.set_visual_state('idle')
                    return "No command detected"
            else:
                logger.info("No wake word detected within timeout")
                self.set_visual_state('idle')
                return "No wake word detected"
        
        finally:
            # Always release the session lock
            with self.session_lock:
                self.wake_session_active = False
                logger.debug("Wake word session ended")
    
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
            "visual_state": self.get_visual_state(),
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
    
    def speak(self, text: str) -> bool:
        """Speak text using George's voice if configured, otherwise use default TTS"""
        if self.george_voice_path:
            return self.tts.speak(text, audio_prompt_path=self.george_voice_path)
        else:
            return self.tts.speak(text) 