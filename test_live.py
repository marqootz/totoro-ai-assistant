#!/usr/bin/env python3
"""
Live test of Totoro's core LLM functionality
This tests the heart of your AI assistant!
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_live_assistant():
    """Test the core AI assistant functionality"""
    print("🎭 Totoro Live Assistant Test")
    print("=" * 50)
    
    try:
        # Import and setup
        from config import Config
        from llm.local_llm_processor import LocalLLMProcessor
        
        config = Config()
        print(f"✅ Configuration loaded")
        print(f"   Backend: {config.LLM_BACKEND}")
        print(f"   Model: {config.LOCAL_LLM_MODEL}")
        
        # Initialize processor
        llm_config = config.get_llm_config()
        processor = LocalLLMProcessor(
            model_name=llm_config["model_name"],
            base_url=llm_config["base_url"]
        )
        print(f"✅ LLM processor ready")
        
        # Interactive test
        print("\n🤖 Totoro is ready! Try these commands:")
        print("   • 'turn on the living room lights'")
        print("   • 'play some jazz music'")
        print("   • 'set bedroom lights to 30%'")
        print("   • 'turn off all lights and pause music'")
        print("   • Type 'quit' to exit")
        
        current_room = "living_room"
        
        while True:
            print(f"\n[{current_room}] > ", end="")
            command = input().strip()
            
            if command.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if command.startswith("room "):
                current_room = command[5:].strip()
                print(f"🏠 Moved to {current_room}")
                continue
            
            if command:
                try:
                    print("🤔 Thinking...")
                    result = processor.process_command(command, current_room)
                    
                    print(f"\n🗣️ Totoro: {result.response}")
                    
                    if result.success and result.tasks:
                        print(f"\n📋 Tasks to execute ({len(result.tasks)}):")
                        for i, task in enumerate(result.tasks, 1):
                            print(f"   {i}. {task.action}")
                            print(f"      Room: {task.room}")
                            if hasattr(task, 'parameters') and task.parameters:
                                print(f"      Params: {task.parameters}")
                    
                    elif not result.success:
                        print("⚠️ Command could not be processed")
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nMake sure:")
        print("1. Ollama is running: ollama serve")
        print("2. Model is available: ollama pull llama3.1:8b")
        print("3. .env file is configured with LLM_BACKEND=local")

if __name__ == "__main__":
    test_live_assistant() 