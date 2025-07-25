#!/usr/bin/env python3
"""
Create WAV Files from Text Using Voice Synthesis
Demonstrates how to use the voice synthesis functionality to create audio files
"""

import os
import sys
import tempfile
import time
from typing import Optional

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

class WAVFileCreator:
    """Create WAV files from text using voice synthesis"""
    
    def __init__(self, voice_preference: str = "coqui"):
        self.tts = TextToSpeech(voice_preference=voice_preference)
        self.voice_preference = voice_preference
    
    def create_wav_file(self, text: str, output_path: str, 
                       audio_prompt_path: Optional[str] = None) -> bool:
        """
        Create a WAV file from text using voice synthesis
        
        Args:
            text: Text to convert to speech
            output_path: Path where the WAV file should be saved
            audio_prompt_path: Optional path to audio file for voice cloning (for Coqui TTS)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text.strip():
            print("❌ No text provided")
            return False
        
        print(f"🎵 Creating WAV file: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"📁 Output: {output_path}")
        
        start_time = time.time()
        
        try:
            if self.voice_preference == "coqui" and self.tts.coqui_tts:
                # Use Coqui TTS for high-quality voice synthesis
                success = self._create_wav_coqui(text, output_path, audio_prompt_path)
            else:
                # Use system TTS as fallback
                success = self._create_wav_system(text, output_path)
            
            if success:
                duration = time.time() - start_time
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                print(f"✅ WAV file created successfully!")
                print(f"   ⏱️  Time: {duration:.2f}s")
                print(f"   📊 Size: {file_size:,} bytes")
                return True
            else:
                print("❌ Failed to create WAV file")
                return False
                
        except Exception as e:
            print(f"❌ Error creating WAV file: {e}")
            return False
    
    def _create_wav_coqui(self, text: str, output_path: str, 
                         audio_prompt_path: Optional[str] = None) -> bool:
        """Create WAV file using Coqui TTS with voice cloning"""
        try:
            # Get voice path from config if not provided
            if not audio_prompt_path:
                import config
                if hasattr(config, 'K2SO_VOICE_PATH') and getattr(config, 'USE_K2SO_VOICE', False):
                    audio_prompt_path = config.K2SO_VOICE_PATH
                    print("🤖 Using K2-SO voice for cloning")
                elif hasattr(config, 'GEORGE_VOICE_PATH') and getattr(config, 'USE_GEORGE_VOICE', False):
                    audio_prompt_path = config.GEORGE_VOICE_PATH
                    print("🎭 Using George voice for cloning")
                else:
                    audio_prompt_path = getattr(config, 'DEFAULT_VOICE_PATH', None)
                    print("🎤 Using default voice")
            
            # Coqui XTTS requires a speaker voice for cloning
            if not audio_prompt_path or not os.path.exists(audio_prompt_path):
                print("❌ Coqui XTTS requires a speaker voice file")
                return False
            
            print(f"🎯 Voice cloning from: {audio_prompt_path}")
            
            # Generate audio with voice cloning
            self.tts.coqui_tts.tts_to_file(
                text=text,
                speaker_wav=audio_prompt_path,
                language="en",
                file_path=output_path,
                speed=1.0
            )
            
            return os.path.exists(output_path)
            
        except Exception as e:
            print(f"❌ Coqui TTS error: {e}")
            return False
    
    def _create_wav_system(self, text: str, output_path: str) -> bool:
        """Create WAV file using system TTS"""
        try:
            # Create a temporary script to generate WAV file
            import subprocess
            import tempfile
            
            script_content = f'''
import pyttsx3
import sys

def create_wav(text, output_path):
    try:
        engine = pyttsx3.init()
        
        # Configure voice settings
        voices = engine.getProperty('voices')
        if voices:
            # Use Samantha or first available voice
            for voice in voices:
                if 'samantha' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            else:
                engine.setProperty('voice', voices[0].id)
        
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.8)
        
        # Save to file
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return True
        
    except Exception as e:
        print(f"TTS Error: {{e}}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        text = " ".join(sys.argv[1:-1])
        output_path = sys.argv[-1]
        success = create_wav(text, output_path)
        sys.exit(0 if success else 1)
'''
            
            # Write the script to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                # Run TTS in a separate process
                result = subprocess.run(
                    [sys.executable, script_path, text, output_path],
                    timeout=30,
                    capture_output=True,
                    text=True
                )
                
                return result.returncode == 0
                
            finally:
                # Clean up the temporary script
                try:
                    os.unlink(script_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ System TTS error: {e}")
            return False
    
    def create_multiple_wav_files(self, text_files: dict) -> dict:
        """
        Create multiple WAV files from a dictionary of text
        
        Args:
            text_files: Dictionary with {output_path: text} pairs
            
        Returns:
            dict: Results for each file
        """
        results = {}
        
        for output_path, text in text_files.items():
            print(f"\n📝 Processing: {output_path}")
            success = self.create_wav_file(text, output_path)
            results[output_path] = {
                'success': success,
                'text': text,
                'exists': os.path.exists(output_path) if success else False
            }
        
        return results

def main():
    """Demo function showing how to create WAV files"""
    
    # Initialize the WAV file creator
    creator = WAVFileCreator(voice_preference="coqui")
    
    # Example 1: Create a single WAV file
    print("=" * 60)
    print("EXAMPLE 1: Single WAV File Creation")
    print("=" * 60)
    
    text = "Hello! This is a test of the voice synthesis system. I can create WAV files from any text you provide."
    output_file = "example_output.wav"
    
    success = creator.create_wav_file(text, output_file)
    
    if success:
        print(f"✅ Created: {output_file}")
    else:
        print(f"❌ Failed to create: {output_file}")
    
    # Example 2: Create multiple WAV files
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multiple WAV Files Creation")
    print("=" * 60)
    
    text_files = {
        "greeting.wav": "Hello, welcome to the voice synthesis demo!",
        "weather.wav": "The weather today is sunny with a high of 75 degrees.",
        "joke.wav": "Why don't scientists trust atoms? Because they make up everything!",
        "farewell.wav": "Thank you for using the voice synthesis system. Goodbye!"
    }
    
    results = creator.create_multiple_wav_files(text_files)
    
    # Print results summary
    print("\n📊 Results Summary:")
    print("-" * 40)
    successful = sum(1 for r in results.values() if r['success'])
    total = len(results)
    
    for path, result in results.items():
        status = "✅" if result['success'] else "❌"
        print(f"{status} {path}")
    
    print(f"\n🎯 Success Rate: {successful}/{total} ({successful/total*100:.1f}%)")

if __name__ == "__main__":
    main() 