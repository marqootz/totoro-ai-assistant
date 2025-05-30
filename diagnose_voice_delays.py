#!/usr/bin/env python3
"""
Voice Delay Diagnostic Tool for Totoro Assistant
Identifies bottlenecks in the voice processing pipeline
"""

import time
import logging
from src.voice.speech_recognition import VoiceRecognizer
from src.voice.text_to_speech import TextToSpeech
from src.assistant import TotoroAssistant
import config

# Set up logging to track timing
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

class VoiceDelayDiagnostic:
    def __init__(self):
        self.timings = {}
        
    def time_operation(self, operation_name, func, *args, **kwargs):
        """Time an operation and log results"""
        start_time = time.time()
        logger.info(f"🕐 Starting: {operation_name}")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            self.timings[operation_name] = duration
            logger.info(f"✅ Completed: {operation_name} in {duration:.2f}s")
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f"❌ Failed: {operation_name} after {duration:.2f}s - {e}")
            self.timings[operation_name] = duration
            return None
    
    def diagnose_initialization_delays(self):
        """Diagnose delays in component initialization"""
        print("🔍 DIAGNOSING INITIALIZATION DELAYS")
        print("=" * 50)
        
        # Test TTS initialization
        def init_tts_chatterbox():
            return TextToSpeech(voice_preference='chatterbox')
        
        def init_tts_system():
            return TextToSpeech(voice_preference='system')
        
        def init_voice_recognizer():
            return VoiceRecognizer(wake_word=config.WAKE_WORD)
        
        def init_assistant():
            return TotoroAssistant()
        
        # Time each initialization
        tts_chatterbox = self.time_operation("TTS (Chatterbox) Init", init_tts_chatterbox)
        tts_system = self.time_operation("TTS (System) Init", init_tts_system) 
        voice_recognizer = self.time_operation("Voice Recognition Init", init_voice_recognizer)
        assistant = self.time_operation("Assistant Init", init_assistant)
        
        return {
            'tts_chatterbox': tts_chatterbox,
            'tts_system': tts_system,
            'voice_recognizer': voice_recognizer,
            'assistant': assistant
        }
    
    def diagnose_speech_recognition_delays(self, voice_recognizer):
        """Diagnose delays in speech recognition"""
        print("\n🎤 DIAGNOSING SPEECH RECOGNITION DELAYS")
        print("=" * 50)
        
        if not voice_recognizer:
            print("❌ Voice recognizer not available")
            return
        
        # Test ambient noise adjustment
        def adjust_ambient_noise():
            if voice_recognizer.microphone:
                with voice_recognizer.microphone as source:
                    voice_recognizer.recognizer.adjust_for_ambient_noise(source, duration=1)
                return True
            return False
        
        self.time_operation("Ambient Noise Adjustment", adjust_ambient_noise)
        
        # Test speech recognition (manual test)
        print("\n🗣️ Manual Speech Recognition Test:")
        print("   Say something when prompted...")
        print("   This will measure: Audio Capture + Speech-to-Text")
        
        def test_recognition():
            return voice_recognizer.listen_for_command(timeout=5)
        
        command = self.time_operation("Speech Recognition (5s timeout)", test_recognition)
        
        if command:
            print(f"✅ Recognized: '{command}'")
        else:
            print("⚠️ No speech recognized")
    
    def diagnose_tts_delays(self, tts_chatterbox, tts_system):
        """Diagnose delays in text-to-speech"""
        print("\n🗣️ DIAGNOSING TTS DELAYS")  
        print("=" * 50)
        
        test_text = "Hello! This is a test of speech synthesis speed."
        
        # Test Chatterbox TTS
        if tts_chatterbox and tts_chatterbox.chatterbox_model:
            def test_chatterbox():
                return tts_chatterbox._speak_chatterbox(test_text)
            
            self.time_operation("Chatterbox TTS Generation", test_chatterbox)
        else:
            print("⚠️ Chatterbox TTS not available")
        
        # Test System TTS
        if tts_system and tts_system.tts_engine:
            def test_system_tts():
                return tts_system._speak_pyttsx3(test_text)
            
            self.time_operation("System TTS Generation", test_system_tts)
        else:
            print("⚠️ System TTS not available")
    
    def diagnose_llm_processing_delays(self, assistant):
        """Diagnose delays in LLM processing"""
        print("\n🧠 DIAGNOSING LLM PROCESSING DELAYS")
        print("=" * 50)
        
        if not assistant:
            print("❌ Assistant not available")
            return
        
        test_commands = [
            "what time is it",
            "turn on the lights", 
            "tell me a joke"
        ]
        
        for command in test_commands:
            def process_command():
                return assistant.process_command(command)
            
            response = self.time_operation(f"LLM Processing: '{command}'", process_command)
            if response:
                print(f"   Response: {response[:100]}...")
    
    def diagnose_full_voice_cycle(self, assistant):
        """Diagnose full voice interaction cycle"""
        print("\n🔄 DIAGNOSING FULL VOICE CYCLE")
        print("=" * 50)
        
        if not assistant:
            print("❌ Assistant not available")
            return
        
        print(f"🎯 Say '{config.WAKE_WORD}' followed by a command...")
        print("   This will measure the complete cycle:")
        print("   Wake Word → Command Recognition → Processing → TTS Response")
        
        def full_voice_cycle():
            return assistant.start_wake_word_session()
        
        result = self.time_operation("Complete Voice Cycle", full_voice_cycle)
        return result
    
    def analyze_bottlenecks(self):
        """Analyze timing results to identify bottlenecks"""
        print("\n📊 BOTTLENECK ANALYSIS")
        print("=" * 50)
        
        if not self.timings:
            print("❌ No timing data available")
            return
        
        # Sort by time (longest first)
        sorted_timings = sorted(self.timings.items(), key=lambda x: x[1], reverse=True)
        
        print("⏰ Processing Times (slowest first):")
        for operation, duration in sorted_timings:
            if duration > 5.0:
                emoji = "🚨"  # Very slow
            elif duration > 2.0:
                emoji = "⚠️"   # Slow
            elif duration > 1.0:
                emoji = "⏳"   # Moderate
            else:
                emoji = "✅"   # Fast
                
            print(f"   {emoji} {operation}: {duration:.2f}s")
        
        # Identify primary bottleneck
        if sorted_timings:
            slowest_operation, slowest_time = sorted_timings[0]
            print(f"\n🎯 PRIMARY BOTTLENECK: {slowest_operation} ({slowest_time:.2f}s)")
            
            # Provide specific recommendations
            self.provide_recommendations(slowest_operation, slowest_time)
    
    def provide_recommendations(self, bottleneck_operation, duration):
        """Provide specific recommendations based on bottleneck"""
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        print("=" * 50)
        
        if "Chatterbox TTS" in bottleneck_operation:
            print("🎤 CHATTERBOX TTS OPTIMIZATION:")
            print("   • Neural TTS is compute-intensive")
            print("   • Consider switching to System TTS for faster response")
            print("   • GPU acceleration would help (if available)")
            print("   • Reduce CHATTERBOX_CFG_WEIGHT for faster generation")
            print("   • Use shorter responses where possible")
            
        elif "System TTS" in bottleneck_operation:
            print("🔊 SYSTEM TTS OPTIMIZATION:")
            print("   • System TTS should be fast - check audio drivers")
            print("   • Verify no audio conflicts (close Spotify, Music, etc.)")
            print("   • Try different voice (some are faster than others)")
            
        elif "Speech Recognition" in bottleneck_operation:
            print("🎤 SPEECH RECOGNITION OPTIMIZATION:")
            print("   • Uses Google Cloud Speech - check internet speed")
            print("   • Reduce timeout values for faster failure detection")
            print("   • Use cleaner microphone input (noise reduction)")
            print("   • Consider offline speech recognition for privacy")
            
        elif "LLM Processing" in bottleneck_operation:
            print("🧠 LLM PROCESSING OPTIMIZATION:")
            print("   • Check which LLM backend is active")
            print("   • Local LLMs may be slower but more private")
            print("   • OpenAI API is faster but requires internet")
            print("   • Consider model size vs. speed tradeoffs")
            
        elif "Assistant Init" in bottleneck_operation:
            print("🚀 INITIALIZATION OPTIMIZATION:")
            print("   • Keep assistant running in background")
            print("   • Pre-load neural models at startup")
            print("   • Consider lazy loading of non-essential components")
        
        print(f"\n⚡ IMMEDIATE FIXES:")
        if duration > 10:
            print("   🚨 CRITICAL: >10s delay - major performance issue")
            print("   • Switch to 'system' TTS preference")
            print("   • Check system resources (CPU, memory)")
            print("   • Close resource-heavy applications")
        elif duration > 5:
            print("   ⚠️ HIGH: >5s delay - noticeable lag")
            print("   • Optimize the slowest component")
            print("   • Consider hardware upgrades")
        else:
            print("   ✅ ACCEPTABLE: <5s total processing time")

