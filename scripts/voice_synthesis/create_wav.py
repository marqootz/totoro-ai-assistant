#!/usr/bin/env python3
"""
Command-line WAV File Creator
Usage: python create_wav.py "Your text here" output.wav [voice_sample.mp3]
"""

import os
import sys
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def create_wav_file(text, output_path, voice_sample_path=None):
    """Create a WAV file from text using voice synthesis"""
    print(f"🎵 Creating WAV file...")
    print(f"📝 Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    print(f"📁 Output: {output_path}")
    
    # Initialize TTS
    tts = TextToSpeech(voice_preference="coqui")
    
    if not tts.coqui_tts:
        print("❌ Coqui TTS not available")
        return False
    
    # Use provided voice sample or default
    if not voice_sample_path:
        # Try to use K2-SO voice if available
        k2so_path = "assets/k2so-voice-samples.mp3"
        if os.path.exists(k2so_path):
            voice_sample_path = k2so_path
            print("🤖 Using K2-SO voice for cloning")
        else:
            print("❌ No voice sample provided and K2-SO voice not found")
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
    parser = argparse.ArgumentParser(description="Create WAV files from text using voice synthesis")
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("output", help="Output WAV file path")
    parser.add_argument("--voice", "-v", help="Voice sample file for cloning (optional)")
    parser.add_argument("--speed", "-s", type=float, default=1.0, help="Speech speed (0.5-2.0, default: 1.0)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.text.strip():
        print("❌ No text provided")
        sys.exit(1)
    
    if not args.output.endswith('.wav'):
        print("⚠️  Warning: Output file should have .wav extension")
    
    # Create the WAV file
    success = create_wav_file(args.text, args.output, args.voice)
    
    if success:
        print(f"🎉 Successfully created: {args.output}")
        sys.exit(0)
    else:
        print(f"💥 Failed to create: {args.output}")
        sys.exit(1)

if __name__ == "__main__":
    main() 