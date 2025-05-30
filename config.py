import os
import sys

# Voice Recognition Settings
WAKE_WORD = "totoro"
RECOGNITION_TIMEOUT = 30
COMMAND_TIMEOUT = 10

# Voice Output Settings - Default to Chatterbox TTS for superior quality
# Use 'chatterbox' for state-of-the-art neural TTS, 'system' for fallback
voice_pref = os.getenv('VOICE_PREFERENCE', 'chatterbox')  # Reverted to chatterbox default

# No Python version restrictions for Chatterbox (unlike old Coqui TTS)
VOICE_PREFERENCE = voice_pref
TTS_RATE = 180
TTS_VOLUME = 0.8

# Chatterbox TTS Settings
CHATTERBOX_EXAGGERATION = 0.5  # Control emotion intensity (0.0-1.0)
CHATTERBOX_CFG_WEIGHT = 0.5   # Control generation stability (0.0-1.0)

# System Voice Settings (fallback when VOICE_PREFERENCE = "system")
# British woman in her 60's - using Grandma (English UK) voice
SYSTEM_VOICE_ID = "com.apple.eloquence.en-GB.Grandma"
SYSTEM_VOICE_NAME = "Grandma (English (UK))"

# Alternative British voices (uncomment to use):
# SYSTEM_VOICE_ID = "com.apple.voice.compact.en-IE.Moira"  # Irish accent
# SYSTEM_VOICE_ID = "com.apple.eloquence.en-GB.Flo"        # British female
# SYSTEM_VOICE_ID = "com.apple.eloquence.en-GB.Sandy"      # British female 