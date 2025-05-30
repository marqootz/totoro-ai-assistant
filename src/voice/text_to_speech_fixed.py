import pyttsx3
import os
import tempfile
import pygame
import logging
from typing import Optional
import threading
import time
import torchaudio as ta

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Text-to-speech with Chatterbox TTS (Resemble AI) - FIXED to prevent double audio"""
    
    def __init__(self, voice_preference: str = "chatterbox"):
        self.voice_preference = voice_preference
        self.tts_engine = None
        self.chatterbox_model = None
        self._lock = threading.Lock()
        
        # CRITICAL FIX: Only initialize the audio system once
        self._audio_initialized = False
        self._init_audio_system()
        
        # Initialize TTS engines based on preference
        if voice_preference == "chatterbox":
            self._init_chatterbox_tts()
            # Only fallback if Chatterbox completely fails
            if not self.chatterbox_model:
                logger.warning("Chatterbox TTS failed, initializing system TTS fallback")
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
            logger.info("✅ Audio mixer initialized (fixed)")
        except Exception as e:
            logger.warning(f"Failed to initialize audio mixer: {e}")
    
    def _init_chatterbox_tts(self):
        """Initialize Chatterbox TTS for high-quality neural voices"""
        try:
            import torch
            from chatterbox.tts import ChatterboxTTS
            
            # Check for GPU availability and set device appropriately
            if torch.cuda.is_available():
                device = "cuda"
                logger.info(f"🎮 CUDA available - Loading Chatterbox TTS model on GPU...")
            else:
                device = "cpu"
                logger.info(f"💻 Loading Chatterbox TTS model on CPU...")
                # Set default tensor type to FloatTensor to avoid CUDA issues
                torch.set_default_tensor_type(torch.FloatTensor)
            
            # Load the pretrained Chatterbox model with proper device mapping
            try:
                self.chatterbox_model = ChatterboxTTS.from_pretrained(device=device)
            except RuntimeError as e:
                if "CUDA device" in str(e) and device == "cpu":
                    # Force CPU loading with map_location
                    logger.info("🔧 Forcing CPU mapping for CUDA-saved model...")
                    # Monkey patch torch.load to force CPU mapping
                    original_load = torch.load
                    def cpu_load(*args, **kwargs):
                        kwargs['map_location'] = torch.device('cpu')
                        return original_load(*args, **kwargs)
                    torch.load = cpu_load
                    
                    try:
                        self.chatterbox_model = ChatterboxTTS.from_pretrained(device=device)
                    finally:
                        # Restore original torch.load
                        torch.load = original_load
                else:
                    raise e
            
            logger.info("✅ Chatterbox TTS initialized successfully!")
            
        except ImportError as e:
            logger.info(f"Chatterbox TTS library not available: {e}")
            logger.info("Install with: pip install chatterbox-tts")
            self.chatterbox_model = None
        except Exception as e:
            logger.warning(f"Chatterbox TTS initialization failed: {e}")
            logger.info("Will fall back to system TTS")
            self.chatterbox_model = None
    
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
        """Speak text using ONLY ONE TTS engine to prevent double audio
        
        Args:
            text: Text to synthesize
            audio_prompt_path: Optional path to audio file for voice cloning
        """
        if not text.strip():
            return False
        
        with self._lock:
            logger.info(f"🗣️ Speaking with {self.voice_preference} TTS: {text[:50]}...")
            
            # CRITICAL FIX: Use ONLY the preferred engine, no fallback unless it completely fails
            if self.voice_preference == "chatterbox" and self.chatterbox_model:
                success = self._speak_chatterbox(text, audio_prompt_path)
                if success:
                    logger.info("✅ Chatterbox TTS completed successfully")
                    return True
                else:
                    logger.error("❌ Chatterbox TTS failed completely")
                    # Only fallback on complete failure
                    if self.tts_engine:
                        logger.warning("🔄 Falling back to system TTS due to Chatterbox failure")
                        return self._speak_pyttsx3(text)
                    return False
            
            # For system preference or if Chatterbox not available
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
    
    def _speak_chatterbox(self, text: str, audio_prompt_path: Optional[str] = None) -> bool:
        """Speak using Chatterbox TTS"""
        try:
            import sys
            import os
            
            # Add parent directory to path to access root config
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            import config
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generate speech with Chatterbox TTS
            logger.debug(f"Generating Chatterbox speech...")
            
            # Generate audio with optional voice cloning and config parameters
            if audio_prompt_path and os.path.exists(audio_prompt_path):
                wav = self.chatterbox_model.generate(
                    text, 
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=config.CHATTERBOX_EXAGGERATION,
                    cfg_weight=config.CHATTERBOX_CFG_WEIGHT
                )
                logger.debug(f"Using voice clone from: {audio_prompt_path}")
            else:
                wav = self.chatterbox_model.generate(
                    text,
                    exaggeration=config.CHATTERBOX_EXAGGERATION,
                    cfg_weight=config.CHATTERBOX_CFG_WEIGHT
                )
            
            # Save the generated audio
            ta.save(temp_path, wav, self.chatterbox_model.sr)
            
            # CRITICAL FIX: Stop any previous audio before playing new
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                time.sleep(0.1)  # Brief pause
            
            # Play the generated audio
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            os.unlink(temp_path)
            logger.debug("Chatterbox speech completed")
            return True
            
        except Exception as e:
            logger.error(f"Chatterbox TTS error: {e}")
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
            
            # CRITICAL FIX: Stop any pygame audio before using pyttsx3
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
        """Set voice preference: 'chatterbox' or 'system'"""
        self.voice_preference = preference
        logger.info(f"Voice preference set to: {preference}")
    
    def set_voice_clone(self, audio_prompt_path: str):
        """Set a voice clone audio file for Chatterbox TTS"""
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
    
    def test_speech(self, text: str = "Hello! I'm your Totoro assistant with fixed audio - no more double voice!"):
        """Test speech output"""
        logger.info("Testing speech output...")
        
        if self.voice_preference == "chatterbox" and self.chatterbox_model:
            logger.info("🎤 Testing Chatterbox TTS (fixed)...")
            success = self._speak_chatterbox(text)
            if success:
                logger.info("✅ Chatterbox TTS working - no double audio!")
                return True
            else:
                logger.warning("❌ Chatterbox TTS failed")
        
        logger.info("🔄 Testing system TTS...")
        success = self._speak_pyttsx3(text)
        if success:
            logger.info("✅ System TTS working!")
            return True
        else:
            logger.error("❌ All TTS methods failed!")
            return False 