def main():
    print("🕵️ TOTORO VOICE DELAY DIAGNOSTIC")
    print("=" * 60)
    print("This tool will identify bottlenecks in voice processing.")
    print("You'll be asked to speak during some tests.")
    print("")
    
    diagnostic = VoiceDelayDiagnostic()
    
    # Run comprehensive diagnostics
    components = diagnostic.diagnose_initialization_delays()
    
    if components['voice_recognizer']:
        diagnostic.diagnose_speech_recognition_delays(components['voice_recognizer'])
    
    diagnostic.diagnose_tts_delays(components['tts_chatterbox'], components['tts_system'])
    
    if components['assistant']:
        diagnostic.diagnose_llm_processing_delays(components['assistant'])
        
        # Optional full cycle test
        print(f"\n🎮 OPTIONAL: Full voice cycle test")
        print("Press Enter to test complete voice interaction, or Ctrl+C to skip...")
        try:
            input()
            diagnostic.diagnose_full_voice_cycle(components['assistant'])
        except KeyboardInterrupt:
            print("⏭️ Skipped full cycle test")
    
    # Analyze results
    diagnostic.analyze_bottlenecks()
    
    print(f"\n🎯 SUMMARY: Voice processing analysis complete!")
    print("Check the recommendations above to optimize performance.")

if __name__ == "__main__":
    main() 