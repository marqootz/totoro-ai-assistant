#!/usr/bin/env python3
"""
Optimized K2-SO Voice System
Smart performance optimization based on phrase length and use case
"""

import sys
import os
import time
import threading
from typing import Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.voice.text_to_speech import TextToSpeech

class OptimizedK2SOVoice:
    def __init__(self):
        self.tts = None
        self.model_loaded = False
        self.load_start_time = None
        
        # Performance thresholds
        self.SHORT_PHRASE_WORDS = 3  # "OK", "Yes", "Got it"
        self.MEDIUM_PHRASE_WORDS = 10  # Most conversational responses
        self.LONG_PHRASE_WORDS = 20   # Longer explanations
        
        # Cached common phrases
        self.common_phrases = {
            "yes": "Yes.",
            "no": "No.",
            "ok": "OK.",
            "understood": "Understood.",
            "affirmative": "Affirmative.",
            "negative": "Negative.",
            "ready": "Ready.",
            "complete": "Complete.",
            "processing": "Processing.",
            "error": "Error detected."
        }
    
    def _lazy_init_tts(self):
        """Initialize TTS only when needed"""
        if not self.tts:
            print("🤖 Initializing K2-SO voice system...")
            self.load_start_time = time.time()
            self.tts = TextToSpeech(voice_preference="coqui")
            
            if self.tts.coqui_tts:
                load_time = time.time() - self.load_start_time
                print(f"✅ K2-SO voice ready in {load_time:.1f}s")
                self.model_loaded = True
            else:
                print("❌ Failed to load K2-SO voice system")
                return False
        return True
    
    def analyze_phrase(self, text: str) -> Dict:
        """Analyze phrase characteristics for optimization"""
        words = text.split()
        word_count = len(words)
        
        # Categorize phrase length
        if word_count <= self.SHORT_PHRASE_WORDS:
            category = "short"
            expected_time = "~2-3s"
        elif word_count <= self.MEDIUM_PHRASE_WORDS:
            category = "medium"
            expected_time = "~3-5s"
        elif word_count <= self.LONG_PHRASE_WORDS:
            category = "long"
            expected_time = "~5-8s"
        else:
            category = "very_long"
            expected_time = ">8s"
        
        # Check if it's a common phrase
        is_common = text.lower().strip('.!?') in self.common_phrases
        
        return {
            'word_count': word_count,
            'category': category,
            'expected_time': expected_time,
            'is_common': is_common,
            'use_cache': is_common and category == "short"
        }
    
    def speak_optimized(self, text: str, force_clean: bool = True) -> Dict:
        """Optimized speaking with performance analytics"""
        start_time = time.time()
        
        # Initialize TTS if needed
        if not self._lazy_init_tts():
            return {'success': False, 'error': 'TTS initialization failed'}
        
        # Analyze the phrase
        analysis = self.analyze_phrase(text)
        
        print(f"🗣️ K2-SO Speaking: '{text[:40]}{'...' if len(text) > 40 else ''}'")
        print(f"   Category: {analysis['category']} ({analysis['word_count']} words)")
        print(f"   Expected: {analysis['expected_time']}")
        
        # Choose audio source (cleaned by default for better performance)
        if force_clean and os.path.exists("assets/k2so-voice-samples-clean.mp3"):
            audio_path = "assets/k2so-voice-samples-clean.mp3"
            print("   🧹 Using cleaned audio")
        else:
            audio_path = "assets/k2so-voice-samples.mp3"
            print("   🤖 Using original audio")
        
        # Perform synthesis
        synthesis_start = time.time()
        success = self.tts.speak(text, audio_prompt_path=audio_path)
        synthesis_time = time.time() - synthesis_start
        
        total_time = time.time() - start_time
        
        # Performance metrics
        result = {
            'success': success,
            'text': text,
            'analysis': analysis,
            'synthesis_time': synthesis_time,
            'total_time': total_time,
            'audio_path': audio_path,
            'model_load_time': self.load_start_time and (time.time() - self.load_start_time) or 0
        }
        
        if success:
            print(f"✅ Synthesis completed in {synthesis_time:.2f}s (Total: {total_time:.2f}s)")
        else:
            print(f"❌ Synthesis failed after {synthesis_time:.2f}s")
        
        return result
    
    def quick_response(self, text: str) -> bool:
        """Quick response for short phrases"""
        analysis = self.analyze_phrase(text)
        if analysis['category'] == 'short':
            result = self.speak_optimized(text)
            return result['success']
        else:
            print("⚠️ Use speak_optimized() for longer phrases")
            return self.speak_optimized(text)['success']
    
    def benchmark_performance(self):
        """Benchmark different phrase types"""
        print("🏁 K2-SO VOICE PERFORMANCE BENCHMARK")
        print("=" * 50)
        
        test_cases = [
            ("OK", "short"),
            ("Affirmative", "short"),
            ("I am K2-SO", "short"),
            ("Congratulations, you are being rescued", "medium"),
            ("I have a bad feeling about this mission", "medium"),
            ("The odds of success are approximately three thousand seven hundred and twenty to one", "long")
        ]
        
        results = []
        
        for text, expected_category in test_cases:
            print(f"\n🧪 Testing: '{text}'")
            result = self.speak_optimized(text)
            
            if result['success']:
                actual_category = result['analysis']['category']
                match = "✅" if actual_category == expected_category else "⚠️"
                print(f"   {match} Category: {actual_category} (expected {expected_category})")
                print(f"   ⏱️ Time: {result['synthesis_time']:.2f}s")
                results.append(result)
            else:
                print(f"   ❌ Failed")
        
        # Summary
        if results:
            avg_time = sum(r['synthesis_time'] for r in results) / len(results)
            short_results = [r for r in results if r['analysis']['category'] == 'short']
            medium_results = [r for r in results if r['analysis']['category'] == 'medium']
            long_results = [r for r in results if r['analysis']['category'] == 'long']
            
            print(f"\n📊 PERFORMANCE SUMMARY:")
            print(f"   Overall Average: {avg_time:.2f}s")
            
            if short_results:
                short_avg = sum(r['synthesis_time'] for r in short_results) / len(short_results)
                print(f"   Short phrases: {short_avg:.2f}s avg ({len(short_results)} tests)")
            
            if medium_results:
                medium_avg = sum(r['synthesis_time'] for r in medium_results) / len(medium_results)
                print(f"   Medium phrases: {medium_avg:.2f}s avg ({len(medium_results)} tests)")
            
            if long_results:
                long_avg = sum(r['synthesis_time'] for r in long_results) / len(long_results)
                print(f"   Long phrases: {long_avg:.2f}s avg ({len(long_results)} tests)")
        
        return results

def main():
    """Main function for testing and demonstration"""
    k2so = OptimizedK2SOVoice()
    
    if len(sys.argv) > 1:
        # Command line usage
        if sys.argv[1] == "--benchmark":
            k2so.benchmark_performance()
        elif sys.argv[1] == "--quick":
            text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "OK"
            k2so.quick_response(text)
        else:
            text = " ".join(sys.argv[1:])
            k2so.speak_optimized(text)
    else:
        # Default demo
        print("🤖 K2-SO Optimized Voice Demo")
        print("Testing different phrase types...\n")
        
        demo_phrases = [
            "Affirmative",
            "I am K2-SO",
            "Congratulations, you are being rescued"
        ]
        
        for phrase in demo_phrases:
            k2so.speak_optimized(phrase)
            print()

if __name__ == "__main__":
    main() 