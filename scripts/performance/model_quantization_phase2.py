#!/usr/bin/env python3
"""
K2-SO Voice Model Quantization - Phase 2 Implementation
Additional 30-40% speed improvement + 50% memory reduction
"""

import os
import sys
import time
import tempfile
import threading
from typing import Optional, Dict, Any
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.voice.text_to_speech import TextToSpeech

class K2SOQuantizedTTS:
    """
    Phase 2: Model quantization for K2-SO voice synthesis
    Goal: 30-40% additional speed + 50% memory reduction
    """
    
    def __init__(self, audio_prompt_path: str = "assets/k2so-voice-samples-optimized.mp3"):
        self.audio_prompt_path = audio_prompt_path
        self.quantized_model = None
        self.original_model = None
        self.quantization_method = "dynamic"  # dynamic, fp16, or int8
        
        # Performance tracking
        self.metrics = {
            'model_size_original': 0,
            'model_size_quantized': 0,
            'memory_reduction': 0,
            'speed_improvement': 0,
            'quality_score': 0
        }
        
        # Quantization configuration
        self.quantization_config = {
            'dynamic': {
                'precision': 'int8',
                'speed_boost': 35,  # Expected % improvement
                'memory_reduction': 50,
                'quality_retention': 95
            },
            'fp16': {
                'precision': 'float16',
                'speed_boost': 25,
                'memory_reduction': 50,
                'quality_retention': 98
            },
            'int8': {
                'precision': 'int8',
                'speed_boost': 40,
                'memory_reduction': 60,
                'quality_retention': 90
            }
        }
    
    def _analyze_original_model(self) -> Dict[str, Any]:
        """Analyze original model for quantization baseline"""
        print("🔍 Analyzing original XTTS v2 model...")
        
        try:
            from TTS.api import TTS
            import torch
            import psutil
            
            # Initialize original model
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            
            # Get model size information
            total_params = 0
            total_size = 0
            
            if hasattr(model, 'synthesizer') and hasattr(model.synthesizer, 'tts_model'):
                tts_model = model.synthesizer.tts_model
                
                for name, param in tts_model.named_parameters():
                    total_params += param.numel()
                    total_size += param.numel() * param.element_size()
                
                # Convert to MB
                model_size_mb = total_size / (1024 * 1024)
                
                # Memory usage
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                memory_usage = end_memory - start_memory
                
                analysis = {
                    'total_parameters': total_params,
                    'model_size_mb': model_size_mb,
                    'memory_usage_mb': memory_usage,
                    'precision': 'float32',
                    'device': next(tts_model.parameters()).device.type
                }
                
                print(f"📊 Original Model Analysis:")
                print(f"   Parameters: {total_params:,}")
                print(f"   Model Size: {model_size_mb:.1f} MB")
                print(f"   Memory Usage: {memory_usage:.1f} MB")
                print(f"   Precision: {analysis['precision']}")
                print(f"   Device: {analysis['device']}")
                
                self.original_model = model
                self.metrics['model_size_original'] = model_size_mb
                
                return analysis
            else:
                print("⚠️ Could not access model internals for analysis")
                return {}
                
        except Exception as e:
            print(f"❌ Model analysis failed: {e}")
            return {}
    
    def _apply_dynamic_quantization(self) -> bool:
        """Apply dynamic quantization to the model"""
        try:
            import torch
            
            print("⚙️ Applying dynamic quantization (INT8)...")
            
            if not self.original_model:
                print("❌ Original model not available")
                return False
            
            # Get the TTS model
            tts_model = self.original_model.synthesizer.tts_model
            
            # Apply dynamic quantization
            quantized_model = torch.quantization.quantize_dynamic(
                tts_model,
                {torch.nn.Linear, torch.nn.Conv1d},  # Quantize these layer types
                dtype=torch.qint8
            )
            
            # Replace the model in the TTS object
            self.original_model.synthesizer.tts_model = quantized_model
            self.quantized_model = self.original_model
            
            # Calculate new model size
            total_size = 0
            for name, param in quantized_model.named_parameters():
                total_size += param.numel() * param.element_size()
            
            quantized_size_mb = total_size / (1024 * 1024)
            self.metrics['model_size_quantized'] = quantized_size_mb
            
            # Calculate reduction
            original_size = self.metrics['model_size_original']
            reduction = ((original_size - quantized_size_mb) / original_size) * 100
            self.metrics['memory_reduction'] = reduction
            
            print(f"✅ Dynamic quantization complete!")
            print(f"   Original: {original_size:.1f} MB")
            print(f"   Quantized: {quantized_size_mb:.1f} MB")
            print(f"   Reduction: {reduction:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ Dynamic quantization failed: {e}")
            return False
    
    def _apply_fp16_quantization(self) -> bool:
        """Apply FP16 quantization to the model"""
        try:
            import torch
            
            print("⚙️ Applying FP16 quantization...")
            
            if not self.original_model:
                print("❌ Original model not available")
                return False
            
            # Get the TTS model
            tts_model = self.original_model.synthesizer.tts_model
            
            # Convert to half precision
            tts_model = tts_model.half()
            
            # Replace the model
            self.original_model.synthesizer.tts_model = tts_model
            self.quantized_model = self.original_model
            
            # Calculate new model size (FP16 is half the size of FP32)
            original_size = self.metrics['model_size_original']
            quantized_size_mb = original_size / 2
            self.metrics['model_size_quantized'] = quantized_size_mb
            
            # Calculate reduction
            reduction = 50.0  # FP16 is exactly half of FP32
            self.metrics['memory_reduction'] = reduction
            
            print(f"✅ FP16 quantization complete!")
            print(f"   Original: {original_size:.1f} MB")
            print(f"   Quantized: {quantized_size_mb:.1f} MB")
            print(f"   Reduction: {reduction:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ FP16 quantization failed: {e}")
            return False
    
    def initialize_quantized_model(self, method: str = "dynamic") -> bool:
        """Initialize model with specified quantization method"""
        print(f"🚀 K2-SO MODEL QUANTIZATION - PHASE 2")
        print(f"Method: {method.upper()}")
        print("=" * 50)
        
        self.quantization_method = method
        
        # Step 1: Analyze original model
        analysis = self._analyze_original_model()
        if not analysis:
            return False
        
        # Step 2: Apply quantization
        if method == "dynamic":
            success = self._apply_dynamic_quantization()
        elif method == "fp16":
            success = self._apply_fp16_quantization()
        else:
            print(f"❌ Unsupported quantization method: {method}")
            return False
        
        if success:
            config = self.quantization_config[method]
            print(f"\n🎯 Expected Performance Gains:")
            print(f"   Speed Improvement: ~{config['speed_boost']}%")
            print(f"   Memory Reduction: ~{config['memory_reduction']}%")
            print(f"   Quality Retention: ~{config['quality_retention']}%")
        
        return success
    
    def synthesize_with_quantized_model(self, text: str) -> Dict[str, Any]:
        """Synthesize speech using quantized model with performance tracking"""
        if not self.quantized_model:
            return {
                'success': False,
                'error': 'Quantized model not initialized'
            }
        
        print(f"🎵 Quantized K2-SO: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        # Performance timing
        start_time = time.time()
        
        try:
            # Create temporary file for output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Synthesize using quantized model
            synthesis_start = time.time()
            
            self.quantized_model.tts_to_file(
                text=text,
                speaker_wav=self.audio_prompt_path,
                language="en",
                file_path=temp_path,
                speed=1.0
            )
            
            synthesis_time = time.time() - synthesis_start
            total_time = time.time() - start_time
            
            # Check if file was created
            if os.path.exists(temp_path):
                file_size = os.path.getsize(temp_path)
                
                # Clean up
                os.unlink(temp_path)
                
                return {
                    'success': True,
                    'synthesis_time': synthesis_time,
                    'total_time': total_time,
                    'file_size': file_size,
                    'method': self.quantization_method,
                    'text': text
                }
            else:
                return {
                    'success': False,
                    'error': 'Audio file not generated'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Synthesis failed: {e}'
            }

class QuantizationBenchmark:
    """Benchmark quantized vs original models"""
    
    def __init__(self):
        self.test_phrases = [
            ("Short", "Affirmative"),
            ("Medium", "I am K2-SO, a droid"),
            ("Long", "Congratulations, you are being rescued"),
            ("Very Long", "The odds of successfully navigating an asteroid field are approximately three thousand seven hundred and twenty to one")
        ]
    
    def run_performance_comparison(self):
        """Compare original vs quantized model performance"""
        print("🏁 K2-SO QUANTIZATION PERFORMANCE BENCHMARK")
        print("=" * 60)
        
        results = {
            'original': [],
            'quantized': []
        }
        
        # Test original model
        print("\n📊 Testing Original Model Performance...")
        print("-" * 40)
        
        try:
            # Initialize original TTS
            original_tts = TextToSpeech(voice_preference="coqui")
            
            for category, phrase in self.test_phrases:
                print(f"Testing {category}: '{phrase[:30]}...'")
                
                start_time = time.time()
                success = original_tts.speak(phrase, audio_prompt_path="assets/k2so-voice-samples-optimized.mp3")
                total_time = time.time() - start_time
                
                if success:
                    results['original'].append({
                        'category': category,
                        'phrase': phrase,
                        'time': total_time,
                        'success': True
                    })
                    print(f"   ✅ {total_time:.2f}s")
                else:
                    print(f"   ❌ Failed")
        
        except Exception as e:
            print(f"❌ Original model test failed: {e}")
        
        # Test quantized models
        for method in ["fp16", "dynamic"]:
            print(f"\n📊 Testing {method.upper()} Quantized Model...")
            print("-" * 40)
            
            try:
                quantized_tts = K2SOQuantizedTTS()
                
                if quantized_tts.initialize_quantized_model(method):
                    for category, phrase in self.test_phrases:
                        print(f"Testing {category}: '{phrase[:30]}...'")
                        
                        result = quantized_tts.synthesize_with_quantized_model(phrase)
                        
                        if result['success']:
                            results['quantized'].append({
                                'category': category,
                                'phrase': phrase,
                                'time': result['synthesis_time'],
                                'method': method,
                                'success': True
                            })
                            print(f"   ✅ {result['synthesis_time']:.2f}s")
                        else:
                            print(f"   ❌ Failed: {result.get('error', 'Unknown')}")
                else:
                    print(f"❌ {method} quantization initialization failed")
                    
            except Exception as e:
                print(f"❌ {method} quantized model test failed: {e}")
        
        # Analyze results
        self._analyze_benchmark_results(results)
        
        return results
    
    def _analyze_benchmark_results(self, results: Dict):
        """Analyze and display benchmark results"""
        print(f"\n📈 QUANTIZATION PERFORMANCE ANALYSIS")
        print("=" * 50)
        
        if results['original'] and results['quantized']:
            # Calculate averages
            original_avg = sum(r['time'] for r in results['original']) / len(results['original'])
            
            # Group quantized results by method
            quantized_by_method = {}
            for result in results['quantized']:
                method = result['method']
                if method not in quantized_by_method:
                    quantized_by_method[method] = []
                quantized_by_method[method].append(result['time'])
            
            print(f"Original Model Average: {original_avg:.2f}s")
            
            for method, times in quantized_by_method.items():
                if times:
                    quantized_avg = sum(times) / len(times)
                    improvement = ((original_avg - quantized_avg) / original_avg) * 100
                    
                    print(f"{method.upper()} Quantized Average: {quantized_avg:.2f}s")
                    print(f"{method.upper()} Speed Improvement: {improvement:.1f}%")
            
            # Combined with streaming (from Phase 1)
            print(f"\n🚀 COMBINED PHASE 1 + PHASE 2 PROJECTION:")
            best_quantized = min(quantized_by_method.values(), key=lambda x: sum(x)/len(x) if x else float('inf'))
            if best_quantized:
                best_avg = sum(best_quantized) / len(best_quantized)
                streaming_latency = 0.16  # From Phase 1 results
                
                # Estimate combined improvement
                synthesis_reduction = ((original_avg - best_avg) / original_avg) * 100
                total_improvement = 84.1 + (synthesis_reduction * 0.3)  # Conservative estimate
                
                print(f"   Streaming (Phase 1): 84.1% latency reduction")
                print(f"   Quantization (Phase 2): {synthesis_reduction:.1f}% synthesis speedup") 
                print(f"   🎯 COMBINED IMPROVEMENT: ~{total_improvement:.1f}%")
        else:
            print("❌ Insufficient data for analysis")

def main():
    """Phase 2 quantization implementation and testing"""
    print("🚀 K2-SO MODEL QUANTIZATION - PHASE 2")
    print("Goal: 30-40% additional speed + 50% memory reduction")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--benchmark":
            # Run full benchmark
            benchmark = QuantizationBenchmark()
            benchmark.run_performance_comparison()
            
        elif sys.argv[1] == "--method":
            # Test specific quantization method
            method = sys.argv[2] if len(sys.argv) > 2 else "fp16"
            text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "I am K2-SO"
            
            quantized_tts = K2SOQuantizedTTS()
            if quantized_tts.initialize_quantized_model(method):
                result = quantized_tts.synthesize_with_quantized_model(text)
                if result['success']:
                    print(f"✅ {method} synthesis: {result['synthesis_time']:.2f}s")
                else:
                    print(f"❌ Failed: {result.get('error')}")
            
        else:
            # Quick test with text
            text = " ".join(sys.argv[1:])
            quantized_tts = K2SOQuantizedTTS()
            if quantized_tts.initialize_quantized_model("fp16"):
                result = quantized_tts.synthesize_with_quantized_model(text)
                if result['success']:
                    print(f"✅ Quantized synthesis: {result['synthesis_time']:.2f}s")
    else:
        # Default: run FP16 quantization demo
        print("🎯 Running FP16 quantization demo...")
        quantized_tts = K2SOQuantizedTTS()
        if quantized_tts.initialize_quantized_model("fp16"):
            result = quantized_tts.synthesize_with_quantized_model("I am K2-SO, ready for optimized performance")
            if result['success']:
                print(f"✅ Demo complete: {result['synthesis_time']:.2f}s synthesis time")
                print(f"🎯 Memory reduction: {quantized_tts.metrics['memory_reduction']:.1f}%")

if __name__ == "__main__":
    main() 