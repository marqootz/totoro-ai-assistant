import os
from typing import List, Optional
from dotenv import load_dotenv
import json

load_dotenv()

class Config:
    """Configuration class for Totoro Personal Assistant"""
    
    # LLM Configuration
    LLM_BACKEND: str = os.getenv("LLM_BACKEND", "unified")  # openai, local, unified, huggingface
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Local LLM Configuration (Ollama, etc.)
    LOCAL_LLM_URL: str = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
    LOCAL_LLM_MODEL: str = os.getenv("LOCAL_LLM_MODEL", "llama3.1:8b")
    
    # Hugging Face Configuration
    HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-medium")
    
    # Home Assistant Configuration
    HOME_ASSISTANT_URL: str = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")
    HOME_ASSISTANT_TOKEN: str = os.getenv("HOME_ASSISTANT_TOKEN", "")
    
    # Spotify Configuration
    SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    
    # Voice Configuration
    WAKE_WORD: str = os.getenv("WAKE_WORD", "totoro")
    VOICE_RATE: int = int(os.getenv("VOICE_RATE", "200"))
    VOICE_VOLUME: float = float(os.getenv("VOICE_VOLUME", "0.9"))
    
    # Room Presence Configuration
    PRESENCE_DETECTION_METHOD: str = os.getenv("PRESENCE_DETECTION_METHOD", "bluetooth")
    BLUETOOTH_DEVICES: List[str] = json.loads(os.getenv("BLUETOOTH_DEVICES", "[]"))
    
    # Assistant Configuration
    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "Totoro")
    DEFAULT_ROOM: str = os.getenv("DEFAULT_ROOM", "living_room")
    COMMAND_TIMEOUT: int = int(os.getenv("COMMAND_TIMEOUT", "30"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if cls.LLM_BACKEND == "openai":
            required_fields = [cls.OPENAI_API_KEY, cls.HOME_ASSISTANT_TOKEN]
        elif cls.LLM_BACKEND in ["local", "unified"]:
            required_fields = [cls.HOME_ASSISTANT_TOKEN]  # Only HA token required for local LLM
        elif cls.LLM_BACKEND == "huggingface":
            required_fields = [cls.HOME_ASSISTANT_TOKEN]  # Only HA token required for HF
        else:
            required_fields = [cls.HOME_ASSISTANT_TOKEN]
        
        return all(field for field in required_fields)
    
    @classmethod
    def get_missing_config(cls) -> List[str]:
        """Get list of missing required configuration"""
        missing = []
        
        if cls.LLM_BACKEND == "openai" and not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        
        if not cls.HOME_ASSISTANT_TOKEN:
            missing.append("HOME_ASSISTANT_TOKEN")
            
        return missing
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM-specific configuration"""
        if cls.LLM_BACKEND == "openai":
            return {
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL
            }
        elif cls.LLM_BACKEND in ["local", "unified"]:
            return {
                "base_url": cls.LOCAL_LLM_URL,
                "model_name": cls.LOCAL_LLM_MODEL
            }
        elif cls.LLM_BACKEND == "huggingface":
            return {
                "model_name": cls.HUGGINGFACE_MODEL
            }
        else:
            raise ValueError(f"Unknown LLM backend: {cls.LLM_BACKEND}") 