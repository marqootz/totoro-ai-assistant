#!/usr/bin/env python3
"""
Woman's Voice WAV Creator
Creates WAV files using a woman's voice in her mid-30s
"""

import os
import sys
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def create_woman_voice_wav(text, output_path, voice_sample_path):
    """
    Create a WAV file using a woman's voice sample
    
    Args:
        text: Text to convert to speech
        output_path: Path where the WAV file should be saved
        voice_sample_path: Path to the woman's voice sample file
    """
    print(f"🎵 Creating WAV file with woman's voice...")
    print(f"📝 Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    print(f"📁 Output: {output_path}")
    print(f"🎤 Voice Sample: {voice_sample_path}")
    
    # Initialize TTS
    tts = TextToSpeech(voice_preference="coqui")
    
    if not tts.coqui_tts:
        print("❌ Coqui TTS not available")
        return False
    
    # Check if voice sample exists
    if not os.path.exists(voice_sample_path):
        print(f"❌ Voice sample not found: {voice_sample_path}")
        return False
    
    try:
        # Generate audio with voice cloning
        tts.coqui_tts.tts_to_file(
            text=text,
            speaker_wav=voice_sample_path,
            language="en",
            file_path=output_path,
            speed=1.0
        )
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ WAV file created successfully! ({file_size:,} bytes)")
            return True
        else:
            print("❌ Failed to create WAV file")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create WAV files using a woman's voice")
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("output", help="Output WAV file path")
    parser.add_argument("voice_sample", help="Path to woman's voice sample file")
    parser.add_argument("--speed", "-s", type=float, default=1.0, help="Speech speed (0.5-2.0, default: 1.0)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.text.strip():
        print("❌ No text provided")
        sys.exit(1)
    
    if not args.output.endswith('.wav'):
        print("⚠️  Warning: Output file should have .wav extension")
    
    # Create the WAV file
    success = create_woman_voice_wav(args.text, args.output, args.voice_sample)
    
    if success:
        print(f"🎉 Successfully created: {args.output}")
        sys.exit(0)
    else:
        print(f"💥 Failed to create: {args.output}")
        sys.exit(1)

if __name__ == "__main__":
    main() 