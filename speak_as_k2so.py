#!/usr/bin/env python3
"""
K2-SO Voice Wrapper - Easy way to speak with K2-SO's voice
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def speak_as_k2so(text, use_clean=False):
    """Speak text using K2-SO's cloned voice"""
    tts = TextToSpeech(voice_preference="coqui")
    
    # Choose between original and cleaned K2-SO voice samples
    if use_clean and os.path.exists("assets/k2so-voice-samples-clean.mp3"):
        k2so_voice_path = "assets/k2so-voice-samples-clean.mp3"
        print("🧹 Using cleaned K2-SO voice sample")
    else:
        k2so_voice_path = "assets/k2so-voice-samples.mp3"
        print("🤖 Using original K2-SO voice sample")
    
    if os.path.exists(k2so_voice_path):
        return tts.speak(text, audio_prompt_path=k2so_voice_path)
    else:
        print(f"❌ K2-SO voice file not found: {k2so_voice_path}")
        return tts.speak(text)

if __name__ == "__main__":
    use_clean = False
    text_args = []
    
    # Parse command line arguments
    for arg in sys.argv[1:]:
        if arg == "--clean":
            use_clean = True
        else:
            text_args.append(arg)
    
    if text_args:
        text = " ".join(text_args)
        speak_as_k2so(text, use_clean=use_clean)
    else:
        speak_as_k2so("I am K2-SO. Imperial security droid. Former Imperial security droid.", use_clean=use_clean) 