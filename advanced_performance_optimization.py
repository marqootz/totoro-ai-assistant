#!/usr/bin/env python3
"""
Advanced Performance Optimization for K2-SO Voice
Sampling rate optimization, model tuning, and performance enhancements
"""

import os
import sys
import librosa
import soundfile as sf
import numpy as np
import time
import tempfile
from typing import Dict, List, Tuple, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.voice.text_to_speech import TextToSpeech

class AdvancedK2SOOptimizer:
    def __init__(self):
        self.current_audio_specs = {}
        self.optimization_results = {}
        
        # Common TTS sample rates for optimization testing
        self.test_sample_rates = [16000, 22050, 24000, 44100, 48000]
        
        # XTTS v2 optimal configurations (based on research)
        self.xtts_optimal_config = {
            'sample_rate': 22050,  # XTTS v2 typically works best at 22050 Hz
            'chunk_length_s': 20,   # Shorter chunks for faster processing
            'overlap_wav_s': 1.0,   # Overlap for seamless audio
            'temperature': 0.7,     # Lower temperature for more consistent output
            'length_penalty': 1.0,  # Standard length penalty
            'repetition_penalty': 5.0, # Reduce repetition
            'top_k': 50,           # Limit vocabulary for faster generation
            'top_p': 0.85,         # Nucleus sampling
            'speed': 1.0           # Playback speed
        }
    
    def analyze_current_audio(self) -> Dict:
        """Analyze current K2-SO audio specifications"""
        print("🔍 ANALYZING CURRENT AUDIO SPECIFICATIONS")
        print("=" * 60)
        
        files_to_analyze = [
            ("K2-SO Original", "assets/k2so-voice-samples.mp3"),
            ("K2-SO Clean", "assets/k2so-voice-samples-clean.mp3"),
            ("George Original", "assets/george-source-voice.mp3"),
            ("George Clean", "assets/george-source-voice-clean.mp3")
        ]
        
        analysis_results = {}
        
        for name, file_path in files_to_analyze:
            if os.path.exists(file_path):
                try:
                    # Load with original sample rate
                    audio, sr = librosa.load(file_path, sr=None)
                    
                    # Calculate audio characteristics
                    duration = len(audio) / sr
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    rms_energy = np.sqrt(np.mean(audio**2))
                    dynamic_range = np.max(audio) - np.min(audio)
                    
                    # Frequency analysis
                    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
                    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(audio))
                    
                    analysis_results[name] = {
                        'file_path': file_path,
                        'sample_rate': sr,
                        'duration': duration,
                        'file_size_mb': file_size_mb,
                        'rms_energy': rms_energy,
                        'dynamic_range': dynamic_range,
                        'spectral_centroid': spectral_centroid,
                        'zero_crossing_rate': zero_crossing_rate,
                        'bits_per_second': (file_size_mb * 8 * 1024 * 1024) / duration
                    }
                    
                    print(f"📊 {name}:")
                    print(f"   Sample Rate: {sr} Hz")
                    print(f"   Duration: {duration:.2f}s")
                    print(f"   File Size: {file_size_mb:.2f} MB")
                    print(f"   RMS Energy: {rms_energy:.4f}")
                    print(f"   Spectral Centroid: {spectral_centroid:.2f} Hz")
                    print(f"   Bitrate: {analysis_results[name]['bits_per_second']/1000:.0f} kbps")
                    print()
                    
                except Exception as e:
                    print(f"❌ Error analyzing {name}: {e}")
            else:
                print(f"⚠️ {name}: File not found ({file_path})")
        
        self.current_audio_specs = analysis_results
        return analysis_results
    
    def create_optimized_samples(self) -> Dict[str, str]:
        """Create optimized audio samples with different configurations"""
        print("🚀 CREATING OPTIMIZED AUDIO SAMPLES")
        print("=" * 60)
        
        source_file = "assets/k2so-voice-samples-clean.mp3"
        if not os.path.exists(source_file):
            source_file = "assets/k2so-voice-samples.mp3"
        
        if not os.path.exists(source_file):
            print("❌ No K2-SO source file found!")
            return {}
        
        # Load original audio
        audio_original, sr_original = librosa.load(source_file, sr=None)
        print(f"📁 Source: {source_file} ({sr_original} Hz)")
        
        optimized_files = {}
        
        # Optimization 1: XTTS v2 Optimal Sample Rate (22050 Hz)
        print("\n🎛️ Creating 22050 Hz optimized version...")
        audio_22k = librosa.resample(audio_original, orig_sr=sr_original, target_sr=22050)
        output_22k = "assets/k2so-voice-samples-22050hz.mp3"
        sf.write(output_22k, audio_22k, 22050)
        optimized_files['22050Hz'] = output_22k
        print(f"✅ Created: {output_22k}")
        
        # Optimization 2: Compact 16kHz version for speed
        print("\n📻 Creating 16kHz compact version...")
        audio_16k = librosa.resample(audio_original, orig_sr=sr_original, target_sr=16000)
        output_16k = "assets/k2so-voice-samples-16000hz.mp3"
        sf.write(output_16k, audio_16k, 16000)
        optimized_files['16000Hz'] = output_16k
        print(f"✅ Created: {output_16k}")
        
        # Optimization 3: Shortened version (first 60 seconds for faster processing)
        print("\n✂️ Creating shortened version (60s)...")
        duration_limit = 60  # seconds
        samples_limit = int(duration_limit * sr_original)
        audio_short = audio_original[:min(samples_limit, len(audio_original))]
        output_short = "assets/k2so-voice-samples-short.mp3"
        sf.write(output_short, audio_short, sr_original)
        optimized_files['shortened'] = output_short
        print(f"✅ Created: {output_short} ({len(audio_short)/sr_original:.1f}s)")
        
        # Optimization 4: Combined - 22050Hz + shortened
        print("\n⚡ Creating optimized combo (22050Hz + 60s)...")
        audio_short_22k = librosa.resample(audio_short, orig_sr=sr_original, target_sr=22050)
        output_combo = "assets/k2so-voice-samples-optimized.mp3"
        sf.write(output_combo, audio_short_22k, 22050)
        optimized_files['optimized'] = output_combo
        print(f"✅ Created: {output_combo}")
        
        print(f"\n📈 OPTIMIZATION SUMMARY:")
        for name, file_path in optimized_files.items():
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            audio_test, sr_test = librosa.load(file_path, sr=None)
            duration_test = len(audio_test) / sr_test
            print(f"   {name}: {size_mb:.2f}MB, {duration_test:.1f}s, {sr_test}Hz")
        
        return optimized_files
    
    def benchmark_sample_rates(self) -> Dict:
        """Benchmark different sample rate configurations"""
        print("🏁 SAMPLE RATE PERFORMANCE BENCHMARK")
        print("=" * 60)
        
        # Create test files if they don't exist
        optimized_files = self.create_optimized_samples()
        
        test_configs = [
            ("Original (44100Hz)", "assets/k2so-voice-samples.mp3"),
            ("Clean (44100Hz)", "assets/k2so-voice-samples-clean.mp3"),
            ("Optimized 22050Hz", optimized_files.get('22050Hz')),
            ("Compact 16000Hz", optimized_files.get('16000Hz')),
            ("Shortened", optimized_files.get('shortened')),
            ("Optimized Combo", optimized_files.get('optimized'))
        ]
        
        test_phrase = "I am K2-SO. Congratulations, you are being rescued."
        benchmark_results = {}
        
        for config_name, audio_path in test_configs:
            if not audio_path or not os.path.exists(audio_path):
                print(f"⚠️ Skipping {config_name}: File not found")
                continue
            
            print(f"\n🧪 Testing {config_name}...")
            
            # Initialize TTS
            start_time = time.time()
            tts = TextToSpeech(voice_preference="coqui")
            init_time = time.time() - start_time
            
            if not tts.coqui_tts:
                print(f"❌ Failed to initialize TTS for {config_name}")
                continue
            
            # Benchmark synthesis
            synthesis_start = time.time()
            success = tts.speak(test_phrase, audio_prompt_path=audio_path)
            synthesis_time = time.time() - synthesis_start
            
            # Get file info
            file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            audio_info, sr_info = librosa.load(audio_path, sr=None)
            duration_info = len(audio_info) / sr_info
            
            benchmark_results[config_name] = {
                'audio_path': audio_path,
                'file_size_mb': file_size_mb,
                'sample_rate': sr_info,
                'duration': duration_info,
                'init_time': init_time,
                'synthesis_time': synthesis_time,
                'total_time': init_time + synthesis_time,
                'success': success,
                'size_to_time_ratio': file_size_mb / synthesis_time if success else float('inf')
            }
            
            if success:
                print(f"✅ Success: {synthesis_time:.2f}s synthesis")
                print(f"   File: {file_size_mb:.2f}MB, {sr_info}Hz, {duration_info:.1f}s")
                print(f"   Efficiency: {file_size_mb/synthesis_time:.3f} MB/s")
            else:
                print(f"❌ Failed after {synthesis_time:.2f}s")
        
        return benchmark_results
    
    def analyze_results_and_recommend(self, results: Dict) -> Dict:
        """Analyze benchmark results and provide recommendations"""
        print(f"\n📈 PERFORMANCE ANALYSIS & RECOMMENDATIONS")
        print("=" * 70)
        
        successful_results = {k: v for k, v in results.items() if v['success']}
        
        if not successful_results:
            print("❌ No successful benchmarks to analyze")
            return {}
        
        # Find optimal configurations
        fastest_synthesis = min(successful_results.items(), key=lambda x: x[1]['synthesis_time'])
        smallest_file = min(successful_results.items(), key=lambda x: x[1]['file_size_mb'])
        best_efficiency = min(successful_results.items(), key=lambda x: x[1]['size_to_time_ratio'])
        
        print(f"🏆 WINNERS:")
        print(f"   🚀 Fastest Synthesis: {fastest_synthesis[0]} ({fastest_synthesis[1]['synthesis_time']:.2f}s)")
        print(f"   📦 Smallest File: {smallest_file[0]} ({smallest_file[1]['file_size_mb']:.2f}MB)")
        print(f"   ⚡ Best Efficiency: {best_efficiency[0]} ({best_efficiency[1]['size_to_time_ratio']:.3f} MB/s)")
        
        # Performance comparison table
        print(f"\n📊 DETAILED COMPARISON:")
        print(f"{'Configuration':<20} {'Size(MB)':<10} {'Rate(Hz)':<10} {'Synth(s)':<10} {'Efficiency':<12}")
        print("-" * 70)
        
        for name, data in successful_results.items():
            print(f"{name[:19]:<20} "
                  f"{data['file_size_mb']:<10.2f} "
                  f"{data['sample_rate']:<10.0f} "
                  f"{data['synthesis_time']:<10.2f} "
                  f"{data['size_to_time_ratio']:<12.3f}")
        
        # Recommendations
        recommendations = {
            'fastest_config': fastest_synthesis[0],
            'fastest_path': fastest_synthesis[1]['audio_path'],
            'recommended_sample_rate': fastest_synthesis[1]['sample_rate'],
            'expected_performance_improvement': self._calculate_improvement(results),
            'optimal_file_size': smallest_file[1]['file_size_mb'],
            'recommendations': []
        }
        
        # Generate specific recommendations
        if fastest_synthesis[1]['sample_rate'] == 22050:
            recommendations['recommendations'].append("✅ 22050Hz is optimal for XTTS v2")
        elif fastest_synthesis[1]['sample_rate'] == 16000:
            recommendations['recommendations'].append("📻 16000Hz provides fastest processing")
        
        if 'Optimized Combo' in fastest_synthesis[0]:
            recommendations['recommendations'].append("⚡ Combined optimizations (sample rate + duration) work best")
        
        if fastest_synthesis[1]['file_size_mb'] < 2.0:
            recommendations['recommendations'].append("📦 Shorter voice samples significantly improve performance")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in recommendations['recommendations']:
            print(f"   {rec}")
        
        print(f"\n🎯 OPTIMAL CONFIGURATION:")
        print(f"   File: {recommendations['fastest_path']}")
        print(f"   Sample Rate: {recommendations['recommended_sample_rate']} Hz")
        print(f"   Expected Performance: {recommendations['expected_performance_improvement']}")
        
        return recommendations
    
    def _calculate_improvement(self, results: Dict) -> str:
        """Calculate performance improvement percentage"""
        if 'Original (44100Hz)' in results and results['Original (44100Hz)']['success']:
            original_time = results['Original (44100Hz)']['synthesis_time']
            
            # Find best performing configuration
            successful_results = {k: v for k, v in results.items() if v['success']}
            if successful_results:
                best_time = min(successful_results.values(), key=lambda x: x['synthesis_time'])['synthesis_time']
                improvement = ((original_time - best_time) / original_time) * 100
                return f"{improvement:.1f}% faster than original"
        
        return "Baseline measurement"
    
    def create_production_config(self, recommendations: Dict):
        """Create optimized production configuration"""
        print(f"\n🏭 CREATING PRODUCTION CONFIGURATION")
        print("=" * 60)
        
        config_content = f'''#!/usr/bin/env python3
"""
Optimized K2-SO Voice Production Configuration
Auto-generated based on performance benchmarking
"""

import os

# Optimal Audio Configuration
OPTIMAL_K2SO_CONFIG = {{
    'audio_path': '{recommendations.get('fastest_path', 'assets/k2so-voice-samples-clean.mp3')}',
    'sample_rate': {recommendations.get('recommended_sample_rate', 22050)},
    'expected_performance': '{recommendations.get('expected_performance_improvement', 'Optimized')}',
    'file_size_mb': {recommendations.get('optimal_file_size', 1.5):.2f}
}}

# XTTS v2 Optimal Settings
XTTS_PRODUCTION_CONFIG = {self.xtts_optimal_config}

# Performance Thresholds
PERFORMANCE_TARGETS = {{
    'short_phrase_max_time': 2.5,  # seconds
    'medium_phrase_max_time': 4.0,  # seconds
    'long_phrase_max_time': 6.0,   # seconds
    'model_load_max_time': 15.0    # seconds
}}

def get_optimal_audio_path():
    """Get the optimal audio path for K2-SO voice"""
    optimal_path = OPTIMAL_K2SO_CONFIG['audio_path']
    if os.path.exists(optimal_path):
        return optimal_path
    
    # Fallback chain
    fallbacks = [
        'assets/k2so-voice-samples-optimized.mp3',
        'assets/k2so-voice-samples-22050hz.mp3',
        'assets/k2so-voice-samples-clean.mp3',
        'assets/k2so-voice-samples.mp3'
    ]
    
    for fallback in fallbacks:
        if os.path.exists(fallback):
            return fallback
    
    raise FileNotFoundError("No K2-SO voice file found!")

if __name__ == "__main__":
    print("🤖 K2-SO Production Configuration")
    print(f"Optimal audio: {{OPTIMAL_K2SO_CONFIG['audio_path']}}")
    print(f"Sample rate: {{OPTIMAL_K2SO_CONFIG['sample_rate']}} Hz")
    print(f"Performance: {{OPTIMAL_K2SO_CONFIG['expected_performance']}}")
'''
        
        config_path = "k2so_production_config.py"
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        print(f"✅ Created production config: {config_path}")
        print(f"📋 Optimal settings saved for deployment")
        
        return config_path

def main():
    """Main optimization workflow"""
    optimizer = AdvancedK2SOOptimizer()
    
    # Step 1: Analyze current audio
    current_specs = optimizer.analyze_current_audio()
    
    # Step 2: Create optimized samples
    optimized_files = optimizer.create_optimized_samples()
    
    # Step 3: Benchmark different configurations
    benchmark_results = optimizer.benchmark_sample_rates()
    
    # Step 4: Analyze and recommend
    recommendations = optimizer.analyze_results_and_recommend(benchmark_results)
    
    # Step 5: Create production configuration
    if recommendations:
        config_path = optimizer.create_production_config(recommendations)
        
        print(f"\n🎉 OPTIMIZATION COMPLETE!")
        print(f"✅ Use production config: python {config_path}")
        print(f"🚀 Expected improvement: {recommendations.get('expected_performance_improvement', 'Optimized')}")

if __name__ == "__main__":
    main() 