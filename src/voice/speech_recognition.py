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
        self.microphone = None
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stop_listening = None
        self.wake_word_detected = threading.Event()
        
        # Use system default microphone (simplified)
        self._initialize_default_microphone()
        
        # Adjust for ambient noise
        if self.microphone:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info("Ready for voice commands!")
        else:
            logger.error("No microphone available!")
    
    def _initialize_default_microphone(self):
        """Initialize system default microphone (simplified)"""
        try:
            # Just use the system default microphone
            self.microphone = sr.Microphone()
            logger.info("Using system default microphone")
            
        except Exception as e:
            logger.error(f"Failed to initialize default microphone: {e}")
            self.microphone = None
    
    def list_microphones(self):
        """List all available microphones"""
        try:
            mic_names = sr.Microphone.list_microphone_names()
            print("Available microphones:")
            for i, name in enumerate(mic_names):
                print(f"  {i}: {name}")
            return mic_names
        except Exception as e:
            logger.error(f"Error listing microphones: {e}")
            return []
    
    def listen_for_wake_word(self, timeout: int = 30) -> bool:
        """Listen for wake word with timeout"""
        try:
            logger.info(f"Listening for wake word: '{self.wake_word}'...")
            
            while True:
                try:
                    with self.microphone as source:
                        # Listen for audio with shorter timeout for responsiveness
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio, language='en-US').lower()
                    logger.debug(f"Heard: '{text}'")
                    
                    # Check for wake word
                    if self.wake_word in text:
                        logger.info(f"Wake word '{self.wake_word}' detected!")
                        return True
                        
                except sr.WaitTimeoutError:
                    # Continue listening - this is normal
                    continue
                except sr.UnknownValueError:
                    # Speech was unintelligible - continue listening
                    continue
                except sr.RequestError as e:
                    logger.error(f"Speech recognition service error: {e}")
                    return False
                    
        except KeyboardInterrupt:
            logger.info("Wake word listening interrupted by user")
            return False
        except Exception as e:
            logger.error(f"Error in wake word detection: {e}")
            return False
    
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
                # Give user time to speak
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
            
            command = self.recognizer.recognize_google(audio, language='en-US')
            logger.info(f"Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout - no command detected")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def test_microphone(self) -> bool:
        """Test if microphone is working"""
        try:
            with self.microphone as source:
                logger.info("Testing microphone... Please say something.")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Microphone test successful. Heard: '{text}'")
            return True
            
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False 