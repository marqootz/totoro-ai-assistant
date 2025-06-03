#!/usr/bin/env python3
"""
Voice Performance Comparison: K2-SO vs George
Benchmark processing time, quality, and resource usage
"""

import os
import sys
import time
import psutil
import threading
from typing import Dict, List, Tuple

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.voice.text_to_speech import TextToSpeech

class VoicePerformanceBenchmark:
    def __init__(self):
        self.results = {}
        self.test_phrases = [
            "Hello, I am testing voice cloning performance.",
            "This is a medium length phrase for performance testing.",
            "The quick brown fox jumps over the lazy dog.",
            "Performance evaluation complete.",
            "I am analyzing voice synthesis speed and quality."
        ]
    
    def monitor_resources(self, duration: float = 10.0) -> Dict:
        """Monitor CPU and memory usage during voice synthesis"""
        process = psutil.Process()
        cpu_percentages = []
        memory_usage = []
        
        start_time = time.time()
        while time.time() - start_time < duration:
            cpu_percentages.append(process.cpu_percent())
            memory_usage.append(process.memory_info().rss / 1024 / 1024)  # MB
            time.sleep(0.1)
        
        return {
            'avg_cpu': sum(cpu_percentages) / len(cpu_percentages),
            'max_cpu': max(cpu_percentages),
            'avg_memory_mb': sum(memory_usage) / len(memory_usage),
            'max_memory_mb': max(memory_usage)
        }
    
    def benchmark_voice(self, voice_name: str, audio_path: str) -> Dict:
        """Benchmark a specific voice configuration"""
        print(f"\n🎤 BENCHMARKING {voice_name.upper()} VOICE")
        print("=" * 50)
        
        if not os.path.exists(audio_path):
            print(f"❌ Voice file not found: {audio_path}")
            return {}
        
        # Initialize TTS
        print("🚀 Initializing TTS...")
        init_start = time.time()
        tts = TextToSpeech(voice_preference="coqui")
        init_time = time.time() - init_start
        
        if not tts.coqui_tts:
            print("❌ Coqui TTS not available")
            return {}
        
        print(f"✅ TTS initialized in {init_time:.2f}s")
        
        # Benchmark each test phrase
        phrase_results = []
        total_audio_duration = 0
        total_processing_time = 0
        
        for i, phrase in enumerate(self.test_phrases, 1):
            print(f"\n🗣️ Test {i}: '{phrase[:40]}{'...' if len(phrase) > 40 else ''}'")
            
            # Start resource monitoring
            monitor_thread = None
            resource_data = {}
            
            def monitor():
                nonlocal resource_data
                resource_data = self.monitor_resources(duration=15.0)
            
            # Measure processing time
            start_time = time.time()
            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.start()
            
            success = tts.speak(phrase, audio_prompt_path=audio_path)
            
            processing_time = time.time() - start_time
            
            # Stop monitoring
            if monitor_thread:
                monitor_thread.join(timeout=1.0)
            
            # Estimate audio duration (rough calculation)
            estimated_audio_duration = len(phrase.split()) * 0.5  # ~0.5s per word
            
            if success:
                phrase_result = {
                    'phrase': phrase,
                    'processing_time': processing_time,
                    'estimated_audio_duration': estimated_audio_duration,
                    'real_time_factor': processing_time / estimated_audio_duration,
                    'success': True,
                    'resources': resource_data
                }
                print(f"✅ Completed in {processing_time:.2f}s (RTF: {phrase_result['real_time_factor']:.2f})")
                
                total_processing_time += processing_time
                total_audio_duration += estimated_audio_duration
                
            else:
                phrase_result = {
                    'phrase': phrase,
                    'processing_time': processing_time,
                    'success': False
                }
                print(f"❌ Failed after {processing_time:.2f}s")
            
            phrase_results.append(phrase_result)
        
        # Calculate overall statistics
        successful_results = [r for r in phrase_results if r['success']]
        
        if successful_results:
            avg_processing_time = sum(r['processing_time'] for r in successful_results) / len(successful_results)
            avg_rtf = sum(r['real_time_factor'] for r in successful_results) / len(successful_results)
            
            # Resource usage statistics
            all_cpu = [r['resources'].get('avg_cpu', 0) for r in successful_results if 'resources' in r]
            all_memory = [r['resources'].get('avg_memory_mb', 0) for r in successful_results if 'resources' in r]
            
            results = {
                'voice_name': voice_name,
                'audio_path': audio_path,
                'initialization_time': init_time,
                'total_phrases': len(self.test_phrases),
                'successful_phrases': len(successful_results),
                'success_rate': len(successful_results) / len(self.test_phrases) * 100,
                'avg_processing_time': avg_processing_time,
                'total_processing_time': total_processing_time,
                'total_audio_duration': total_audio_duration,
                'overall_rtf': total_processing_time / total_audio_duration if total_audio_duration > 0 else float('inf'),
                'avg_rtf': avg_rtf,
                'avg_cpu_usage': sum(all_cpu) / len(all_cpu) if all_cpu else 0,
                'avg_memory_usage_mb': sum(all_memory) / len(all_memory) if all_memory else 0,
                'phrase_results': phrase_results
            }
            
            print(f"\n📊 {voice_name.upper()} VOICE SUMMARY:")
            print(f"   Success Rate: {results['success_rate']:.1f}%")
            print(f"   Avg Processing Time: {results['avg_processing_time']:.2f}s")
            print(f"   Avg Real-time Factor: {results['avg_rtf']:.2f}x")
            print(f"   Avg CPU Usage: {results['avg_cpu_usage']:.1f}%")
            print(f"   Avg Memory Usage: {results['avg_memory_usage_mb']:.1f} MB")
            
            return results
        
        else:
            return {
                'voice_name': voice_name,
                'audio_path': audio_path,
                'initialization_time': init_time,
                'success_rate': 0,
                'error': 'All phrase tests failed'
            }
    
    def compare_voices(self) -> Dict:
        """Compare K2-SO and George voices"""
        print("🏁 VOICE PERFORMANCE COMPARISON")
        print("=" * 60)
        
        comparison_results = {}
        
        # Test K2-SO voice (original)
        k2so_original = self.benchmark_voice("K2-SO Original", "assets/k2so-voice-samples.mp3")
        if k2so_original:
            comparison_results['k2so_original'] = k2so_original
        
        # Test K2-SO voice (cleaned, if exists)
        k2so_clean_path = "assets/k2so-voice-samples-clean.mp3"
        if os.path.exists(k2so_clean_path):
            k2so_clean = self.benchmark_voice("K2-SO Clean", k2so_clean_path)
            if k2so_clean:
                comparison_results['k2so_clean'] = k2so_clean
        
        # Test George voice (if exists)
        george_path = "assets/george-source-voice.mp3"
        if os.path.exists(george_path):
            george_original = self.benchmark_voice("George Original", george_path)
            if george_original:
                comparison_results['george_original'] = george_original
        
        # Test George voice (cleaned, if exists)
        george_clean_path = "assets/george-source-voice-clean.mp3"
        if os.path.exists(george_clean_path):
            george_clean = self.benchmark_voice("George Clean", george_clean_path)
            if george_clean:
                comparison_results['george_clean'] = george_clean
        
        return comparison_results
    
    def generate_report(self, results: Dict):
        """Generate comprehensive comparison report"""
        print(f"\n📈 COMPREHENSIVE PERFORMANCE REPORT")
        print("=" * 70)
        
        if not results:
            print("❌ No results to compare")
            return
        
        # Create comparison table
        print(f"\n{'Voice':<20} {'Success%':<10} {'Avg Time':<12} {'Avg RTF':<10} {'CPU%':<8} {'Memory':<10}")
        print("-" * 70)
        
        for key, result in results.items():
            if 'success_rate' in result:
                print(f"{result['voice_name']:<20} "
                      f"{result['success_rate']:<10.1f} "
                      f"{result['avg_processing_time']:<12.2f} "
                      f"{result['avg_rtf']:<10.2f} "
                      f"{result['avg_cpu_usage']:<8.1f} "
                      f"{result['avg_memory_usage_mb']:<10.1f}")
        
        # Performance recommendations
        print(f"\n🏆 PERFORMANCE ANALYSIS:")
        
        # Find fastest voice
        valid_results = {k: v for k, v in results.items() if 'avg_processing_time' in v}
        if valid_results:
            fastest = min(valid_results.items(), key=lambda x: x[1]['avg_processing_time'])
            most_efficient = min(valid_results.items(), key=lambda x: x[1]['avg_rtf'])
            
            print(f"   🚀 Fastest Processing: {fastest[1]['voice_name']} ({fastest[1]['avg_processing_time']:.2f}s avg)")
            print(f"   ⚡ Most Efficient RTF: {most_efficient[1]['voice_name']} ({most_efficient[1]['avg_rtf']:.2f}x)")
            
            # Compare K2-SO vs George if both exist
            k2so_results = [v for k, v in valid_results.items() if 'k2so' in k.lower()]
            george_results = [v for k, v in valid_results.items() if 'george' in k.lower()]
            
            if k2so_results and george_results:
                k2so_best = min(k2so_results, key=lambda x: x['avg_processing_time'])
                george_best = min(george_results, key=lambda x: x['avg_processing_time'])
                
                speed_diff = k2so_best['avg_processing_time'] / george_best['avg_processing_time']
                rtf_diff = k2so_best['avg_rtf'] / george_best['avg_rtf']
                
                print(f"\n🤖 K2-SO vs 👤 GEORGE COMPARISON:")
                print(f"   Speed Ratio: {speed_diff:.2f}x ({'K2-SO faster' if speed_diff < 1 else 'George faster'})")
                print(f"   Efficiency Ratio: {rtf_diff:.2f}x ({'K2-SO more efficient' if rtf_diff < 1 else 'George more efficient'})")
        
        # Audio preprocessing recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if 'k2so_clean' in results and 'k2so_original' in results:
            clean = results['k2so_clean']
            original = results['k2so_original']
            improvement = (original['avg_processing_time'] - clean['avg_processing_time']) / original['avg_processing_time'] * 100
            print(f"   🧹 Noise reduction improved K2-SO performance by {improvement:.1f}%")
        
        print(f"   🎛️ Run audio preprocessing: python audio_preprocessing.py")
        print(f"   🔧 For best performance, use the fastest configuration identified above")

def main():
    """Main comparison function"""
    benchmark = VoicePerformanceBenchmark()
    
    # Run comparison
    results = benchmark.compare_voices()
    
    # Generate report
    benchmark.generate_report(results)
    
    print(f"\n✨ Performance comparison complete!")

if __name__ == "__main__":
    main() 