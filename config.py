import os
import sys

# Voice Recognition Settings
WAKE_WORD = "totoro"
RECOGNITION_TIMEOUT = 30
COMMAND_TIMEOUT = 10

# Voice Output Settings - Default to system TTS for better compatibility
# Use 'neural' only if explicitly requested and Python 3.10+
voice_pref = os.getenv('VOICE_PREFERENCE', 'system')
if voice_pref == 'neural' and sys.version_info < (3, 10):
    print("Note: Neural TTS requires Python 3.10+. Using system TTS.")
    voice_pref = 'system'

VOICE_PREFERENCE = voice_pref
TTS_RATE = 180
TTS_VOLUME = 0.8 