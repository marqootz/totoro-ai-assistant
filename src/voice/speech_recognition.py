import speech_recognition as sr
import threading
import queue
import time
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)

class VoiceRecognizer:
    """Handles speech recognition with wake word detection"""
    
    def __init__(self, wake_word: str = "totoro", callback: Optional[Callable] = None):
        self.wake_word = wake_word.lower()
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stop_listening = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
            logger.info("Ready for voice commands!")
    
    def start_listening(self):
        """Start continuous listening for wake word"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self._audio_callback,
            phrase_time_limit=5
        )
        logger.info(f"Listening for wake word: '{self.wake_word}'")
    
    def stop_listening_for_commands(self):
        """Stop listening for commands"""
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
            self.is_listening = False
            logger.info("Stopped listening")
    
    def _audio_callback(self, recognizer, audio):
        """Callback for processing audio in background"""
        try:
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio).lower()
            logger.debug(f"Heard: {text}")
            
            if self.wake_word in text:
                logger.info(f"Wake word '{self.wake_word}' detected!")
                # Extract command after wake word
                command = self._extract_command(text)
                if command and self.callback:
                    self.callback(command)
                    
        except sr.UnknownValueError:
            # Speech was unintelligible
            pass
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
    
    def _extract_command(self, text: str) -> Optional[str]:
        """Extract command from text after wake word"""
        wake_word_index = text.find(self.wake_word)
        if wake_word_index != -1:
            command_start = wake_word_index + len(self.wake_word)
            command = text[command_start:].strip()
            return command if command else None
        return None
    
    def listen_for_command(self, timeout: int = 10) -> Optional[str]:
        """Listen for a single command with timeout"""
        try:
            with self.microphone as source:
                logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            command = self.recognizer.recognize_google(audio)
            logger.info(f"Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None 