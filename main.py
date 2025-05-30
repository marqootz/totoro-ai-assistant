#!/usr/bin/env python3
"""
Totoro Personal Assistant
Main entry point for the voice-controlled smart home assistant
"""

import sys
import os
import argparse
import asyncio
from src.assistant import TotoroAssistant

async def main():
    parser = argparse.ArgumentParser(description="Totoro Personal Assistant")
    parser.add_argument("--test", action="store_true", help="Run in test mode (text input only)")
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
            result = await assistant.process_text_command(args.command)
            print(f"Result: {result}")
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
                        result = await assistant.process_text_command(command)
                        print(f"🤖 Totoro: {result}")
                
                except KeyboardInterrupt:
                    break
        else:
            # Normal voice mode
            print("Starting Totoro Assistant in voice mode...")
            print("Press Ctrl+C to stop")
            await assistant.start_voice_mode()
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 