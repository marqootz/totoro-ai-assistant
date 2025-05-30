#!/usr/bin/env python3
"""
Example test commands for Totoro Assistant
Run this to test various command scenarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.assistant import TotoroAssistant

def test_commands():
    """Test various command scenarios"""
    
    # Create assistant instance
    assistant = TotoroAssistant()
    
    # Test commands
    test_cases = [
        "turn on the living room lights",
        "dim the bedroom lights to 50%",
        "turn off all lights",
        "play some jazz music",
        "pause the music",
        "set volume to 70%",
        "play relaxing music in the bedroom and dim the lights",
        "turn on the kitchen lights and play cooking music",
        "good night",  # Should turn off lights and stop music
        "good morning",  # Should turn on lights and play morning music
    ]
    
    print("Testing Totoro Assistant Commands")
    print("=" * 40)
    
    for i, command in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{command}'")
        print("-" * 30)
        
        try:
            result = assistant.process_text_command(command)
            
            # Print command processing result
            cmd_result = result['command_result']
            print(f"✓ Understood: {cmd_result.success}")
            print(f"✓ Response: {cmd_result.response}")
            print(f"✓ Tasks: {len(cmd_result.tasks)}")
            
            for task in cmd_result.tasks:
                print(f"  - {task.action} on {task.target} (priority: {task.priority})")
            
            # Print execution result
            if result['execution_result']:
                exec_result = result['execution_result']
                print(f"✓ Executed: {exec_result['executed']} tasks")
                if exec_result['errors']:
                    print(f"✗ Errors: {exec_result['errors']}")
            
        except Exception as e:
            print(f"✗ Error: {e}")
        
        input("Press Enter to continue...")

if __name__ == "__main__":
    test_commands() 