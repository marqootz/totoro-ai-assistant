import os
import sys

# Voice Recognition Settings
WAKE_WORD = "totoro"
RECOGNITION_TIMEOUT = 30
COMMAND_TIMEOUT = 10

# Voice Output Settings - Using system voice by default
voice_pref = os.getenv('VOICE_PREFERENCE', 'coqui')
VOICE_PREFERENCE = voice_pref
TTS_RATE = 180
TTS_VOLUME = 0.8

# Coqui TTS Settings
COQUI_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
COQUI_SPEED = 1.0  # Speech speed multiplier (0.5-2.0)

# George's Voice Clone Settings
GEORGE_VOICE_PATH = os.path.join(os.path.dirname(__file__), "assets", "george-source-voice.mp3")
USE_GEORGE_VOICE = True  # Set to True to enable George's voice

# System Voice Settings (fallback when VOICE_PREFERENCE = "system")
SYSTEM_VOICE_NAME = "Samantha"
SYSTEM_VOICE_ID = None  # Will be set automatically if available

# Default voice file for Coqui TTS
DEFAULT_VOICE_PATH = os.path.join(os.path.dirname(__file__), "assets", "default_voice.wav")
