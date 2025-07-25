#!/usr/bin/env python3
"""
George Voice Wrapper - Easy way to speak with George's voice
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech
import config

def speak_as_george(text):
    """Speak text using George's cloned voice"""
    tts = TextToSpeech(voice_preference="chatterbox")
    
    if hasattr(config, 'GEORGE_VOICE_PATH') and config.USE_GEORGE_VOICE:
        return tts.speak(text, audio_prompt_path=config.GEORGE_VOICE_PATH)
    else:
        return tts.speak(text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        speak_as_george(text)
    else:
        speak_as_george("Hello, I'm speaking with George's cloned voice!")
