#!/usr/bin/env python3
"""
Test script for local LLM functionality
Tests the local LLM processors without requiring full Totoro setup
"""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_local_llm_processor():
    """Test LocalLLMProcessor"""
    print("\n--- Testing Local LLM Processor (Ollama) ---")
    
    try:
        from llm.local_llm_processor import LocalLLMProcessor
        
        # Test initialization (will warn if Ollama not running)
        processor = LocalLLMProcessor(model_name="llama3.2")
        print("✓ LocalLLMProcessor initialized")
        
        # Test available actions
        actions = processor.get_available_actions()
        print(f"✓ Available actions: {list(actions.keys())}")
        
        # Test command processing (will fail gracefully if no Ollama)
        try:
            result = processor.process_command("turn on the living room lights")
            print(f"✓ Command processing works: {result.success}")
            if result.success:
                print(f"  Response: {result.response}")
                print(f"  Tasks: {len(result.tasks)}")
        except Exception as e:
            print(f"⚠ Command processing failed (expected if Ollama not running): {e}")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_huggingface_processor():
    """Test HuggingFaceLLMProcessor"""
    print("\n--- Testing Hugging Face Processor ---")
    
    try:
        from llm.local_llm_processor import HuggingFaceLLMProcessor
        
        print("⚠ Note: This will download a model if not cached (~345MB)")
        response = input("Continue with Hugging Face test? (y/N): ")
        
        if response.lower() != 'y':
            print("⏭ Skipping Hugging Face test")
            return
        
        # Test initialization
        processor = HuggingFaceLLMProcessor()
        print("✓ HuggingFaceLLMProcessor initialized")
        
        # Test command processing
        result = processor.process_command("turn on the living room lights")
        print(f"✓ Command processing: {result.success}")
        if result.success:
            print(f"  Response: {result.response}")
            print(f"  Tasks: {len(result.tasks)}")
        
    except ImportError as e:
        print(f"⚠ Hugging Face transformers not installed: {e}")
        print("  Install with: pip install transformers torch")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_configuration():
    """Test configuration for different backends"""
    print("\n--- Testing Configuration ---")
    
    try:
        from config import Config
        
        # Test different backends
        backends = ["openai", "local", "huggingface"]
        
        for backend in backends:
            os.environ["LLM_BACKEND"] = backend
            
            # Reload config
            import importlib
            import config
            importlib.reload(config)
            
            test_config = config.Config()
            llm_config = test_config.get_llm_config()
            
            print(f"✓ {backend} backend config: {list(llm_config.keys())}")
        
        # Reset to default
        os.environ["LLM_BACKEND"] = "openai"
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")

def test_mock_integration():
    """Test integration with mock data"""
    print("\n--- Testing Mock Integration ---")
    
    try:
        from llm.local_llm_processor import LocalLLMProcessor
        
        processor = LocalLLMProcessor()
        
        # Test various commands
        test_commands = [
            "turn on the living room lights",
            "play some jazz music",
            "turn off all lights",
            "set bedroom lights to 50%",
            "pause the music"
        ]
        
        for command in test_commands:
            try:
                result = processor.process_command(command, current_room="living_room")
                print(f"✓ '{command}' -> {result.success} ({len(result.tasks)} tasks)")
            except Exception as e:
                print(f"⚠ '{command}' -> Error: {e}")
        
    except Exception as e:
        print(f"✗ Mock integration error: {e}")

def check_ollama_status():
    """Check if Ollama is running"""
    print("\n--- Checking Ollama Status ---")
    
    try:
        import requests
        
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models")
            for model in models[:3]:  # Show first 3 models
                print(f"  - {model.get('name', 'Unknown')}")
            if len(models) > 3:
                print(f"  ... and {len(models) - 3} more")
        else:
            print(f"⚠ Ollama responded with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running")
        print("   Start with: ollama serve")
        print("   Install from: https://ollama.ai")
    except Exception as e:
        print(f"⚠ Error checking Ollama: {e}")

def main():
    print("🎭 Totoro Local LLM Test Suite")
    print("=" * 50)
    
    check_ollama_status()
    test_configuration()
    test_local_llm_processor()
    test_huggingface_processor()
    test_mock_integration()
    
    print("\n" + "=" * 50)
    print("✅ Local LLM tests completed!")
    print("\nNext steps:")
    print("1. Install Ollama: https://ollama.ai")
    print("2. Run: ollama pull llama3.2")
    print("3. Run: ollama serve")
    print("4. Set LLM_BACKEND=local in your .env file")
    print("5. Test with: python main.py --command 'turn on the lights'")

if __name__ == "__main__":
    main() 