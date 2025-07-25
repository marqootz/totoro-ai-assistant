#!/usr/bin/env python3
"""
Simple WAV File Creator - Basic usage example
Shows how to create WAV files from text using the voice synthesis system
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

def create_wav_file(text, output_path, voice_sample_path=None):
    """
    Create a WAV file from text using voice synthesis
    
    Args:
        text: Text to convert to speech
        output_path: Path where the WAV file should be saved
        voice_sample_path: Optional path to voice sample for cloning (for Coqui TTS)
    """
    print(f"🎵 Creating WAV file: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    print(f"📁 Output: {output_path}")
    
    # Initialize TTS
    tts = TextToSpeech(voice_preference="coqui")
    
    if tts.coqui_tts:
        # Use Coqui TTS for high-quality voice synthesis
        print("🤖 Using Coqui TTS with voice cloning")
        
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
    else:
        print("❌ Coqui TTS not available")
        return False

def main():
    """Example usage"""
    
    # Example 1: Create a simple WAV file
    text = "Hello! This is a test of the voice synthesis system."
    output_file = "test_output.wav"
    
    success = create_wav_file(text, output_file)
    
    if success:
        print(f"✅ Successfully created: {output_file}")
    else:
        print(f"❌ Failed to create: {output_file}")
    
    # Example 2: Create WAV file with custom voice sample
    print("\n" + "="*50)
    print("Creating WAV file with custom voice sample...")
    
    # Check if K2-SO voice sample exists
    k2so_voice = "assets/k2so-voice-samples.mp3"
    if os.path.exists(k2so_voice):
        text2 = "I am K2-SO, a reprogrammed Imperial droid."
        output_file2 = "k2so_test.wav"
        
        success2 = create_wav_file(text2, output_file2, k2so_voice)
        
        if success2:
            print(f"✅ Successfully created K2-SO voice: {output_file2}")
        else:
            print(f"❌ Failed to create K2-SO voice: {output_file2}")
    else:
        print("⚠️  K2-SO voice sample not found, skipping custom voice example")

if __name__ == "__main__":
    main() 