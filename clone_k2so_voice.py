#!/usr/bin/env python3
"""
Voice Cloning Script for K2-SO's Voice
Clone the voice from k2so-voice-samples.mp3 using Coqui TTS
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import TTS
from src.voice.text_to_speech import TextToSpeech
import config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def clone_k2so_voice():
    """Clone K2-SO's voice using the provided audio samples"""
    
    print("🤖 K2-SO VOICE CLONING")
    print("=" * 50)
    
    # Check if source audio file exists
    source_audio = "assets/k2so-voice-samples.mp3"
    if not os.path.exists(source_audio):
        print(f"❌ Source audio file not found: {source_audio}")
        print("Please make sure the file exists in the assets directory.")
        return False
    
    print(f"✅ Found source audio: {source_audio}")
    
    # Initialize TTS with coqui
    print("🚀 Initializing Coqui TTS...")
    tts = TextToSpeech(voice_preference="coqui")
    
    if not tts.coqui_tts:
        print("❌ Coqui TTS not available. Please install it:")
        print("   pip install TTS torch torchaudio")
        return False
    
    print("✅ Coqui TTS initialized successfully!")
    
    # K2-SO specific test phrases in character
    test_phrases = [
        "I am K2-SO. Imperial security droid. Former Imperial security droid.",
        "The odds of success are approximately three thousand seven hundred and twenty to one.",
        "I have a bad feeling about this.",
        "Congratulations, you are being rescued. Please do not resist.",
        "I find that answer vague and unconvincing.",
        "Your friend is quite a mercenary. I like him.",
        "There are a lot of explosions for a droid rescue.",
        "Did you know that wasn't me?",
        "Climb. Climb!"
    ]
    
    print(f"\n🎤 Cloning voice using {source_audio}...")
    print("Testing with K2-SO characteristic phrases:\n")
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"🤖 Test {i}: '{phrase[:60]}{'...' if len(phrase) > 60 else ''}'")
        
        # Use voice cloning with the source audio
        success = tts.speak(phrase, audio_prompt_path=source_audio)
        
        if success:
            print(f"✅ Test {i} completed successfully!")
        else:
            print(f"❌ Test {i} failed!")
        
        print()  # Empty line for spacing
    
    print("🎉 K2-SO voice cloning demonstration complete!")
    print("\n💡 To use K2-SO's voice in your Totoro assistant:")
    print(f"   tts.speak('Your text here', audio_prompt_path='{source_audio}')")
    
    return True

def set_k2so_as_default_voice():
    """Set K2-SO's voice as the default for the assistant"""
    
    print("\n🔧 SETTING K2-SO AS DEFAULT VOICE")
    print("=" * 50)
    
    source_audio = "assets/k2so-voice-samples.mp3"
    
    # Update config to use K2-SO's voice by default
    config_content = f'''import os
import sys

# Voice Recognition Settings
WAKE_WORD = "totoro"
RECOGNITION_TIMEOUT = 30
COMMAND_TIMEOUT = 10

# Voice Output Settings - Using K2-SO's cloned voice
voice_pref = os.getenv('VOICE_PREFERENCE', 'coqui')
VOICE_PREFERENCE = voice_pref
TTS_RATE = 180
TTS_VOLUME = 0.8

# Coqui TTS Settings
COQUI_EXAGGERATION = 0.5  # Control emotion intensity (0.0-1.0)
COQUI_CFG_WEIGHT = 0.5   # Control generation stability (0.0-1.0)

# K2-SO's Voice Clone Settings
K2SO_VOICE_PATH = "{source_audio}"
USE_K2SO_VOICE = True  # Set to False to disable K2-SO's voice

# Legacy George Voice Settings (for fallback compatibility)
GEORGE_VOICE_PATH = "assets/george-source-voice.mp3"
USE_GEORGE_VOICE = False  # Disabled in favor of K2-SO

# System Voice Settings (fallback when VOICE_PREFERENCE = "system")
SYSTEM_VOICE_ID = "com.apple.eloquence.en-GB.Grandma"
SYSTEM_VOICE_NAME = "Grandma (English (UK))"
'''
    
    # Write updated config
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Updated config.py with K2-SO's voice settings")
    print("✅ K2-SO's voice is now set as default for voice cloning")
    
    # Create a wrapper script for easy K2-SO voice usage
    wrapper_content = '''#!/usr/bin/env python3
"""
K2-SO Voice Wrapper - Easy way to speak with K2-SO's voice
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech
import config

def speak_as_k2so(text):
    """Speak text using K2-SO's cloned voice"""
    tts = TextToSpeech(voice_preference="coqui")
    
    if hasattr(config, 'K2SO_VOICE_PATH') and config.USE_K2SO_VOICE:
        return tts.speak(text, audio_prompt_path=config.K2SO_VOICE_PATH)
    elif hasattr(config, 'GEORGE_VOICE_PATH') and config.USE_GEORGE_VOICE:
        # Fallback to George voice if available
        return tts.speak(text, audio_prompt_path=config.GEORGE_VOICE_PATH)
    else:
        return tts.speak(text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        speak_as_k2so(text)
    else:
        speak_as_k2so("I am K2-SO. Imperial security droid. Former Imperial security droid.")
'''
    
    with open('speak_as_k2so.py', 'w') as f:
        f.write(wrapper_content)
    
    print("✅ Created speak_as_k2so.py wrapper script")
    print("\n💡 Usage examples:")
    print("   python speak_as_k2so.py 'The odds of success are approximately three thousand seven hundred and twenty to one.'")
    print("   python speak_as_k2so.py 'Any text you want K2-SO to say'")

def main():
    """Main function"""
    print("🤖 TOTORO ASSISTANT - K2-SO VOICE CLONING")
    print("=" * 60)
    
    # Step 1: Clone and test the voice
    success = clone_k2so_voice()
    
    if not success:
        print("❌ Voice cloning failed. Please check your setup.")
        return
    
    # Step 2: Offer to set as default
    print("\n" + "=" * 60)
    response = input("Would you like to set K2-SO's voice as the default? (y/n): ").lower()
    
    if response in ['y', 'yes']:
        set_k2so_as_default_voice()
        print("\n🎉 K2-SO's voice is now your default Totoro assistant voice!")
    else:
        print("\n💡 You can manually use K2-SO's voice anytime by calling:")
        print("   tts.speak('text', audio_prompt_path='assets/k2so-voice-samples.mp3')")
    
    print("\n✨ Voice cloning setup complete!")

if __name__ == "__main__":
    main() 