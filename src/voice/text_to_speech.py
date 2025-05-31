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
    """Text-to-speech using only Coqui TTS (XTTS v2) - No Chatterbox dependencies"""
    
    def __init__(self, voice_preference: str = "coqui"):
        self.voice_preference = voice_preference
        self.tts_engine = None
        self.coqui_tts = None
        self._lock = threading.Lock()
        
        # Initialize audio system once
        self._audio_initialized = False
        self._init_audio_system()
        
        # Initialize TTS engines based on preference
        if voice_preference == "coqui":
            self._init_coqui_tts()
            # Fallback to system TTS if Coqui fails
            if not self.coqui_tts:
                logger.warning("Coqui TTS failed, initializing system TTS fallback")
                self._init_pyttsx3()
        else:
            # For system preference, only use pyttsx3
            self._init_pyttsx3()
    
    def _init_audio_system(self):
        """Initialize audio system once to prevent conflicts"""
        if self._audio_initialized:
            return
            
        try:
            pygame.mixer.quit()  # Ensure clean state
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            self._audio_initialized = True
            logger.info("✅ Audio mixer initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize audio mixer: {e}")
    
    def _init_coqui_tts(self):
        """Initialize Coqui TTS for high-quality neural voices"""
        try:
            from TTS.api import TTS
            import torch
            
            # Fix PyTorch weights loading issue for newer versions
            # Set weights_only=False for trusted Coqui models
            original_load = torch.load
            def patched_load(*args, **kwargs):
                kwargs.setdefault('weights_only', False)
                return original_load(*args, **kwargs)
            torch.load = patched_load
            
            logger.info("🚀 Loading Coqui XTTS v2 model...")
            self.coqui_tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            
            # Restore original torch.load
            torch.load = original_load
            
            # Check if CUDA is available
            try:
                if torch.cuda.is_available():
                    self.coqui_tts = self.coqui_tts.to("cuda")
                    logger.info("🎮 Coqui TTS loaded on GPU")
                else:
                    logger.info("💻 Coqui TTS loaded on CPU")
            except:
                logger.info("💻 Coqui TTS loaded on CPU")
            
            logger.info("✅ Coqui TTS initialized successfully!")
            
        except ImportError as e:
            logger.info(f"Coqui TTS library not available: {e}")
            logger.info("Install with: pip install TTS")
            self.coqui_tts = None
        except Exception as e:
            logger.warning(f"Coqui TTS initialization failed: {e}")
            logger.info("Will fall back to system TTS")
            self.coqui_tts = None
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 as fallback"""
        try:
            import sys
            import os
            
            # Add parent directory to path to access root config
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            import config
            
            self.tts_engine = pyttsx3.init()
            
            # Configure voice settings - prioritize specific voice from config
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # First try to use the configured specific voice
                target_voice_id = getattr(config, 'SYSTEM_VOICE_ID', None)
                target_voice_name = getattr(config, 'SYSTEM_VOICE_NAME', 'Configured Voice')
                
                if target_voice_id:
                    # Look for the specific voice ID
                    for voice in voices:
                        if voice.id == target_voice_id:
                            self.tts_engine.setProperty('voice', voice.id)
                            logger.info(f"✅ Using configured voice: {target_voice_name}")
                            break
                    else:
                        logger.warning(f"⚠️ Configured voice '{target_voice_name}' not found, falling back...")
                        # Fallback to Samantha or first available
                        for voice in voices:
                            if 'samantha' in voice.name.lower():
                                self.tts_engine.setProperty('voice', voice.id)
                                logger.info(f"Using fallback voice: {voice.name}")
                                break
                        else:
                            self.tts_engine.setProperty('voice', voices[0].id)
                            logger.info(f"Using first available voice: {voices[0].name}")
                else:
                    # Original fallback logic
                    for voice in voices:
                        if 'samantha' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            logger.info(f"Using voice: {voice.name}")
                            break
                    else:
                        self.tts_engine.setProperty('voice', voices[0].id)
                        logger.info(f"Using voice: {voices[0].name}")
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.8)
            
            logger.info("✅ System TTS (pyttsx3) initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize fallback TTS: {e}")
            self.tts_engine = None
    
    def speak(self, text: str, audio_prompt_path: Optional[str] = None) -> bool:
        """Speak text using Coqui TTS or system TTS fallback
        
        Args:
            text: Text to synthesize
            audio_prompt_path: Optional path to audio file for voice cloning
        """
        if not text.strip():
            return False
        
        with self._lock:
            logger.info(f"🗣️ Speaking with {self.voice_preference} TTS: {text[:50]}...")
            
            # Use Coqui TTS if available and preferred
            if self.voice_preference == "coqui" and self.coqui_tts:
                success = self._speak_coqui(text, audio_prompt_path)
                if success:
                    logger.info("✅ Coqui TTS completed successfully")
                    return True
                else:
                    logger.error("❌ Coqui TTS failed completely")
                    # Only fallback on complete failure
                    if self.tts_engine:
                        logger.warning("🔄 Falling back to system TTS due to Coqui failure")
                        return self._speak_pyttsx3(text)
                    return False
            
            # For system preference or if Coqui not available
            elif self.tts_engine:
                success = self._speak_pyttsx3(text)
                if success:
                    logger.info("✅ System TTS completed successfully")
                    return True
                else:
                    logger.error("❌ System TTS failed")
                    return False
            else:
                logger.error("❌ No TTS engine available")
                return False
    
    def _speak_coqui(self, text: str, audio_prompt_path: Optional[str] = None) -> bool:
        """Speak using Coqui TTS"""
        try:
            import sys
            import os
            
            # Add parent directory to path to access root config
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            import config
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generate speech with Coqui TTS
            logger.debug(f"Generating Coqui speech...")
            
            # Get George's voice path from config if no specific path provided
            if not audio_prompt_path:
                audio_prompt_path = getattr(config, 'GEORGE_VOICE_PATH', None)
            
            # Coqui XTTS requires a speaker voice for cloning
            if not audio_prompt_path or not os.path.exists(audio_prompt_path):
                logger.error("Coqui XTTS requires a speaker voice file")
                return False
            
            # Generate audio with voice cloning
            self.coqui_tts.tts_to_file(
                text=text,
                speaker_wav=audio_prompt_path,
                language="en",
                file_path=temp_path,
                speed=1.0
            )
            
            logger.debug(f"Voice cloning from: {audio_prompt_path}")
            
            # Stop any previous audio before playing new
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                time.sleep(0.1)
            
            # Play the generated audio
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            os.unlink(temp_path)
            logger.debug("Coqui speech completed")
            return True
            
        except Exception as e:
            logger.error(f"Coqui TTS error: {e}")
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
                logger.error("No system TTS engine available")
                return False
            
            logger.debug(f"Speaking with system TTS...")
            
            # Stop any pygame audio before using pyttsx3
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                time.sleep(0.1)
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
            
        except Exception as e:
            logger.error(f"System TTS error: {e}")
            return False
    
    def set_voice_preference(self, preference: str):
        """Set voice preference: 'coqui' or 'system'"""
        self.voice_preference = preference
        logger.info(f"Voice preference set to: {preference}")
    
    def set_voice_clone(self, audio_prompt_path: str):
        """Set a voice clone audio file for Coqui TTS"""
        if os.path.exists(audio_prompt_path):
            self.voice_clone_path = audio_prompt_path
            logger.info(f"Voice clone set to: {audio_prompt_path}")
        else:
            logger.error(f"Voice clone file not found: {audio_prompt_path}")
    
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
    
    def test_speech(self, text: str = "Hello! I'm your Totoro assistant with Coqui neural voice synthesis."):
        """Test speech output"""
        logger.info("Testing speech output...")
        
        if self.coqui_tts:
            logger.info("🎤 Testing Coqui TTS...")
            success = self._speak_coqui(text)
            if success:
                logger.info("✅ Coqui TTS working!")
                return True
            else:
                logger.warning("❌ Coqui TTS failed")
        
        logger.info("🔄 Testing fallback TTS...")
        success = self._speak_pyttsx3(text)
        if success:
            logger.info("✅ Fallback TTS working!")
            return True
        else:
            logger.error("❌ All TTS methods failed!")
            return False 