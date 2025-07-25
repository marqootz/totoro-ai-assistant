#!/usr/bin/env python3
"""
Design for Unified Totoro Assistant
Combines smart home excellence with general AI capabilities
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class UnifiedTotoroProcessor:
    """
    Unified LLM processor that handles both smart home commands 
    and general AI capabilities in one system
    """
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        self.conversation_history = []
        
        # Unified tool registry - combines smart home + general tools
        self.tools = {
            # Smart Home Tools (high reliability)
            "turn_on_lights": {
                "description": "Turn on lights in specified room",
                "parameters": ["room", "brightness"],
                "category": "smart_home",
                "requires_json": True,
                "function": self._turn_on_lights
            },
            "play_music": {
                "description": "Play music with specified query/genre",
                "parameters": ["query", "type"],
                "category": "smart_home", 
                "requires_json": True,
                "function": self._play_music
            },
            "set_temperature": {
                "description": "Set temperature in room",
                "parameters": ["room", "temperature"],
                "category": "smart_home",
                "requires_json": True,
                "function": self._set_temperature
            },
            
            # General AI Tools (flexible)
            "web_search": {
                "description": "Search the web for current information",
                "parameters": ["query"],
                "category": "general",
                "requires_json": False,
                "function": self._web_search
            },
            "get_time": {
                "description": "Get current date and time",
                "parameters": [],
                "category": "general",
                "requires_json": False,
                "function": self._get_time
            },
            "calculate": {
                "description": "Perform mathematical calculations",
                "parameters": ["expression"],
                "category": "general",
                "requires_json": False,
                "function": self._calculate
            },
            "get_weather": {
                "description": "Get weather for specified location",
                "parameters": ["location"],
                "category": "general",
                "requires_json": False,
                "function": self._get_weather
            }
        }
    
    async def process_unified_command(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process any command - smart home or general AI
        Uses intelligent routing and hybrid response format
        """
        try:
            # Analyze input to determine response strategy
            analysis = self._analyze_input(user_input)
            
            # Create appropriate system prompt
            system_prompt = self._create_unified_system_prompt(analysis, context)
            
            # Get LLM response
            llm_response = await self._call_unified_llm(system_prompt, user_input)
            
            # Parse response based on analysis
            if analysis["has_smart_home_commands"]:
                # Smart home: require JSON + extract tasks
                result = self._parse_smart_home_response(llm_response, user_input)
            else:
                # General AI: natural response + tool extraction
                result = await self._parse_general_response(llm_response, user_input)
            
            # Add to conversation history
            self._update_conversation_history(user_input, result)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "response": f"I encountered an error: {str(e)}",
                "error": str(e)
            }
    
    def _analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze input to determine appropriate processing strategy"""
        smart_home_keywords = [
            "lights", "music", "temperature", "volume", "brightness",
            "play", "pause", "turn on", "turn off", "set", "dim", "brighten"
        ]
        
        general_ai_keywords = [
            "time", "weather", "calculate", "math", "search", "what is",
            "how to", "explain", "tell me about"
        ]
        
        text_lower = user_input.lower()
        
        has_smart_home = any(keyword in text_lower for keyword in smart_home_keywords)
        has_general = any(keyword in text_lower for keyword in general_ai_keywords)
        
        return {
            "has_smart_home_commands": has_smart_home,
            "has_general_queries": has_general,
            "is_hybrid": has_smart_home and has_general,
            "complexity": "high" if has_smart_home and has_general else "standard"
        }
    
    def _create_unified_system_prompt(self, analysis: Dict[str, Any], context: Optional[Dict] = None) -> str:
        """Create a unified system prompt that handles both capabilities"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Smart home tools (require JSON)
        smart_home_tools = {k: v for k, v in self.tools.items() if v["category"] == "smart_home"}
        # General tools (flexible format)
        general_tools = {k: v for k, v in self.tools.items() if v["category"] == "general"}
        
        if analysis["has_smart_home_commands"]:
            # Include JSON format requirement
            json_format = """
IMPORTANT: For smart home commands, you MUST include a JSON section like this:

SMART_HOME_JSON:
{
  "tasks": [
    {
      "action": "turn_on_lights",
      "room": "living_room", 
      "parameters": {"brightness": 128}
    }
  ],
  "success": true
}

You can include natural conversation before or after the JSON.
"""
        else:
            json_format = ""
        
        return f"""You are Totoro, an intelligent AI assistant with both smart home control and general AI capabilities.

Current time: {current_time}

SMART HOME CAPABILITIES:
{self._format_tools_description(smart_home_tools)}

GENERAL AI CAPABILITIES:  
{self._format_tools_description(general_tools)}

{json_format}

EXAMPLES:

User: "Turn on the living room lights and what time is it?"
Response: "I'll turn on the living room lights for you! The current time is {current_time}."

SMART_HOME_JSON:
{{"tasks": [{{"action": "turn_on_lights", "room": "living_room", "parameters": {{"brightness": 255}}}}], "success": true}}

TOOL_CALL: get_time()

User: "What's 15 * 23?"
Response: "Let me calculate that for you."
TOOL_CALL: calculate(expression="15 * 23")

User: "Play jazz music"
Response: "I'll play some jazz music for you."
SMART_HOME_JSON:
{{"tasks": [{{"action": "play_music", "parameters": {{"query": "jazz", "type": "genre"}}}}], "success": true}}

Instructions:
1. Handle both smart home and general queries in the same conversation
2. For smart home commands: Always include SMART_HOME_JSON section
3. For general queries: Use TOOL_CALL format when needed
4. Be conversational and helpful
5. You can combine both capabilities in one response
"""
    
    def _format_tools_description(self, tools: Dict) -> str:
        """Format tools for the system prompt"""
        return "\n".join([
            f"- {name}: {info['description']} (parameters: {', '.join(info['parameters']) if info['parameters'] else 'none'})"
            for name, info in tools.items()
        ])
    
    async def _call_unified_llm(self, system_prompt: str, user_input: str) -> str:
        """Call the LLM with unified prompting"""
        # Implementation would be similar to existing LLM calls
        # but with the unified prompt
        pass
    
    def _parse_smart_home_response(self, response: str, original_command: str) -> Dict[str, Any]:
        """Parse smart home JSON from response while preserving conversational text"""
        import re
        
        # Extract JSON section
        json_pattern = r'SMART_HOME_JSON:\s*(\{.*?\})'
        json_match = re.search(json_pattern, response, re.DOTALL)
        
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                tasks = json_data.get("tasks", [])
                
                # Extract conversational text (everything except JSON)
                conversational_text = re.sub(json_pattern, "", response, flags=re.DOTALL).strip()
                
                return {
                    "success": True,
                    "response": conversational_text,
                    "tasks": tasks,
                    "type": "smart_home"
                }
            except json.JSONDecodeError:
                pass
        
        # Fallback to natural language parsing
        return {
            "success": False,
            "response": response,
            "tasks": [],
            "type": "smart_home"
        }
    
    async def _parse_general_response(self, response: str, original_command: str) -> Dict[str, Any]:
        """Parse general AI response with tool calls"""
        import re
        
        # Extract tool calls
        tool_pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        tool_matches = re.findall(tool_pattern, response)
        
        tool_calls = []
        for tool_name, params_str in tool_matches:
            if tool_name in self.tools:
                # Parse parameters
                params = {}
                if params_str.strip():
                    param_pairs = re.findall(r'(\w+)="([^"]*)"', params_str)
                    params = dict(param_pairs)
                
                tool_calls.append({
                    "tool": tool_name,
                    "parameters": params
                })
        
        # Execute tools if any
        tool_results = {}
        if tool_calls:
            tool_results = await self._execute_tools(tool_calls)
        
        # Remove tool call syntax from response
        clean_response = re.sub(tool_pattern, "", response).strip()
        
        return {
            "success": True,
            "response": clean_response,
            "tool_calls": tool_calls,
            "tool_results": tool_results,
            "type": "general"
        }
    
    async def _execute_tools(self, tool_calls: List[Dict]) -> Dict[str, Any]:
        """Execute tool calls"""
        results = {}
        for call in tool_calls:
            tool_name = call["tool"]
            parameters = call["parameters"]
            
            if tool_name in self.tools:
                func = self.tools[tool_name]["function"]
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(**parameters)
                    else:
                        result = func(**parameters)
                    results[tool_name] = result
                except Exception as e:
                    results[tool_name] = f"Error: {str(e)}"
        
        return results
    
    def _update_conversation_history(self, user_input: str, result: Dict[str, Any]):
        """Update conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        self.conversation_history.append({
            "role": "assistant", 
            "content": result["response"],
            "type": result.get("type", "general")
        })
        
        # Keep manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    # Tool implementations would go here...
    async def _web_search(self, query: str) -> str:
        return f"Web search results for: {query}"
    
    def _get_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _calculate(self, expression: str) -> str:
        # Safe math evaluation
        return str(eval(expression))  # Simplified
    
    async def _get_weather(self, location: str) -> str:
        return f"Weather for {location}: Sunny, 72°F"
    
    def _turn_on_lights(self, room: str, brightness: int = 255):
        return f"Lights turned on in {room} at {brightness/255*100:.0f}%"
    
    def _play_music(self, query: str, type: str = "track"):
        return f"Playing {type}: {query}"
    
    def _set_temperature(self, room: str, temperature: int):
        return f"Temperature set to {temperature}°F in {room}"


# Example usage:
async def demo_unified_assistant():
    """Demonstrate unified assistant capabilities"""
    assistant = UnifiedTotoroProcessor()
    
    test_commands = [
        "Turn on the living room lights and what time is it?",
        "Play jazz music and calculate 15 * 23", 
        "What's the weather like?",
        "Set bedroom lights to 30% and search for news about AI",
        "Just turn off all lights"
    ]
    
    for command in test_commands:
        print(f"\nUser: {command}")
        result = await assistant.process_unified_command(command)
        print(f"Totoro: {result['response']}")
        
        if result.get("tasks"):
            print(f"Smart Home Tasks: {len(result['tasks'])}")
        if result.get("tool_calls"):
            print(f"General Tools Used: {[call['tool'] for call in result['tool_calls']]}")

if __name__ == "__main__":
    asyncio.run(demo_unified_assistant()) 