#!/usr/bin/env python3
"""
Test Totoro Assistant with actual commands
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_assistant():
    """Test the full assistant with real commands"""
    try:
        print("🎭 Testing Totoro Assistant")
        print("=" * 40)
        
        # Import components directly
        from config import Config
        from llm.local_llm_processor import LocalLLMProcessor
        from voice import TextToSpeech
        from presence import SimplePresenceDetector
        from core import TaskExecutor
        from integrations import HomeAssistantClient
        
        print("✅ All imports successful!")
        
        # Initialize configuration
        config = Config()
        print(f"✅ Config loaded: {config.LLM_BACKEND}")
        
        # Initialize LLM processor
        llm_config = config.get_llm_config()
        if config.LLM_BACKEND == "local":
            processor = LocalLLMProcessor(
                model_name=llm_config["model_name"],
                base_url=llm_config["base_url"]
            )
            print("✅ Local LLM processor initialized")
        else:
            print(f"⚠️ Using {config.LLM_BACKEND} backend")
        
        # Initialize other components
        tts = TextToSpeech()
        presence = SimplePresenceDetector()
        task_executor = TaskExecutor()
        
        print("✅ Core components initialized")
        
        # Test command processing
        test_commands = [
            "turn on the living room lights",
            "play some jazz music",
            "set bedroom lights to 50%"
        ]
        
        print("\n🧪 Testing Commands:")
        print("-" * 30)
        
        for i, command in enumerate(test_commands, 1):
            print(f"\n{i}. Command: '{command}'")
            try:
                current_room = presence.get_current_room()
                result = processor.process_command(command, current_room)
                
                print(f"✅ Success: {result.success}")
                print(f"✅ Response: {result.response}")
                print(f"✅ Tasks: {len(result.tasks) if result.tasks else 0}")
                
                if result.tasks:
                    for task in result.tasks:
                        print(f"   - {task.action} in {task.room}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n✅ Command processing tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_assistant()) 