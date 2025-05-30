import pyttsx3
import threading
import queue
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Handles text-to-speech output"""
    
    def __init__(self, rate: int = 200, volume: float = 0.9):
        self.engine = pyttsx3.init()
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        
        # Configure voice settings
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Try to set a pleasant voice
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            else:
                # Use first available voice
                self.engine.setProperty('voice', voices[0].id)
        
        logger.info("Text-to-speech initialized")
    
    def speak(self, text: str, interrupt: bool = False):
        """Speak the given text"""
        if interrupt and self.is_speaking:
            self.stop()
        
        if not text.strip():
            return
            
        logger.info(f"Speaking: {text}")
        
        # Run speech in separate thread to avoid blocking
        speech_thread = threading.Thread(target=self._speak_threaded, args=(text,))
        speech_thread.daemon = True
        speech_thread.start()
    
    def _speak_threaded(self, text: str):
        """Internal method to handle speech in separate thread"""
        try:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error during speech: {e}")
        finally:
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
            self.is_speaking = False
            logger.info("Speech stopped")
        except Exception as e:
            logger.error(f"Error stopping speech: {e}")
    
    def set_rate(self, rate: int):
        """Set speech rate"""
        self.engine.setProperty('rate', rate)
        logger.info(f"Speech rate set to {rate}")
    
    def set_volume(self, volume: float):
        """Set speech volume (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', volume)
        logger.info(f"Speech volume set to {volume}")
    
    def get_voices(self):
        """Get available voices"""
        voices = self.engine.getProperty('voices')
        return [(voice.id, voice.name) for voice in voices] if voices else []
    
    def set_voice(self, voice_id: str):
        """Set voice by ID"""
        try:
            self.engine.setProperty('voice', voice_id)
            logger.info(f"Voice set to {voice_id}")
        except Exception as e:
            logger.error(f"Error setting voice: {e}") 