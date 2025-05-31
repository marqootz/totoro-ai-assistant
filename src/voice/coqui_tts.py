import os
import tempfile
import pygame
import logging
import threading
import time
from typing import Optional

logger = logging.getLogger(__name__)

class CoquiTTS:
    """Coqui TTS (XTTS v2) - Fast neural voice synthesis with voice cloning"""
    
    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        self.model_name = model_name
        self.tts = None
        self.george_voice_path = None
        self._lock = threading.Lock()
        self._audio_initialized = False
        
        self._init_audio()
        self._init_coqui_tts()
        
    def _init_audio(self):
        """Initialize audio system"""
        if self._audio_initialized:
            return
            
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            self._audio_initialized = True
            logger.info("✅ Audio initialized for Coqui TTS")
        except Exception as e:
            logger.warning(f"Audio initialization failed: {e}")
    
    def _init_coqui_tts(self):
        """Initialize Coqui TTS (XTTS v2) model"""
        try:
            from TTS.api import TTS
            
            logger.info("🚀 Loading Coqui XTTS v2 model...")
            self.tts = TTS(self.model_name)
            
            # Check if CUDA is available
            try:
                import torch
                if torch.cuda.is_available():
                    self.tts = self.tts.to("cuda")
                    logger.info("🎮 Coqui TTS loaded on GPU")
                else:
                    logger.info("💻 Coqui TTS loaded on CPU")
            except:
                logger.info("💻 Coqui TTS loaded on CPU")
            
            logger.info("✅ Coqui TTS initialized successfully!")
            
        except ImportError as e:
            logger.error(f"Coqui TTS not available: {e}")
            logger.info("Install with: pip install TTS")
            self.tts = None
        except Exception as e:
            logger.error(f"Coqui TTS initialization failed: {e}")
            self.tts = None
    
    def set_george_voice(self, voice_path: str):
        """Set George's voice for cloning"""
        if os.path.exists(voice_path):
            self.george_voice_path = voice_path
            logger.info(f"🎭 George voice set: {voice_path}")
        else:
            logger.error(f"Voice file not found: {voice_path}")
    
    def speak(self, text: str, speaker_wav: Optional[str] = None, speed: float = 1.0) -> bool:
        """Generate and play speech with Coqui TTS"""
        if not self.tts:
            logger.error("Coqui TTS not available")
            return False
        
        if not text.strip():
            return False
        
        with self._lock:
            try:
                # Use George's voice if set and no specific speaker provided
                if not speaker_wav and self.george_voice_path:
                    speaker_wav = self.george_voice_path
                
                # Coqui XTTS requires a speaker voice for cloning
                if not speaker_wav:
                    logger.error("Coqui XTTS requires a speaker voice file")
                    return False
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                logger.info(f"🗣️ Coqui TTS generating: {text[:50]}...")
                
                # Generate speech with Coqui TTS
                self.tts.tts_to_file(
                    text=text,
                    speaker_wav=speaker_wav,
                    language="en",
                    file_path=temp_path,
                    speed=speed
                )
                
                logger.debug(f"Voice cloning from: {speaker_wav}")
                
                # Stop any previous audio
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
                logger.info("✅ Coqui TTS speech completed")
                return True
                
            except Exception as e:
                logger.error(f"Coqui TTS generation failed: {e}")
                try:
                    if 'temp_path' in locals():
                        os.unlink(temp_path)
                except:
                    pass
                return False
    
    def test_speed(self, test_text: str = "Hello! This is a speed test of Coqui TTS with voice cloning."):
        """Test Coqui TTS speed"""
        if not self.george_voice_path:
            logger.error("❌ George's voice not set")
            return False
        
        logger.info(f"🎤 Testing Coqui TTS speed...")
        start_time = time.time()
        
        success = self.speak(test_text)
        
        end_time = time.time()
        
        if success:
            duration = end_time - start_time
            logger.info(f"✅ Coqui TTS completed in {duration:.1f} seconds")
            
            if duration < 5:
                logger.info("🚀 Excellent speed!")
            elif duration < 10:
                logger.info("⚡ Good speed!")
            else:
                logger.info("🤔 Slower than expected - check your setup")
            return True
        else:
            logger.error("❌ Coqui TTS test failed")
            return False
    
    def list_available_models(self):
        """List available Coqui TTS models"""
        try:
            from TTS.api import TTS
            models = TTS.list_models()
            logger.info("Available Coqui TTS models:")
            for model in models:
                if "xtts" in model.lower():
                    logger.info(f"  🎯 {model}")
                else:
                    logger.info(f"    {model}")
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return [] 