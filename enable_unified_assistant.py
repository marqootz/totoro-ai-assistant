#!/usr/bin/env python3
"""
Enable Unified Totoro Assistant
Script to enable and test the unified assistant combining smart home + general AI
"""

import os
import sys
import subprocess
from pathlib import Path

def update_env_file():
    """Update .env file to use unified backend"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("# Unified Totoro Assistant Configuration\n")
            f.write("LLM_BACKEND=unified\n")
            f.write("LOCAL_LLM_MODEL=llama3.1:8b\n")
            f.write("LOCAL_LLM_URL=http://localhost:11434\n")
            f.write("\n# Add your other configuration here\n")
            f.write("# HOME_ASSISTANT_URL=http://localhost:8123\n")
            f.write("# HOME_ASSISTANT_TOKEN=your_token_here\n")
        print("✅ Created .env file with unified backend")
    else:
        # Read existing file
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update LLM_BACKEND
        if "LLM_BACKEND=" in content:
            # Replace existing
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("LLM_BACKEND="):
                    lines[i] = "LLM_BACKEND=unified"
                    break
            content = '\n'.join(lines)
        else:
            # Add new
            content = "LLM_BACKEND=unified\n" + content
        
        # Ensure model is set
        if "LOCAL_LLM_MODEL=" not in content:
            content += "\nLOCAL_LLM_MODEL=llama3.1:8b"
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated .env file to use unified backend")

def check_ollama():
    """Check if Ollama is running and has the required model"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models = result.stdout
            if "llama3.1:8b" in models or "llama3.1" in models:
                print("✅ Ollama is running with llama3.1 model")
                return True
            else:
                print("⚠️  Ollama is running but llama3.1:8b model not found")
                print("   Run: ollama pull llama3.1:8b")
                return False
        else:
            print("❌ Ollama is not responding")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
        return False
    except FileNotFoundError:
        print("❌ Ollama not found. Install it first:")
        print("   brew install ollama  # macOS")
        print("   Then: ollama pull llama3.1:8b")
        return False

def run_test():
    """Run the unified assistant test"""
    print("\n🧪 Running unified assistant test...")
    try:
        result = subprocess.run([sys.executable, "test_unified_assistant.py"], 
                               capture_output=False, text=True, timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def run_interactive_test():
    """Run interactive test mode"""
    print("\n🎮 Starting interactive test mode...")
    print("   You can now test commands like:")
    print("   - Turn on the living room lights")
    print("   - What time is it?")
    print("   - Play jazz music and what's the weather?")
    print("   - Calculate 15 * 23")
    print("\n   Type 'quit' to exit\n")
    
    try:
        subprocess.run([sys.executable, "main.py", "--test"], timeout=300)
    except KeyboardInterrupt:
        print("\n👋 Interactive test ended")
    except Exception as e:
        print(f"❌ Interactive test failed: {e}")

def main():
    """Main setup function"""
    print("🦙 TOTORO UNIFIED ASSISTANT SETUP")
    print("🏠 Smart Home Excellence + 🤖 General AI Capabilities")
    print("=" * 60)
    
    # Step 1: Update configuration
    print("\n1️⃣ Updating configuration...")
    update_env_file()
    
    # Step 2: Check Ollama
    print("\n2️⃣ Checking Ollama setup...")
    ollama_ok = check_ollama()
    
    if not ollama_ok:
        print("\n⚠️  Please fix Ollama setup first:")
        print("   1. Install Ollama: brew install ollama")
        print("   2. Start service: brew services start ollama")
        print("   3. Pull model: ollama pull llama3.1:8b")
        print("   4. Run this script again")
        return
    
    # Step 3: Run tests
    print("\n3️⃣ Testing unified capabilities...")
    test_ok = run_test()
    
    if test_ok:
        print("\n✅ UNIFIED ASSISTANT ENABLED SUCCESSFULLY!")
        print("=" * 50)
        print("🎉 Your Totoro assistant now has:")
        print("   🏠 Perfect smart home control")
        print("   🤖 General AI capabilities")
        print("   🔀 Natural hybrid commands")
        print("   💬 Conversational context")
        print("   ⚡ Zero ongoing costs")
        print("   🔒 Complete privacy")
        
        print("\n🔧 IMPORTANT: To use the unified assistant immediately:")
        print("   export LLM_BACKEND=unified")
        print("   # Then run any of the commands below")
        
        # Offer interactive test
        response = input("\n🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n⚠️  Setting environment variable for this session...")
            os.environ['LLM_BACKEND'] = 'unified'
            run_interactive_test()
        
        print("\n🚀 To use your unified assistant:")
        print("   # Set environment variable first:")
        print("   export LLM_BACKEND=unified")
        print("   ")
        print("   # Then use these commands:")
        print("   python main.py --test")
        print("   python main.py")
        print("   python main.py --command 'turn on lights and what time is it'")
        print("   ")
        print("   # Or restart your terminal and the .env file will load automatically")
        
    else:
        print("\n❌ Test failed. Please check your setup.")

if __name__ == "__main__":
    main() 