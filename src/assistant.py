import asyncio
import logging
from typing import Optional, Dict, Any
from .config import Config
from .voice import VoiceRecognizer, TextToSpeech
from .llm.command_processor import CommandProcessor
from .llm.local_llm_processor import LocalLLMProcessor, HuggingFaceLLMProcessor
from .integrations import HomeAssistantClient, SpotifyClient
from .presence import SimplePresenceDetector
from .core import TaskExecutor

logger = logging.getLogger(__name__)

class TotoroAssistant:
    """Main assistant coordinator"""
    
    def __init__(self):
        self.config = Config()
        
        # Initialize components
        self.voice_recognizer = VoiceRecognizer(wake_word=self.config.WAKE_WORD)
        self.tts = TextToSpeech(rate=self.config.VOICE_RATE, volume=self.config.VOICE_VOLUME)
        
        # Initialize LLM processor based on backend
        self.command_processor = self._initialize_llm_processor()
        
        # Initialize integrations
        self.home_assistant = HomeAssistantClient(
            base_url=self.config.HOME_ASSISTANT_URL,
            token=self.config.HOME_ASSISTANT_TOKEN
        )
        
        self.spotify = None
        if self.config.SPOTIFY_CLIENT_ID and self.config.SPOTIFY_CLIENT_SECRET:
            self.spotify = SpotifyClient(
                client_id=self.config.SPOTIFY_CLIENT_ID,
                client_secret=self.config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=self.config.SPOTIFY_REDIRECT_URI
            )
        
        # Initialize presence detection
        self.presence_detector = SimplePresenceDetector(
            default_room=self.config.DEFAULT_ROOM
        )
        
        # Initialize task executor
        self.task_executor = TaskExecutor()
        
        # Set integrations in task executor
        self.task_executor.set_integrations(
            home_assistant=self.home_assistant,
            spotify=self.spotify,
            presence_detector=self.presence_detector,
            tts=self.tts
        )
        
        logger.info(f"Totoro Assistant initialized with {self.config.LLM_BACKEND} LLM backend")
    
    def _initialize_llm_processor(self):
        """Initialize the appropriate LLM processor based on configuration"""
        llm_config = self.config.get_llm_config()
        
        if self.config.LLM_BACKEND == "openai":
            return CommandProcessor(
                api_key=llm_config["api_key"],
                model=llm_config["model"]
            )
        elif self.config.LLM_BACKEND == "local":
            return LocalLLMProcessor(
                model_name=llm_config["model_name"],
                base_url=llm_config["base_url"]
            )
        elif self.config.LLM_BACKEND == "huggingface":
            return HuggingFaceLLMProcessor(
                model_name=llm_config["model_name"]
            )
        else:
            raise ValueError(f"Unsupported LLM backend: {self.config.LLM_BACKEND}")
    
    async def process_text_command(self, command: str) -> str:
        """Process a text command and return response"""
        try:
            logger.info(f"Processing command: {command}")
            
            # Get current room
            current_room = self.presence_detector.get_current_room()
            
            # Process command with LLM
            result = self.command_processor.process_command(command, current_room)
            
            if result.success and result.tasks:
                # Execute tasks
                execution_result = await self.task_executor.execute_tasks(result.tasks)
                
                if execution_result:
                    return result.response
                else:
                    return "I encountered an issue while executing that command."
            else:
                return result.response
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return "Sorry, I encountered an error processing your command."
    
    async def start_voice_mode(self):
        """Start voice interaction mode"""
        logger.info("Starting voice mode...")
        self.tts.speak(f"Hello! {self.config.ASSISTANT_NAME} is ready to help.")
        
        try:
            while True:
                # Listen for wake word
                logger.info(f"Listening for wake word: {self.config.WAKE_WORD}")
                if self.voice_recognizer.listen_for_wake_word():
                    logger.info("Wake word detected!")
                    
                    # Get command
                    command = self.voice_recognizer.listen_for_command()
                    if command:
                        logger.info(f"Command received: {command}")
                        
                        # Process command
                        response = await self.process_text_command(command)
                        
                        # Speak response
                        self.tts.speak(response)
                    else:
                        self.tts.speak("I didn't catch that. Could you try again?")
                
                # Small delay to prevent excessive CPU usage
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Voice mode stopped by user")
            self.tts.speak("Goodbye!")
        except Exception as e:
            logger.error(f"Error in voice mode: {e}")
            self.tts.speak("I'm experiencing technical difficulties. Goodbye!")
    
    async def test_integrations(self) -> Dict[str, bool]:
        """Test all integrations and return status"""
        results = {}
        
        # Test LLM
        try:
            test_result = self.command_processor.process_command("test command")
            results["llm"] = test_result is not None
        except Exception as e:
            logger.error(f"LLM test failed: {e}")
            results["llm"] = False
        
        # Test Home Assistant
        try:
            entities = await self.home_assistant.get_entities()
            results["home_assistant"] = len(entities) > 0
        except Exception as e:
            logger.error(f"Home Assistant test failed: {e}")
            results["home_assistant"] = False
        
        # Test Spotify
        if self.spotify:
            try:
                devices = self.spotify.get_devices()
                results["spotify"] = devices is not None
            except Exception as e:
                logger.error(f"Spotify test failed: {e}")
                results["spotify"] = False
        else:
            results["spotify"] = None  # Not configured
        
        # Test TTS
        try:
            voices = self.tts.get_voices()
            results["tts"] = len(voices) > 0
        except Exception as e:
            logger.error(f"TTS test failed: {e}")
            results["tts"] = False
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get current assistant status"""
        return {
            "llm_backend": self.config.LLM_BACKEND,
            "current_room": self.presence_detector.get_current_room(),
            "wake_word": self.config.WAKE_WORD,
            "integrations": {
                "home_assistant": self.home_assistant is not None,
                "spotify": self.spotify is not None,
            }
        } 