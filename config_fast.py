# config_fast.py - Optimized for Speed
import os

# Voice Settings (OPTIMIZED FOR SPEED)
WAKE_WORD = "totoro"
RECOGNITION_TIMEOUT = 15  # Reduced from 30
COMMAND_TIMEOUT = 8       # Reduced from 10

# Fast TTS Settings
VOICE_PREFERENCE = 'system'  # System TTS is much faster
TTS_RATE = 200              # Faster speech rate
TTS_VOLUME = 0.8

# Fast LLM Settings  
LLM_BACKEND = 'unified'
OLLAMA_MODEL = 'llama3.1:3b'  # Smaller, faster model
OLLAMA_BASE_URL = 'http://localhost:11434'

# System Voice (Fast)
SYSTEM_VOICE_ID = "com.apple.speech.synthesis.voice.Alex"
SYSTEM_VOICE_NAME = "Alex"
