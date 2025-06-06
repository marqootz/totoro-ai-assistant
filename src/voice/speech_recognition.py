import speech_recognition as sr
import threading
import queue
import time
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)

class VoiceRecognizer:
    """Handles speech recognition with wake word detection and continuous dialog"""
    
    def __init__(self, wake_word: str = "totoro", sleep_word: str = "goodbye", callback: Optional[Callable] = None):
        self.wake_word = wake_word.lower()
        self.sleep_word = sleep_word.lower()
        self.callback = callback
        self.recognizer = sr.Recognizer()
        
        # Set a much lower energy threshold for better detection
        self.recognizer.energy_threshold = 300  # Lower threshold for quiet environments
        self.recognizer.dynamic_energy_threshold = True  # Allow automatic adjustment
        
        self.microphone = None
        self.is_listening = False
        self.is_continuous_mode = False
        self.audio_queue = queue.Queue()
        self.stop_listening = None
        self.wake_word_detected = threading.Event()
        self.last_speech_time = 0
        self.continuous_timeout = 30  # Timeout for continuous mode in seconds
        
        # Use system default microphone (simplified)
        self._initialize_default_microphone()
        
        # Adjust for ambient noise with lower baseline
        if self.microphone:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Ensure threshold doesn't get too high
                if self.recognizer.energy_threshold > 1000:
                    self.recognizer.energy_threshold = 400
                    logger.info(f"Reset high energy threshold to: {self.recognizer.energy_threshold}")
                logger.info(f"Energy threshold set to: {self.recognizer.energy_threshold}")
                logger.info("Ready for voice commands!")
        else:
            logger.error("No microphone available!")
    
    def _initialize_default_microphone(self):
        """Initialize system default microphone (simplified)"""
        try:
            # Try different microphones in order of preference for Mac Studio
            microphones_to_try = [
                (2, "Logitech BRIO"),      # Best choice for Mac Studio - high quality USB mic
                (0, "iPhone Microphone"),  # Good fallback when iPhone connected  
                (None, "System Default"),   # System default
            ]
            
            for mic_index, mic_name in microphones_to_try:
                try:
                    if mic_index is not None:
                        self.microphone = sr.Microphone(device_index=mic_index)
                        logger.info(f"Using {mic_name} microphone (index {mic_index})")
                    else:
                        self.microphone = sr.Microphone()
                        logger.info(f"Using {mic_name} microphone")
                    
                    # Test the microphone briefly
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        logger.info(f"✅ {mic_name} microphone working, energy threshold: {self.recognizer.energy_threshold}")
                    
                    return  # Success, exit the function
                    
                except Exception as e:
                    logger.warning(f"❌ {mic_name} microphone failed: {e}")
                    continue
            
            # If all specific microphones failed, try system default as last resort
            logger.warning("All preferred microphones failed, using system default")
            self.microphone = sr.Microphone()
            
        except Exception as e:
            logger.error(f"Failed to initialize any microphone: {e}")
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
        """Listen for wake word with timeout and robust error handling"""
        if not self.microphone:
            logger.error("No microphone available for wake word detection")
            return False
        
        # Stop any ongoing continuous listening to avoid microphone conflicts
        if self.is_listening:
            logger.info("🔄 Stopping continuous listening to start wake word session...")
            self.stop_listening_for_commands()
            time.sleep(0.5)  # Give time for cleanup
            
        try:
            logger.info(f"🎧 Listening for wake word: '{self.wake_word}' (timeout: {timeout}s)")
            
            start_time = time.time()
            attempts = 0
            consecutive_failures = 0
            
            while (time.time() - start_time) < timeout:
                attempts += 1
                try:
                    # Create a fresh microphone context for each attempt to avoid context manager conflicts
                    logger.debug(f"👂 Attempt {attempts}: Listening for audio...")
                    
                    # Use a fresh context each time to avoid conflicts
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=4)
                    
                    # Recognize speech with better error handling
                    logger.debug("🔄 Processing audio with Google Speech API...")
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        logger.info(f"👂 Heard: '{text}'")
                        consecutive_failures = 0  # Reset failure counter
                        
                        # More flexible wake word matching
                        text_lower = text.lower()
                        wake_word_variations = [
                            self.wake_word,
                            "totoro",
                            "toto",
                            "to toro",
                            "to to ro",
                            "to to",
                            "toro"
                        ]
                        
                        # Check if any variation of the wake word is present
                        if any(variation in text_lower for variation in wake_word_variations):
                            logger.info(f"🎉 Wake word detected in: '{text}'")
                            return True
                            
                    except sr.UnknownValueError:
                        # Speech was unintelligible - continue listening
                        logger.debug(f"❓ Could not understand audio on attempt {attempts}")
                        consecutive_failures += 1
                        continue
                    except sr.RequestError as e:
                        logger.error(f"❌ Speech recognition service error: {e}")
                        consecutive_failures += 1
                        # If too many consecutive failures, wait longer
                        if consecutive_failures >= 3:
                            logger.warning("Multiple API failures, waiting 2 seconds...")
                            time.sleep(2)
                            consecutive_failures = 0
                        continue
                        
                except sr.WaitTimeoutError:
                    # Continue listening - this is normal
                    logger.debug(f"⏰ Timeout on attempt {attempts}, continuing...")
                    continue
                except Exception as e:
                    logger.error(f"Microphone context error on attempt {attempts}: {e}")
                    # Wait a bit before retrying to avoid rapid failures
                    time.sleep(0.5)
                    continue
                    
                # Small delay between attempts to avoid overwhelming the API
                time.sleep(0.1)
                    
            logger.info(f"⏰ Wake word listening timed out after {timeout}s ({attempts} attempts)")
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
            try:
                logger.info("🛑 Stopping continuous listening...")
                self.stop_listening(wait_for_stop=True)  # Wait for proper cleanup
                self.stop_listening = None
                self.is_listening = False
                logger.info("✅ Continuous listening stopped")
            except Exception as e:
                logger.error(f"Error stopping continuous listening: {e}")
                # Force reset the state even if there was an error
                self.stop_listening = None
                self.is_listening = False
        else:
            # Just reset the state if no active listener
            self.is_listening = False
    
    def _audio_callback(self, recognizer, audio):
        """Callback for processing audio in background"""
        try:
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio).lower()
            logger.debug(f"Heard: {text}")
            
            # Update last speech time
            self.last_speech_time = time.time()
            
            # Check for sleep word in continuous mode
            if self.is_continuous_mode:
                sleep_word_variations = [
                    self.sleep_word,
                    "goodbye",
                    "good bye",
                    "bye",
                    "stop",
                    "exit"
                ]
                
                if any(variation in text for variation in sleep_word_variations):
                    logger.info(f"Sleep word '{self.sleep_word}' detected!")
                    self.is_continuous_mode = False
                    self.stop_listening_for_commands()
                    return
            
            # Check for wake word if not in continuous mode
            if not self.is_continuous_mode:
                wake_word_variations = [
                    self.wake_word,
                    "totoro",
                    "toto",
                    "to toro",
                    "to to ro",
                    "to to",
                    "toro"
                ]
                
                if any(variation in text for variation in wake_word_variations):
                    logger.info(f"Wake word '{self.wake_word}' detected!")
                    self.is_continuous_mode = True
                    # Extract command after wake word
                    command = self._extract_command(text)
                    if command and self.callback:
                        self.callback(command)
                    return
            
            # In continuous mode, process all speech as commands
            if self.is_continuous_mode and self.callback:
                self.callback(text)
                
        except sr.UnknownValueError:
            # Speech was unintelligible
            pass
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
    
    def start_continuous_listening(self):
        """Start continuous listening mode"""
        if not self.is_listening:
            self.start_listening()
        
        self.is_continuous_mode = True
        self.last_speech_time = time.time()
        
        # Start a thread to check for timeout
        def check_timeout():
            while self.is_continuous_mode:
                if time.time() - self.last_speech_time > self.continuous_timeout:
                    logger.info(f"No speech detected for {self.continuous_timeout} seconds, exiting continuous mode")
                    self.is_continuous_mode = False
                    break
                time.sleep(1)
        
        threading.Thread(target=check_timeout, daemon=True).start()
        logger.info("Entered continuous dialog mode")
    
    def stop_continuous_listening(self):
        """Stop continuous listening mode"""
        self.is_continuous_mode = False
        logger.info("Exited continuous dialog mode")
    
    def _extract_command(self, text: str) -> Optional[str]:
        """Extract command from text after wake word"""
        text_lower = text.lower()
        wake_word_variations = [
            self.wake_word,
            "totoro",
            "toto",
            "to toro",
            "to to ro",
            "to to",
            "toro"
        ]
        
        # Find the earliest occurrence of any wake word variation
        earliest_index = len(text)
        for variation in wake_word_variations:
            index = text_lower.find(variation)
            if index != -1 and index < earliest_index:
                earliest_index = index
        
        if earliest_index < len(text):
            # Find the end of the wake word
            command_start = earliest_index
            for variation in wake_word_variations:
                if text_lower[command_start:].startswith(variation):
                    command_start += len(variation)
                    break
            
            # Extract and clean up the command
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