#!/usr/bin/env python3
"""
Totoro Personal Assistant
Main entry point for the voice-controlled smart home assistant
"""

import sys
import os
import argparse
import asyncio
import config
from src.assistant import TotoroAssistant

async def main():
    parser = argparse.ArgumentParser(description="Totoro Personal Assistant")
    parser.add_argument("--test", action="store_true", help="Run in test mode (text input only)")
    parser.add_argument("--voice", action="store_true", help="Start voice mode immediately")
    parser.add_argument("--test-voice", action="store_true", help="Test voice capabilities")
    parser.add_argument("--command", type=str, help="Execute a single command and exit")
    parser.add_argument("--room", type=str, help="Set initial room context")
    
    args = parser.parse_args()
    
    try:
        # Create assistant instance
        assistant = TotoroAssistant()
        
        # Set room if specified
        if args.room:
            assistant.presence_detector.set_current_room(args.room)
        
        if args.command:
            # Execute single command
            print(f"Executing command: {args.command}")
            result = assistant.process_command(args.command)
            print(f"Result: {result}")
            return
        
        if args.test_voice:
            # Test voice capabilities
            print("Running voice capabilities test...")
            os.system("python test_voice.py")
            return
        
        if args.test:
            # Test mode - text input only
            print("🦙 Totoro Assistant - Unified Test Mode")
            print("🏠 Smart Home + 🤖 General AI capabilities")
            print("Type commands or 'quit' to exit")
            print("\nExamples:")
            print("  - Turn on the living room lights")
            print("  - What time is it?")
            print("  - Play jazz music and what's the weather?")
            print("  - Calculate 15 * 23")
            
            while True:
                try:
                    command = input("\n> ").strip()
                    if command.lower() in ['quit', 'exit', 'bye']:
                        break
                    
                    if command:
                        result = assistant.process_command(command)
                        print(f"🤖 Totoro: {result}")
                
                except KeyboardInterrupt:
                    break
        
        elif args.voice or True:  # Default to voice mode
            # Voice mode
            print("🦙 TOTORO UNIFIED VOICE ASSISTANT")
            print("🎤 Voice Control + 🏠 Smart Home + 🤖 General AI")
            print("=" * 60)
            
            # Show capabilities
            print("\n✨ UNIFIED CAPABILITIES:")
            print("🏠 Smart Home Control:")
            print("   • Turn on/off lights in any room")
            print("   • Play music with Spotify integration") 
            print("   • Control temperature and devices")
            print("   • Room-aware context")
            
            print("\n🤖 General AI:")
            print("   • Current time and date")
            print("   • Mathematical calculations")
            print("   • Weather information")
            print("   • Natural conversations")
            
            print("\n🔀 Unified Commands (Revolutionary!):")
            print("   • 'Turn on lights and what time is it?'")
            print("   • 'Play music and calculate 20 * 30'")
            print("   • 'Dim bedroom lights and what's the weather?'")
            
            print(f"\n🎯 Wake Word: '{config.WAKE_WORD}'")
            print("📢 Example Commands:")
            print(f"   • '{config.WAKE_WORD}, what time is it?'")
            print(f"   • '{config.WAKE_WORD}, turn on the living room lights'")
            print(f"   • '{config.WAKE_WORD}, play jazz music and dim the lights'")
            
            print("\n🔧 Voice Setup:")
            print("   • Microphone: Built-in or external")
            print("   • Speech Recognition: Google Cloud Speech")
            print("   • Text-to-Speech: System voices")
            print("   • Wake Word Detection: Always listening")
            
            print("\n⏹️  Press Ctrl+C to stop")
            print("\n🚀 Starting voice mode...")
            
            assistant.start_voice_mode()
    
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Ensure microphone permissions are granted")
        print("   - Check internet connection for speech recognition")
        print("   - Test voice with: python main.py --test-voice")
        print("   - Use text mode with: python main.py --test")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 