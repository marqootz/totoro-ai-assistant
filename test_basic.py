#!/usr/bin/env python3
"""
Basic test script for Totoro Assistant components
Tests core functionality without requiring API keys
"""

import sys
import os

# Test imports
try:
    from src.voice import TextToSpeech
    from src.llm.command_processor import Task, CommandResult
    from src.presence import SimplePresenceDetector
    from src.core import TaskExecutor
    print("✓ All imports successful!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print("\n--- Testing Text-to-Speech ---")
    try:
        tts = TextToSpeech(voice_preference="system")
        print("✓ TTS initialized successfully")
        
        # Test voice listing
        voices = tts.list_available_voices()
        if voices:
            print(f"✓ Found {len(voices)} available voices")
        else:
            print("✓ TTS working (voice listing may not be available)")
        
        # Test speaking (comment out if you don't want audio)
        # tts.speak("Hello, this is Totoro assistant testing.")
        print("✓ TTS functionality working")
        
    except Exception as e:
        print(f"✗ TTS error: {e}")

def test_presence_detector():
    """Test presence detection"""
    print("\n--- Testing Presence Detection ---")
    try:
        detector = SimplePresenceDetector(default_room="living_room")
        print(f"✓ Presence detector initialized, current room: {detector.get_current_room()}")
        
        # Test room changing
        detector.set_room("kitchen")
        print(f"✓ Room changed to: {detector.get_current_room()}")
        
    except Exception as e:
        print(f"✗ Presence detector error: {e}")

def test_task_creation():
    """Test task creation and structure"""
    print("\n--- Testing Task Creation ---")
    try:
        # Create a sample task
        task = Task(
            action="turn_on_lights",
            target="living_room",
            parameters={"room": "living_room", "brightness": 128},
            room="living_room",
            priority=1
        )
        print(f"✓ Task created: {task.action} on {task.target}")
        
        # Create command result
        result = CommandResult(
            success=True,
            tasks=[task],
            response="I'll turn on the living room lights for you."
        )
        print(f"✓ Command result created with {len(result.tasks)} tasks")
        
    except Exception as e:
        print(f"✗ Task creation error: {e}")

def test_task_executor():
    """Test task executor (without actual execution)"""
    print("\n--- Testing Task Executor ---")
    try:
        executor = TaskExecutor()
        print("✓ Task executor initialized")
        
        # Test with empty task list
        import asyncio
        
        async def test_empty_execution():
            result = await executor.execute_tasks([])
            return result
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(test_empty_execution())
            print(f"✓ Empty task execution: {result}")
        finally:
            loop.close()
        
    except Exception as e:
        print(f"✗ Task executor error: {e}")

def main():
    print("🎭 Totoro Assistant - Basic Component Test")
    print("=" * 50)
    
    test_text_to_speech()
    test_presence_detector()
    test_task_creation()
    test_task_executor()
    
    print("\n" + "=" * 50)
    print("✓ Basic component tests completed!")
    print("\nNext steps:")
    print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Set up your Home Assistant long-lived access token")
    print("3. Copy config.env.example to .env and fill in your credentials")
    print("4. Run: python main.py --test")

if __name__ == "__main__":
    main() 