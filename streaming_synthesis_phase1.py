#!/usr/bin/env python3
"""
K2-SO Voice Streaming Synthesis - Phase 1 Implementation
Immediate UX improvements through audio chunking and parallel playback
"""

import os
import sys
import time
import threading
import queue
import wave
import numpy as np
import tempfile
from typing import Generator, Dict, Optional
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.voice.text_to_speech import TextToSpeech

class K2SOStreamingSynthesis:
    """
    Phase 1: Streaming synthesis implementation
    Goal: Reduce perceived latency from 5.2s to 2-3s
    """
    
    def __init__(self, audio_prompt_path: str = "assets/k2so-voice-samples-optimized.mp3"):
        self.tts = None
        self.audio_prompt_path = audio_prompt_path
        
        # Streaming configuration - optimized for K2-SO
        self.chunk_size = 4096        # Audio samples per chunk
        self.buffer_chunks = 3        # Start playing after N chunks ready
        self.sample_rate = 22050      # Optimized sample rate
        self.stream_speed = 0.8       # Stream slightly faster than real-time
        
        # Threading components
        self.chunk_queue = queue.Queue()
        self.is_generating = False
        self.playback_thread = None
        self.generation_complete = False
        
        # Performance tracking
        self.metrics = {
            'first_chunk_time': None,
            'total_chunks': 0,
            'playback_started': False,
            'synthesis_time': 0,
            'total_time': 0
        }
    
    def _initialize_tts(self) -> bool:
        """Initialize TTS system with error handling"""
        if self.tts is None:
            print("🎧 Initializing K2-SO streaming voice system...")
            start_time = time.time()
            
            try:
                self.tts = TextToSpeech(voice_preference="coqui")
                init_time = time.time() - start_time
                
                if self.tts.coqui_tts:
                    print(f"✅ Streaming TTS ready in {init_time:.1f}s")
                    return True
                else:
                    print("❌ Failed to initialize Coqui TTS")
                    return False
                    
            except Exception as e:
                print(f"❌ TTS initialization error: {e}")
                return False
        
        return self.tts.coqui_tts is not None
    
    def _generate_audio_file(self, text: str) -> Optional[str]:
        """Generate complete audio file (Phase 1 approach)"""
        try:
            # Simple direct generation approach
            print("⚙️ Generating audio directly using Coqui TTS...")
            
            # Create temporary file for audio output
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Generate audio directly using Coqui TTS API
            synthesis_start = time.time()
            
            self.tts.coqui_tts.tts_to_file(
                text=text,
                speaker_wav=self.audio_prompt_path,
                language="en",
                file_path=temp_path,
                speed=1.0
            )
            
            self.metrics['synthesis_time'] = time.time() - synthesis_start
            print(f"⚡ Audio generated in {self.metrics['synthesis_time']:.2f}s")
            
            if os.path.exists(temp_path):
                # Check file size to ensure it was created properly
                file_size = os.path.getsize(temp_path)
                print(f"📁 Generated audio file: {file_size} bytes")
                return temp_path
            else:
                print(f"❌ Audio file not created")
                return None
                
        except Exception as e:
            print(f"❌ Audio generation error: {e}")
            return None
    
    def _chunk_audio_generator(self, audio_file_path: str) -> Generator[np.ndarray, None, None]:
        """
        Generator that yields audio chunks from the complete file
        This simulates true streaming for Phase 1
        """
        try:
            # Load the complete audio file
            with wave.open(audio_file_path, 'rb') as wav_file:
                # Get audio parameters
                frames_total = wav_file.getnframes()
                sample_width = wav_file.getsampwidth()
                
                # Read all frames and convert to numpy array
                frames = wav_file.readframes(frames_total)
                
                if sample_width == 2:  # 16-bit
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                else:  # Handle other bit depths
                    audio_data = np.frombuffer(frames, dtype=np.float32)
                    audio_data = (audio_data * 32767).astype(np.int16)
                
                # Calculate chunk timing
                chunk_count = len(audio_data) // self.chunk_size
                chunk_duration = self.chunk_size / self.sample_rate
                stream_delay = chunk_duration * self.stream_speed
                
                self.metrics['total_chunks'] = chunk_count
                print(f"📡 Streaming {chunk_count} chunks ({chunk_duration:.3f}s each)")
                
                # Yield chunks with streaming delay
                for i in range(0, len(audio_data), self.chunk_size):
                    chunk = audio_data[i:i + self.chunk_size]
                    
                    # Track first chunk timing
                    if self.metrics['first_chunk_time'] is None:
                        self.metrics['first_chunk_time'] = time.time()
                    
                    yield chunk
                    
                    # Simulate streaming delay (slightly faster than real-time)
                    if i > 0:  # Don't delay the first chunk
                        time.sleep(stream_delay)
                
                self.generation_complete = True
                
        except Exception as e:
            print(f"❌ Chunking error: {e}")
            self.generation_complete = True
    
    def _audio_playback_worker(self):
        """
        Worker thread that handles audio playback
        Plays chunks as they become available
        """
        try:
            # Initialize pygame mixer for audio playback - ensure mono configuration
            pygame.mixer.pre_init(
                frequency=self.sample_rate,
                size=-16,  # 16-bit signed
                channels=1,  # Mono (important for K2-SO samples)
                buffer=1024
            )
            pygame.mixer.init()
            
            print("🔊 Audio playback worker started...")
            chunks_played = 0
            buffered_chunks = 0
            
            while not self.generation_complete or not self.chunk_queue.empty():
                try:
                    # Get chunk from queue (with timeout)
                    chunk = self.chunk_queue.get(timeout=0.5)
                    buffered_chunks += 1
                    
                    # Start playback after buffer filled
                    if not self.metrics['playback_started'] and buffered_chunks >= self.buffer_chunks:
                        self.metrics['playback_started'] = True
                        playback_start_time = time.time() - self.metrics['first_chunk_time']
                        print(f"🚀 Playback started after buffering {buffered_chunks} chunks ({playback_start_time:.2f}s)")
                    
                    # Convert chunk to pygame sound and play
                    if self.metrics['playback_started']:
                        try:
                            # Ensure chunk is the right shape for mono playback
                            if len(chunk) > 0:
                                # Convert to pygame sound - ensure mono format
                                sound = pygame.sndarray.make_sound(chunk.reshape(-1, 1))
                                sound.play()
                                chunks_played += 1
                                
                                # Wait for this chunk to finish before playing next
                                while pygame.mixer.get_busy():
                                    pygame.time.wait(10)
                                    
                        except Exception as e:
                            print(f"⚠️ Playback error for chunk {chunks_played}: {e}")
                            # Try alternative playback method
                            try:
                                chunk_bytes = chunk.astype(np.int16).tobytes()
                                # Use pygame.mixer.Sound for more control
                                sound_array = np.frombuffer(chunk_bytes, dtype=np.int16)
                                if len(sound_array) > 0:
                                    # Ensure mono playback
                                    sound = pygame.sndarray.make_sound(sound_array.reshape(-1, 1))
                                    sound.play()
                                    chunks_played += 1
                                    while pygame.mixer.get_busy():
                                        pygame.time.wait(10)
                            except Exception as e2:
                                print(f"⚠️ Alternative playback also failed: {e2}")
                    
                    self.chunk_queue.task_done()
                    
                except queue.Empty:
                    # No chunks available, continue waiting
                    continue
                except Exception as e:
                    print(f"❌ Playback worker error: {e}")
                    break
            
            print(f"✅ Playback complete - {chunks_played} chunks played")
            pygame.mixer.quit()
            
        except Exception as e:
            print(f"❌ Playback worker failed: {e}")
    
    def speak_streaming(self, text: str) -> Dict:
        """
        Main streaming synthesis function
        Returns performance metrics and success status
        """
        start_time = time.time()
        self.metrics = {
            'first_chunk_time': None,
            'total_chunks': 0,
            'playback_started': False,
            'synthesis_time': 0,
            'total_time': 0
        }
        
        print(f"🎵 K2-SO Streaming: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        # Step 1: Initialize TTS
        if not self._initialize_tts():
            return {
                'success': False,
                'error': 'TTS initialization failed',
                'metrics': self.metrics
            }
        
        # Step 2: Generate complete audio file
        print("⚙️ Generating audio...")
        audio_file = self._generate_audio_file(text)
        if not audio_file:
            return {
                'success': False,
                'error': 'Audio generation failed',
                'metrics': self.metrics
            }
        
        # Step 3: Start playback worker thread
        self.generation_complete = False
        self.playback_thread = threading.Thread(target=self._audio_playback_worker)
        self.playback_thread.start()
        
        # Step 4: Stream audio chunks to playback queue
        try:
            chunk_count = 0
            for chunk in self._chunk_audio_generator(audio_file):
                self.chunk_queue.put(chunk)
                chunk_count += 1
                
                # Log first chunk timing
                if chunk_count == 1:
                    first_chunk_latency = time.time() - start_time
                    print(f"🎯 First chunk ready in {first_chunk_latency:.2f}s")
            
            # Wait for playback to complete
            self.playback_thread.join()
            
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            return {
                'success': False,
                'error': f'Streaming failed: {e}',
                'metrics': self.metrics
            }
        finally:
            # Cleanup temporary file
            if audio_file and os.path.exists(audio_file):
                os.unlink(audio_file)
        
        # Calculate final metrics
        total_time = time.time() - start_time
        perceived_latency = self.metrics['first_chunk_time'] - start_time if self.metrics['first_chunk_time'] else total_time
        
        self.metrics.update({
            'total_time': total_time,
            'perceived_latency': perceived_latency,
            'improvement': ((5.2 - perceived_latency) / 5.2) * 100,  # vs baseline
            'chunks_processed': chunk_count
        })
        
        print(f"✅ Streaming complete!")
        print(f"   📊 Perceived latency: {perceived_latency:.2f}s")
        print(f"   📈 Improvement: {self.metrics['improvement']:.1f}% vs baseline")
        print(f"   ⏱️ Total time: {total_time:.2f}s")
        
        return {
            'success': True,
            'metrics': self.metrics,
            'text': text
        }

class StreamingK2SODemo:
    """Demo class for testing streaming synthesis"""
    
    def __init__(self):
        self.streaming_tts = K2SOStreamingSynthesis()
    
    def run_performance_test(self):
        """Run performance tests with different phrase lengths"""
        print("🏁 K2-SO STREAMING SYNTHESIS PERFORMANCE TEST")
        print("=" * 60)
        
        test_phrases = [
            ("Short", "Affirmative"),
            ("Medium", "I am K2-SO, a droid"),
            ("Long", "Congratulations, you are being rescued"),
            ("Very Long", "The odds of successfully navigating an asteroid field are approximately three thousand seven hundred and twenty to one")
        ]
        
        results = []
        
        for category, phrase in test_phrases:
            print(f"\n🧪 Testing {category} phrase...")
            result = self.streaming_tts.speak_streaming(phrase)
            
            if result['success']:
                metrics = result['metrics']
                results.append({
                    'category': category,
                    'phrase': phrase,
                    'perceived_latency': metrics['perceived_latency'],
                    'total_time': metrics['total_time'],
                    'improvement': metrics['improvement'],
                    'synthesis_time': metrics['synthesis_time']
                })
                print(f"   ✅ Success: {metrics['perceived_latency']:.2f}s perceived")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Summary
        if results:
            avg_latency = sum(r['perceived_latency'] for r in results) / len(results)
            avg_improvement = sum(r['improvement'] for r in results) / len(results)
            
            print(f"\n📊 STREAMING PERFORMANCE SUMMARY:")
            print(f"   Average Perceived Latency: {avg_latency:.2f}s")
            print(f"   Average Improvement: {avg_improvement:.1f}%")
            print(f"   Target Achievement: {'✅ Success' if avg_latency < 3.0 else '⚠️ Needs optimization'}")
            
            # Detailed breakdown
            print(f"\n📋 DETAILED RESULTS:")
            for result in results:
                print(f"   {result['category']:<10} {result['perceived_latency']:>6.2f}s  "
                      f"{result['improvement']:>6.1f}%  '{result['phrase'][:30]}...'")
        
        return results

def main():
    """Phase 1 streaming synthesis implementation demo"""
    print("🚀 K2-SO STREAMING SYNTHESIS - PHASE 1")
    print("Goal: Reduce perceived latency from 5.2s to 2-3s")
    print("=" * 60)
    
    demo = StreamingK2SODemo()
    
    if len(sys.argv) > 1:
        # Command line usage
        if sys.argv[1] == "--test":
            demo.run_performance_test()
        else:
            text = " ".join(sys.argv[1:])
            result = demo.streaming_tts.speak_streaming(text)
            if not result['success']:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
    else:
        # Interactive demo
        demo.run_performance_test()

if __name__ == "__main__":
    main() 