#!/usr/bin/env python3
"""
Test script for the new neural voice Totoro assistant
"""

import os
import sys
import logging

# Add src to path
sys.path.insert(0, 'src')

from src.assistant import TotoroAssistant
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_neural_voice():
    """Test the neural voice system"""
    print("🎭 Testing Neural Voice Totoro Assistant")
    print("=" * 50)
    
    try:
        # Initialize assistant
        assistant = TotoroAssistant()
        
        # Test all components
        print("\n🧪 Testing Components...")
        results = assistant.test_components()
        
        for component, status in results.items():
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {component}: {'Working' if status else 'Failed'}")
        
        # Test text commands
        print("\n💬 Testing Text Commands...")
        test_commands = [
            "What time is it?",
            "Hello, how are you?",
            "Tell me a joke",
        ]
        
        for command in test_commands:
            print(f"\n🗣️  Command: {command}")
            response = assistant.process_command(command)
            print(f"🤖 Response: {response}")
        
        # Test single wake word session
        print("\n🎤 Testing Wake Word Detection...")
        print("This will listen for a single wake word session.")
        print(f"Say '{config.WAKE_WORD}' followed by a command...")
        print("(Or press Ctrl+C to skip)")
        
        try:
            result = assistant.start_wake_word_session()
            print(f"Result: {result}")
        except KeyboardInterrupt:
            print("Skipped wake word test")
        
        print("\n✅ Neural voice test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_neural_voice() 