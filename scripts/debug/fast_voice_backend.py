#!/usr/bin/env python3
"""
Fast Voice Backend for Totoro Assistant
Optimized for minimum latency
"""

import time
import datetime
from src.voice.speech_recognition import VoiceRecognizer
from src.voice.text_to_speech import TextToSpeech

class FastTotoroBackend:
    """Minimal, fast voice backend"""
    
    def __init__(self):
        # Use system TTS for speed
        self.tts = TextToSpeech(voice_preference='system')
        self.voice_recognizer = VoiceRecognizer(wake_word="totoro")
        
        print("🚀 Fast Totoro backend initialized")
    
    def process_command_fast(self, command: str) -> str:
        """Process commands with minimal delay"""
        command_lower = command.lower()
        
        # Time queries (instant)
        if 'time' in command_lower:
            return datetime.datetime.now().strftime("The time is %I:%M %p")
        
        # Simple responses for common queries
        quick_responses = {
            'hello': "Hello! How can I help you?",
            'hi': "Hi there!",
            'how are you': "I'm doing great, thanks for asking!",
            'weather': "I'd be happy to help with weather information.",
            'music': "Sure, I can help with music playback.",
            'lights': "I'll help you control the lights.",
            'thank you': "You're welcome!",
            'thanks': "Happy to help!"
        }
        
        for keyword, response in quick_responses.items():
            if keyword in command_lower:
                return response
        
        # Default response
        return "I heard you say: " + command
    
    def start_fast_voice_mode(self):
        """Start optimized voice interaction"""
        print("🎤 Starting fast voice mode...")
        print("Say 'totoro' followed by your command")
        
        while True:
            try:
                # Listen for wake word (faster timeout)
                if self.voice_recognizer.listen_for_wake_word(timeout=10):
                    start_time = time.time()
                    
                    # Get command (shorter timeout)
                    command = self.voice_recognizer.listen_for_command(timeout=5)
                    
                    if command:
                        # Process quickly
                        response = self.process_command_fast(command)
                        
                        # Speak response
                        self.tts.speak(response)
                        
                        # Show timing
                        total_time = time.time() - start_time
                        print(f"⚡ Response time: {total_time:.1f}s")
                    else:
                        self.tts.speak("I didn't catch that.")
                        
            except KeyboardInterrupt:
                print("\nFast voice mode stopped")
                break

if __name__ == "__main__":
    backend = FastTotoroBackend()
    backend.start_fast_voice_mode()
