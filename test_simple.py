#!/usr/bin/env python3
"""
Simple test for Totoro Assistant components
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("🧪 Simple Totoro Test")
    print("=" * 40)
    
    # Test configuration loading
    print("1. Testing configuration...")
    from config import Config
    config = Config()
    print(f"✅ Config loaded: LLM backend = {config.LLM_BACKEND}")
    print(f"✅ LLM config: {config.get_llm_config()}")
    
    # Test LLM processor initialization
    print("\n2. Testing LLM processor...")
    if config.LLM_BACKEND == "local":
        from llm.local_llm_processor import LocalLLMProcessor
        llm_config = config.get_llm_config()
        processor = LocalLLMProcessor(
            model_name=llm_config["model_name"],
            base_url=llm_config["base_url"]
        )
        print("✅ Local LLM processor initialized")
        
        # Test a simple command
        print("\n3. Testing command processing...")
        result = processor.process_command("turn on the lights", "living_room")
        print(f"✅ Command processed: {result.success}")
        print(f"✅ Response: {result.response}")
        print(f"✅ Tasks: {len(result.tasks) if result.tasks else 0}")
        
    elif config.LLM_BACKEND == "openai":
        from llm.command_processor import CommandProcessor
        llm_config = config.get_llm_config()
        processor = CommandProcessor(
            api_key=llm_config["api_key"],
            model=llm_config["model"]
        )
        print("✅ OpenAI processor initialized")
    
    print("\n✅ Simple test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 