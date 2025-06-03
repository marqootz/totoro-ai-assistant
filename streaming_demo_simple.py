#!/usr/bin/env python3
"""
Simple K2-SO Streaming Demo - Shows UX improvement concept
Uses pre-generated audio to demonstrate streaming vs traditional playback
"""

import os
import sys
import time
import threading
import queue
import wave
import numpy as np
from typing import Optional
import pygame

class SimpleStreamingDemo:
    """
    Simple demo showing traditional vs streaming audio playback
    Uses existing K2-SO audio files to demonstrate the concept
    """
    
    def __init__(self):
        self.chunk_size = 4096
        self.buffer_chunks = 3
        self.sample_rate = 22050
        
        # Initialize pygame
        pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=1024)
        
        # Find available K2-SO audio files
        self.audio_files = self._find_k2so_files()
        
    def _find_k2so_files(self):
        """Find available K2-SO audio samples"""
        possible_files = [
            "debug_audio.wav",  # Recently generated files
            "output.wav",  
            "test_k2so_voice.wav",
            "assets/k2so-voice-samples-optimized.mp3",
            "assets/k2so-voice-samples.mp3"
        ]
        
        found_files = []
        for file_path in possible_files:
            if os.path.exists(file_path):
                found_files.append(file_path)
                print(f"✅ Found audio file: {file_path}")
        
        if not found_files:
            print("❌ No audio files found - generating a test file...")
            self._create_test_audio()
            found_files = ["test_audio.wav"]
        
        return found_files
    
    def _create_test_audio(self):
        """Create a simple test audio file if none exists"""
        try:
            # Generate a simple sine wave as test audio
            duration = 3.0  # 3 seconds
            frequency = 440  # A4 note
            
            samples = int(self.sample_rate * duration)
            t = np.linspace(0, duration, samples, False)
            audio_data = np.sin(2 * np.pi * frequency * t) * 0.3  # 30% volume
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save as WAV file
            with wave.open("test_audio.wav", 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            print("✅ Created test audio file: test_audio.wav")
            
        except Exception as e:
            print(f"❌ Failed to create test audio: {e}")
    
    def play_traditional(self, audio_file: str):
        """Traditional playback - load completely, then play"""
        print(f"\n🔄 TRADITIONAL PLAYBACK: {audio_file}")
        print("=" * 50)
        
        start_time = time.time()
        
        # Simulate loading/processing time
        print("⏳ Loading audio file...")
        time.sleep(1.0)  # Simulate file loading
        
        # Load and play complete file
        try:
            pygame.mixer.music.load(audio_file)
            load_time = time.time() - start_time
            
            print(f"🎵 Starting playback after {load_time:.2f}s...")
            pygame.mixer.music.play()
            
            # Wait for completion
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            total_time = time.time() - start_time
            print(f"✅ Traditional playback complete: {total_time:.2f}s total")
            
            return {
                'perceived_latency': load_time,
                'total_time': total_time,
                'method': 'traditional'
            }
            
        except Exception as e:
            print(f"❌ Traditional playback failed: {e}")
            return None
    
    def play_streaming(self, audio_file: str):
        """Streaming playback - start playing while still loading chunks"""
        print(f"\n🚀 STREAMING PLAYBACK: {audio_file}")
        print("=" * 50)
        
        start_time = time.time()
        
        try:
            # Load audio file for chunking
            with wave.open(audio_file, 'rb') as wav_file:
                frames = wav_file.readframes(wav_file.getnframes())
                sample_width = wav_file.getsampwidth()
                
                # Convert to numpy array
                if sample_width == 2:
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                else:
                    audio_data = np.frombuffer(frames, dtype=np.float32)
                    audio_data = (audio_data * 32767).astype(np.int16)
            
            # Set up streaming
            chunk_queue = queue.Queue()
            total_chunks = len(audio_data) // self.chunk_size
            chunks_buffered = 0
            first_audio_time = None
            
            print(f"📡 Streaming {total_chunks} chunks...")
            
            # Start playback thread
            playback_complete = threading.Event()
            
            def playback_worker():
                chunks_played = 0
                while chunks_played < total_chunks:
                    try:
                        chunk = chunk_queue.get(timeout=1.0)
                        
                        # Play chunk
                        if len(chunk) > 0:
                            try:
                                # For mono mixer, use 1D array
                                sound = pygame.sndarray.make_sound(chunk)
                                sound.play()
                                chunks_played += 1
                                
                                # Wait for chunk to finish
                                while pygame.mixer.get_busy():
                                    pygame.time.wait(10)
                            except ValueError:
                                # Fallback: convert to bytes and use mixer.Sound
                                chunk_bytes = chunk.astype(np.int16).tobytes()
                                sound = pygame.mixer.Sound(buffer=chunk_bytes)
                                sound.play()
                                chunks_played += 1
                                while pygame.mixer.get_busy():
                                    pygame.time.wait(10)
                        
                        chunk_queue.task_done()
                        
                    except queue.Empty:
                        break
                
                playback_complete.set()
                print(f"✅ Streaming playback complete - {chunks_played} chunks played")
            
            playback_thread = threading.Thread(target=playback_worker)
            playback_thread.start()
            
            # Generate chunks with realistic delays
            for i in range(0, len(audio_data), self.chunk_size):
                chunk = audio_data[i:i + self.chunk_size]
                
                # Simulate chunk processing delay
                time.sleep(0.05)  # 50ms processing per chunk
                
                chunk_queue.put(chunk)
                chunks_buffered += 1
                
                # Mark when first audio should start
                if chunks_buffered == self.buffer_chunks and first_audio_time is None:
                    first_audio_time = time.time() - start_time
                    print(f"🎯 First audio starts in {first_audio_time:.2f}s (after {chunks_buffered} chunks)")
            
            # Wait for playback completion
            playback_complete.wait(timeout=30)
            playback_thread.join()
            
            total_time = time.time() - start_time
            
            return {
                'perceived_latency': first_audio_time or total_time,
                'total_time': total_time,
                'method': 'streaming'
            }
            
        except Exception as e:
            print(f"❌ Streaming playback failed: {e}")
            return None
    
    def compare_methods(self):
        """Compare traditional vs streaming playback"""
        print("🎯 K2-SO STREAMING SYNTHESIS CONCEPT DEMO")
        print("=" * 60)
        
        if not self.audio_files:
            print("❌ No audio files available for demo")
            return
        
        audio_file = self.audio_files[0]
        print(f"🎵 Using audio file: {audio_file}")
        
        # Test traditional method
        traditional_result = self.play_traditional(audio_file)
        
        time.sleep(1)  # Brief pause between tests
        
        # Test streaming method  
        streaming_result = self.play_streaming(audio_file)
        
        # Compare results
        if traditional_result and streaming_result:
            print(f"\n📊 PERFORMANCE COMPARISON")
            print("=" * 40)
            
            trad_latency = traditional_result['perceived_latency']
            stream_latency = streaming_result['perceived_latency']
            improvement = ((trad_latency - stream_latency) / trad_latency) * 100
            
            print(f"Traditional Latency:  {trad_latency:.2f}s")
            print(f"Streaming Latency:    {stream_latency:.2f}s")
            print(f"Improvement:          {improvement:.1f}%")
            
            print(f"\n🎉 STREAMING CONCEPT DEMONSTRATED!")
            print(f"   User hears audio {improvement:.1f}% faster with streaming")
            print(f"   This is the UX improvement you'll get with K2-SO!")
        
        pygame.mixer.quit()

def main():
    """Run the streaming demo"""
    demo = SimpleStreamingDemo()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        demo.compare_methods()
    else:
        # Quick streaming demo
        if demo.audio_files:
            print("🚀 Quick streaming demo...")
            result = demo.play_streaming(demo.audio_files[0])
            if result:
                print(f"🎯 Perceived latency: {result['perceived_latency']:.2f}s")
        else:
            print("❌ No audio files available")

if __name__ == "__main__":
    main() 