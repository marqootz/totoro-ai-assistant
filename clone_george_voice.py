#!/usr/bin/env python3
"""
Voice Cloning Script for George's Voice
Clone the voice from george-source-voice.mp3 using Chatterbox TTS
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

def clone_george_voice():
    """Clone George's voice using the provided audio sample"""
    
    print("🎭 GEORGE VOICE CLONING")
    print("=" * 50)
    
    # Check if source audio file exists
    source_audio = "assets/george-source-voice.mp3"
    if not os.path.exists(source_audio):
        print(f"❌ Source audio file not found: {source_audio}")
        print("Please make sure the file exists in the assets directory.")
        return False
    
    print(f"✅ Found source audio: {source_audio}")
    
    # Initialize TTS with chatterbox
    print("🚀 Initializing Chatterbox TTS...")
    tts = TextToSpeech(voice_preference="chatterbox")
    
    if not tts.chatterbox_model:
        print("❌ Chatterbox TTS not available. Please install it:")
        print("   pip install chatterbox-tts torchaudio")
        return False
    
    print("✅ Chatterbox TTS initialized successfully!")
    
    # Test phrases to clone
    test_phrases = [
        "Hello, this is George speaking with my cloned voice.",
        "I am your Totoro assistant, now speaking in George's voice.",
        "The voice cloning technology is working perfectly!",
        "How do you like my new cloned voice? Pretty impressive, right?",
        "I can now speak in any voice you want me to use."
    ]
    
    print(f"\n🎤 Cloning voice using {source_audio}...")
    print("Testing with multiple phrases:\n")
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"🗣️ Test {i}: '{phrase[:50]}{'...' if len(phrase) > 50 else ''}'")
        
        # Use voice cloning with the source audio
        success = tts.speak(phrase, audio_prompt_path=source_audio)
        
        if success:
            print(f"✅ Test {i} completed successfully!")
        else:
            print(f"❌ Test {i} failed!")
        
        print()  # Empty line for spacing
    
    print("🎉 Voice cloning demonstration complete!")
    print("\n💡 To use George's voice in your Totoro assistant:")
    print(f"   tts.speak('Your text here', audio_prompt_path='{source_audio}')")
    
    return True

def set_george_as_default_voice():
    """Set George's voice as the default for the assistant"""
    
    print("\n🔧 SETTING GEORGE AS DEFAULT VOICE")
    print("=" * 50)
    
    source_audio = "assets/george-source-voice.mp3"
    
    # Update config to use George's voice by default
    config_content = f'''import os
import sys

# Voice Recognition Settings
WAKE_WORD = "totoro"
RECOGNITION_TIMEOUT = 30
COMMAND_TIMEOUT = 10

# Voice Output Settings - Using George's cloned voice
voice_pref = os.getenv('VOICE_PREFERENCE', 'chatterbox')
VOICE_PREFERENCE = voice_pref
TTS_RATE = 180
TTS_VOLUME = 0.8

# Chatterbox TTS Settings
CHATTERBOX_EXAGGERATION = 0.5  # Control emotion intensity (0.0-1.0)
CHATTERBOX_CFG_WEIGHT = 0.5   # Control generation stability (0.0-1.0)

# George's Voice Clone Settings
GEORGE_VOICE_PATH = "{source_audio}"
USE_GEORGE_VOICE = True  # Set to False to disable George's voice

# System Voice Settings (fallback when VOICE_PREFERENCE = "system")
SYSTEM_VOICE_ID = "com.apple.eloquence.en-GB.Grandma"
SYSTEM_VOICE_NAME = "Grandma (English (UK))"
'''
    
    # Write updated config
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Updated config.py with George's voice settings")
    print("✅ George's voice is now set as default for voice cloning")
    
    # Create a wrapper script for easy George voice usage
    wrapper_content = '''#!/usr/bin/env python3
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
'''
    
    with open('speak_as_george.py', 'w') as f:
        f.write(wrapper_content)
    
    print("✅ Created speak_as_george.py wrapper script")
    print("\n💡 Usage examples:")
    print("   python speak_as_george.py 'Hello world!'")
    print("   python speak_as_george.py 'Any text you want George to say'")

def main():
    """Main function"""
    print("🎭 TOTORO ASSISTANT - GEORGE VOICE CLONING")
    print("=" * 60)
    
    # Step 1: Clone and test the voice
    success = clone_george_voice()
    
    if not success:
        print("❌ Voice cloning failed. Please check your setup.")
        return
    
    # Step 2: Offer to set as default
    print("\n" + "=" * 60)
    response = input("Would you like to set George's voice as the default? (y/n): ").lower()
    
    if response in ['y', 'yes']:
        set_george_as_default_voice()
        print("\n🎉 George's voice is now your default Totoro assistant voice!")
    else:
        print("\n💡 You can manually use George's voice anytime by calling:")
        print("   tts.speak('text', audio_prompt_path='assets/george-source-voice.mp3')")
    
    print("\n✨ Voice cloning setup complete!")

if __name__ == "__main__":
    main() 