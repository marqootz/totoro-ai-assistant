#!/usr/bin/env python3
"""
Test script for Unified Totoro Assistant
Demonstrates both smart home excellence and general AI capabilities
"""

import asyncio
import json
from src.llm.unified_processor import UnifiedLLMProcessor

def test_analysis():
    """Test the input analysis system"""
    processor = UnifiedLLMProcessor()
    
    test_cases = [
        "Turn on the lights",
        "What time is it?", 
        "Play jazz music and what's the weather?",
        "Calculate 15 * 23",
        "Turn on bedroom lights and search for news",
        "Dim the lights to 30%",
        "How much is 45 + 67?",
        "Play classical music and what time is it?"
    ]
    
    print("🔍 INPUT ANALYSIS TEST")
    print("=" * 50)
    
    for command in test_cases:
        analysis = processor._analyze_input(command)
        print(f"\nCommand: '{command}'")
        print(f"  Smart Home: {analysis['has_smart_home_commands']}")
        print(f"  General AI: {analysis['has_general_queries']}")
        print(f"  Hybrid: {analysis['is_hybrid']}")
        print(f"  Complexity: {analysis['complexity']}")

async def test_smart_home_commands():
    """Test smart home command processing"""
    processor = UnifiedLLMProcessor()
    
    smart_home_commands = [
        "Turn on the living room lights",
        "Play jazz music",
        "Set bedroom lights to 50%",
        "Turn off all lights", 
        "Play classical music and dim bedroom lights to 30%"
    ]
    
    print("\n🏠 SMART HOME COMMANDS TEST")
    print("=" * 50)
    
    for command in smart_home_commands:
        print(f"\nTesting: '{command}'")
        try:
            result = await processor.process_unified_command(command, {"current_room": "living_room"})
            
            print(f"✅ Success: {result.success}")
            print(f"📝 Response: {result.response}")
            print(f"📋 Tasks: {len(result.tasks) if result.tasks else 0}")
            
            if result.tasks:
                for i, task in enumerate(result.tasks, 1):
                    print(f"   Task {i}: {task.action} -> {task.target}")
                    if task.parameters:
                        print(f"     Parameters: {task.parameters}")
            
            if result.tool_calls:
                print(f"🔧 Tool Calls: {[call['tool'] for call in result.tool_calls]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_general_ai_capabilities():
    """Test general AI capabilities"""
    processor = UnifiedLLMProcessor()
    
    general_queries = [
        "What time is it?",
        "Calculate 15 * 23 + 45",
        "What's the weather in New York?",
        "Search for latest AI news"
    ]
    
    print("\n🤖 GENERAL AI CAPABILITIES TEST")
    print("=" * 50)
    
    for query in general_queries:
        print(f"\nTesting: '{query}'")
        try:
            result = await processor.process_unified_command(query)
            
            print(f"✅ Success: {result.success}")
            print(f"📝 Response: {result.response}")
            
            if result.tool_calls:
                print(f"🔧 Tools Used: {[call['tool'] for call in result.tool_calls]}")
                
            if result.tool_results:
                for tool, tool_result in result.tool_results.items():
                    print(f"   {tool}: {tool_result}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_hybrid_commands():
    """Test hybrid commands that combine both capabilities"""
    processor = UnifiedLLMProcessor()
    
    hybrid_commands = [
        "Turn on the lights and what time is it?",
        "Play music and calculate 20 * 30",
        "Dim bedroom lights to 25% and what's the weather?",
        "Set living room temperature to 72 and search for energy tips"
    ]
    
    print("\n🔀 HYBRID COMMANDS TEST")
    print("=" * 50)
    
    for command in hybrid_commands:
        print(f"\nTesting: '{command}'")
        try:
            result = await processor.process_unified_command(command, {"current_room": "bedroom"})
            
            print(f"✅ Success: {result.success}")
            print(f"📝 Response: {result.response}")
            
            if result.tasks:
                print(f"🏠 Smart Home Tasks: {len(result.tasks)}")
                for i, task in enumerate(result.tasks, 1):
                    print(f"   Task {i}: {task.action} -> {task.target}")
            
            if result.tool_calls:
                print(f"🔧 General AI Tools: {[call['tool'] for call in result.tool_calls]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_conversation_flow():
    """Test conversation flow and context"""
    processor = UnifiedLLMProcessor()
    
    conversation = [
        "Turn on the bedroom lights",
        "Now dim them to 40%", 
        "What time is it?",
        "Play some relaxing music",
        "Calculate how much 8 hours of 60 watts is in kilowatt-hours"
    ]
    
    print("\n💬 CONVERSATION FLOW TEST")
    print("=" * 50)
    
    for i, message in enumerate(conversation, 1):
        print(f"\nTurn {i}: '{message}'")
        try:
            result = await processor.process_unified_command(message, {"current_room": "bedroom"})
            
            print(f"📝 Totoro: {result.response}")
            
            if result.tasks:
                print(f"🏠 Executed {len(result.tasks)} smart home task(s)")
            
            if result.tool_calls:
                print(f"🔧 Used tools: {[call['tool'] for call in result.tool_calls]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print(f"📚 Conversation Length: {len(processor.conversation_history)}")

def test_compatibility():
    """Test compatibility with existing CommandResult interface"""
    processor = UnifiedLLMProcessor()
    
    print("\n🔄 COMPATIBILITY TEST")
    print("=" * 50)
    
    test_commands = [
        "Turn on living room lights",
        "What time is it?",
        "Play jazz and dim lights to 50%"
    ]
    
    for command in test_commands:
        print(f"\nTesting compatibility: '{command}'")
        try:
            # Test the process_command method (sync interface)
            result = processor.process_command(command, "living_room")
            
            print(f"✅ Success: {result.success}")
            print(f"📝 Response: {result.response}")
            print(f"📋 Tasks: {len(result.tasks)}")
            print(f"❌ Error: {result.error}")
            
        except Exception as e:
            print(f"❌ Compatibility Error: {e}")

async def main():
    """Run all tests"""
    print("🦙 TOTORO UNIFIED ASSISTANT TEST SUITE")
    print("🏠 Smart Home Excellence + 🤖 General AI Capabilities")
    print("=" * 70)
    
    # Test input analysis
    test_analysis()
    
    # Test individual capabilities
    await test_smart_home_commands()
    await test_general_ai_capabilities()
    
    # Test hybrid functionality
    await test_hybrid_commands()
    
    # Test conversation flow
    await test_conversation_flow()
    
    # Test compatibility
    test_compatibility()
    
    print("\n🎉 UNIFIED ASSISTANT TEST COMPLETE!")
    print("=" * 50)
    print("✨ Your Totoro assistant now combines:")
    print("   🏠 Perfect smart home control (JSON-based)")
    print("   🤖 General AI capabilities (tool-based)")
    print("   🔀 Natural hybrid commands")
    print("   💬 Conversational context")
    print("   ⚡ Zero ongoing costs")
    print("   🔒 Complete privacy")

if __name__ == "__main__":
    asyncio.run(main()) 