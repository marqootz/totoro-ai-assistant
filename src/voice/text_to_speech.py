import pyttsx3
import os
import tempfile
import pygame
import logging
from typing import Optional
import threading
import time

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Text-to-speech with neural voices using Coqui TTS"""
    
    def __init__(self, voice_preference: str = "neural"):
        self.voice_preference = voice_preference
        self.tts_engine = None
        self.neural_tts = None
        self._lock = threading.Lock()
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            logger.info("Audio mixer initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize audio mixer: {e}")
        
        # Try to initialize neural TTS first (only if requested and compatible)
        if voice_preference == "neural":
            self._init_neural_tts()
            # If neural TTS failed, fall back to system preference
            if not self.neural_tts:
                logger.info("Switching to system TTS as fallback")
                self.voice_preference = "system"
        
        # Always initialize fallback pyttsx3
        self._init_pyttsx3()
    
    def _init_neural_tts(self):
        """Initialize Coqui TTS for neural voices"""
        try:
            # Check Python version compatibility first
            import sys
            if sys.version_info < (3, 10):
                logger.info("Python 3.10+ recommended for optimal TTS performance. Using fallback TTS.")
                self.neural_tts = None
                return
            
            from TTS.api import TTS
            
            # Use a fast, high-quality English model
            model_name = "tts_models/en/ljspeech/tacotron2-DDC_ph"
            
            logger.info(f"Loading neural TTS model: {model_name}")
            self.neural_tts = TTS(model_name=model_name, progress_bar=False)
            logger.info("✅ Neural TTS initialized successfully!")
            
        except ImportError as e:
            logger.info(f"TTS library not available: {e}")
            logger.info("Install with: pip install TTS")
            self.neural_tts = None
        except Exception as e:
            logger.warning(f"Neural TTS initialization failed: {e}")
            logger.info("Will fall back to system TTS")
            self.neural_tts = None
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 as fallback"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Use Samantha voice if available (most natural on macOS)
                for voice in voices:
                    if 'samantha' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        logger.info(f"Using fallback voice: {voice.name}")
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
                    logger.info(f"Using fallback voice: {voices[0].name}")
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Moderate speed
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            logger.error(f"Failed to initialize fallback TTS: {e}")
            self.tts_engine = None
    
    def speak(self, text: str) -> bool:
        """Speak text using neural TTS (preferred) or fallback"""
        if not text.strip():
            return False
        
        with self._lock:
            # Try neural TTS first
            if self.neural_tts and self.voice_preference == "neural":
                if self._speak_neural(text):
                    return True
                logger.warning("Neural TTS failed, falling back to system TTS")
            
            # Fall back to pyttsx3
            return self._speak_pyttsx3(text)
    
    def _speak_neural(self, text: str) -> bool:
        """Speak using neural TTS"""
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generate speech with neural TTS
            logger.debug(f"Generating neural speech for: {text[:50]}...")
            self.neural_tts.tts_to_file(text=text, file_path=temp_path)
            
            # Play the generated audio
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            os.unlink(temp_path)
            logger.debug("Neural speech completed")
            return True
            
        except Exception as e:
            logger.error(f"Neural TTS error: {e}")
            # Clean up temp file if it exists
            try:
                if 'temp_path' in locals():
                    os.unlink(temp_path)
            except:
                pass
            return False
    
    def _speak_pyttsx3(self, text: str) -> bool:
        """Speak using pyttsx3 fallback"""
        try:
            if not self.tts_engine:
                logger.error("No TTS engine available")
                return False
            
            logger.debug(f"Speaking with fallback TTS: {text[:50]}...")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
            
        except Exception as e:
            logger.error(f"Fallback TTS error: {e}")
            return False
    
    def set_voice_preference(self, preference: str):
        """Set voice preference: 'neural' or 'system'"""
        self.voice_preference = preference
        logger.info(f"Voice preference set to: {preference}")
    
    def list_available_voices(self):
        """List available system voices (pyttsx3)"""
        try:
            if self.tts_engine:
                voices = self.tts_engine.getProperty('voices')
                print("Available system voices:")
                for i, voice in enumerate(voices):
                    print(f"  {i}: {voice.name} ({voice.id})")
                return voices
        except Exception as e:
            logger.error(f"Error listing voices: {e}")
        return []
    
    def test_speech(self, text: str = "Hello! I'm your Totoro assistant with neural voice synthesis."):
        """Test speech output"""
        logger.info("Testing speech output...")
        
        if self.neural_tts:
            logger.info("🎤 Testing neural TTS...")
            success = self._speak_neural(text)
            if success:
                logger.info("✅ Neural TTS working!")
                return True
            else:
                logger.warning("❌ Neural TTS failed")
        
        logger.info("🔄 Testing fallback TTS...")
        success = self._speak_pyttsx3(text)
        if success:
            logger.info("✅ Fallback TTS working!")
            return True
        else:
            logger.error("❌ All TTS methods failed!")
            return False 