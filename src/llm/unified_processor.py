#!/usr/bin/env python3
"""
Unified Totoro LLM Processor
Combines smart home excellence with general AI capabilities
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import aiohttp
import re
import math
from dataclasses import dataclass
from .command_processor import Task, CommandResult

logger = logging.getLogger(__name__)

@dataclass
class UnifiedResult:
    """Result from unified processing"""
    success: bool
    response: str
    tasks: List[Task] = None
    tool_calls: List[Dict] = None
    tool_results: Dict[str, Any] = None
    type: str = "unified"
    error: str = None

class UnifiedLLMProcessor:
    """
    Unified LLM processor that handles both smart home commands 
    and general AI capabilities in one system
    """
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        self.conversation_history = []
        
        # Smart home actions
        self.smart_home_actions = {
            "turn_on_lights": {
                "description": "Turn on lights in a room or specific light",
                "parameters": ["room", "brightness", "color"],
                "category": "smart_home"
            },
            "turn_off_lights": {
                "description": "Turn off lights in a room or specific light", 
                "parameters": ["room"],
                "category": "smart_home"
            },
            "play_music": {
                "description": "Play music on Spotify",
                "parameters": ["query", "device", "type"],
                "category": "smart_home"
            },
            "pause_music": {
                "description": "Pause music playback",
                "parameters": ["device"],
                "category": "smart_home"
            },
            "resume_music": {
                "description": "Resume music playback", 
                "parameters": ["device"],
                "category": "smart_home"
            },
            "set_volume": {
                "description": "Set volume for music or speakers",
                "parameters": ["device", "volume"],
                "category": "smart_home"
            },
            "set_temperature": {
                "description": "Set temperature in room",
                "parameters": ["room", "temperature"],
                "category": "smart_home"
            }
        }
        
        # General AI tools
        self.general_tools = {
            "web_search": {
                "description": "Search the web for current information",
                "parameters": ["query"],
                "category": "general",
                "function": self._web_search
            },
            "get_time": {
                "description": "Get current date and time",
                "parameters": [],
                "category": "general", 
                "function": self._get_time
            },
            "calculate": {
                "description": "Perform mathematical calculations",
                "parameters": ["expression"],
                "category": "general",
                "function": self._calculate
            },
            "get_weather": {
                "description": "Get weather for specified location",
                "parameters": ["location"],
                "category": "general",
                "function": self._get_weather
            }
        }
        
        # Test connection
        if not self._test_connection():
            logger.warning("Could not connect to local LLM. Make sure Ollama is running.")
        else:
            logger.info(f"Connected to unified LLM: {model_name}")
    
    def _test_connection(self) -> bool:
        """Test connection to local LLM"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Local LLM connection error: {e}")
            return False
    
    def process_command(self, command: str, current_room: Optional[str] = None) -> CommandResult:
        """Main entry point - processes any command (smart home or general)"""
        try:
            # Check if we're already in an async context
            try:
                loop = asyncio.get_running_loop()
                # We're in an async context, create a task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.process_unified_command(command, {"current_room": current_room}))
                    result = future.result(timeout=60)
            except RuntimeError:
                # No running loop, safe to create new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.process_unified_command(command, {"current_room": current_room}))
                loop.close()
            
            # Convert to CommandResult for compatibility
            return CommandResult(
                success=result.success,
                tasks=result.tasks or [],
                response=result.response,
                error=result.error
            )
            
        except Exception as e:
            logger.error(f"Error in process_command: {e}")
            return CommandResult(
                success=False,
                tasks=[],
                response="Sorry, I encountered an error processing your command.",
                error=str(e)
            )
    
    async def process_unified_command(self, user_input: str, context: Optional[Dict] = None) -> UnifiedResult:
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
            llm_response = await self._call_unified_llm(system_prompt, user_input, analysis)
            
            # Parse response based on analysis
            if analysis["has_smart_home_commands"]:
                # Smart home: require JSON + extract tasks
                tasks, response_text = self._parse_smart_home_response(llm_response, user_input)
                
                # Check for general AI tools too
                tool_calls = self._extract_tool_calls(llm_response)
                tool_results = {}
                
                if tool_calls:
                    tool_results = await self._execute_tools(tool_calls)
                    # Enhance response with tool results
                    if tool_results:
                        response_text = self._enhance_response_with_tools(response_text, tool_results)
                
                result = UnifiedResult(
                    success=len(tasks) > 0 or len(tool_calls) > 0,
                    response=response_text,
                    tasks=tasks,
                    tool_calls=tool_calls,
                    tool_results=tool_results,
                    type="smart_home" if tasks else "general"
                )
            else:
                # General AI: natural response + tool extraction
                tool_calls = self._extract_tool_calls(llm_response)
                tool_results = {}
                
                if tool_calls:
                    tool_results = await self._execute_tools(tool_calls)
                
                # Clean response (remove tool syntax)
                clean_response = self._clean_response_text(llm_response, tool_results)
                
                result = UnifiedResult(
                    success=True,
                    response=clean_response,
                    tasks=[],
                    tool_calls=tool_calls,
                    tool_results=tool_results,
                    type="general"
                )
            
            # Add to conversation history
            self._update_conversation_history(user_input, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in unified processing: {e}")
            return UnifiedResult(
                success=False,
                response=f"I encountered an error: {str(e)}",
                error=str(e)
            )
    
    def _analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze input to determine appropriate processing strategy"""
        smart_home_keywords = [
            "lights", "music", "temperature", "volume", "brightness",
            "play", "pause", "turn on", "turn off", "set", "dim", "brighten",
            "spotify", "thermostat", "lamp", "bedroom", "living room", "kitchen"
        ]
        
        general_ai_keywords = [
            "time", "weather", "calculate", "math", "search", "what is",
            "how to", "explain", "tell me about", "news", "today", "when"
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
        current_room = context.get("current_room", "unknown") if context else "unknown"
        
        # Format smart home actions
        smart_actions = "\n".join([
            f"- {action}: {info['description']} (parameters: {', '.join(info['parameters'])})"
            for action, info in self.smart_home_actions.items()
        ])
        
        # Format general tools  
        general_tools = "\n".join([
            f"- {name}: {info['description']} (parameters: {', '.join(info['parameters']) if info['parameters'] else 'none'})"
            for name, info in self.general_tools.items()
        ])
        
        if analysis["has_smart_home_commands"]:
            # Include JSON format requirement
            json_format = """
IMPORTANT: For smart home commands, you MUST include a JSON section like this:

SMART_HOME_JSON:
{
  "tasks": [
    {
      "action": "turn_on_lights",
      "target": "living_room", 
      "parameters": {"room": "living_room", "brightness": 128},
      "room": "living_room",
      "priority": 1
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
Current room: {current_room}

SMART HOME CAPABILITIES:
{smart_actions}

GENERAL AI CAPABILITIES:  
{general_tools}

{json_format}

EXAMPLES:

User: "Turn on the living room lights and what time is it?"
Response: "I'll turn on the living room lights for you! The current time is {current_time}."

SMART_HOME_JSON:
{{"tasks": [{{"action": "turn_on_lights", "target": "living_room", "parameters": {{"room": "living_room", "brightness": 255}}, "room": "living_room", "priority": 1}}], "success": true}}

TOOL_CALL: get_time()

User: "What's 15 * 23?"
Response: "Let me calculate that for you."
TOOL_CALL: calculate(expression="15 * 23")

User: "Play jazz music"
Response: "I'll play some jazz music for you."
SMART_HOME_JSON:
{{"tasks": [{{"action": "play_music", "target": "default", "parameters": {{"query": "jazz", "type": "genre"}}, "room": "{current_room}", "priority": 1}}], "success": true}}

Instructions:
1. Handle both smart home and general queries in the same conversation
2. For smart home commands: Always include SMART_HOME_JSON section
3. For general queries: Use TOOL_CALL format when needed
4. Be conversational and helpful
5. You can combine both capabilities in one response
6. Always respond with natural text, JSON and tool calls are additional
"""
    
    async def _call_unified_llm(self, system_prompt: str, user_input: str, analysis: Dict[str, Any]) -> str:
        """Call the LLM with unified prompting"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Adjust temperature based on task type
                temperature = 0.1 if analysis["has_smart_home_commands"] else 0.7
                
                payload = {
                    "model": self.model_name,
                    "prompt": f"{system_prompt}\n\nUser: {user_input}\nAssistant:",
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.9,
                        "repeat_penalty": 1.1,
                        "stop": ["\n\n", "User:", "Human:"]
                    }
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/generate",
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60)
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            llm_response = result.get("response", "").strip()
                            
                            # For smart home commands, validate JSON
                            if analysis["has_smart_home_commands"]:
                                if self._has_valid_smart_home_json(llm_response):
                                    return llm_response
                                elif attempt < max_retries - 1:
                                    logger.warning(f"Attempt {attempt + 1}: Invalid JSON response, retrying...")
                                    continue
                            
                            return llm_response
                        else:
                            raise Exception(f"HTTP {response.status}")
                            
            except Exception as e:
                logger.error(f"Unified LLM API error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                
        return ""
    
    def _has_valid_smart_home_json(self, response: str) -> bool:
        """Check if response contains valid smart home JSON"""
        json_pattern = r'SMART_HOME_JSON:\s*(\{.*?\})'
        json_match = re.search(json_pattern, response, re.DOTALL)
        
        if json_match:
            try:
                json.loads(json_match.group(1))
                return True
            except json.JSONDecodeError:
                pass
        
        return False
    
    def _parse_smart_home_response(self, response: str, original_command: str) -> tuple[List[Task], str]:
        """Parse smart home JSON from response while preserving conversational text"""
        tasks = []
        
        # Extract JSON section
        json_pattern = r'SMART_HOME_JSON:\s*(\{.*?\})'
        json_match = re.search(json_pattern, response, re.DOTALL)
        
        if json_match:
            try:
                json_data = json.loads(json_match.group(1))
                tasks_data = json_data.get("tasks", [])
                
                for task_data in tasks_data:
                    task = Task(
                        action=task_data.get("action", ""),
                        target=task_data.get("target", ""),
                        parameters=task_data.get("parameters", {}),
                        room=task_data.get("room", ""),
                        priority=task_data.get("priority", 1)
                    )
                    tasks.append(task)
                    
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
        
        # Extract conversational text (everything except JSON)
        conversational_text = re.sub(json_pattern, "", response, flags=re.DOTALL).strip()
        
        # If no tasks found, try keyword-based parsing as fallback
        if not tasks:
            tasks = self._keyword_based_parsing(original_command)
            if not conversational_text:
                conversational_text = "I'll help you with that."
        
        return tasks, conversational_text
    
    def _keyword_based_parsing(self, command: str) -> List[Task]:
        """Fallback parsing using keywords"""
        tasks = []
        command_lower = command.lower()
        
        # Simple patterns for common commands
        if "turn on" in command_lower and "light" in command_lower:
            room = "living_room"  # default
            for room_name in ["bedroom", "kitchen", "living room", "bathroom"]:
                if room_name in command_lower:
                    room = room_name.replace(" ", "_")
                    break
            
            task = Task(
                action="turn_on_lights",
                target=room,
                parameters={"room": room},
                room=room,
                priority=1
            )
            tasks.append(task)
        
        elif "play" in command_lower and "music" in command_lower:
            # Extract music query
            query = "music"
            task = Task(
                action="play_music", 
                target="default",
                parameters={"query": query, "type": "track"},
                room="",
                priority=1
            )
            tasks.append(task)
        
        return tasks
    
    def _extract_tool_calls(self, response: str) -> List[Dict]:
        """Extract tool calls from LLM response"""
        tool_pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        tool_matches = re.findall(tool_pattern, response)
        
        tool_calls = []
        for tool_name, params_str in tool_matches:
            if tool_name in self.general_tools:
                # Parse parameters
                params = {}
                if params_str.strip():
                    # Handle both quoted and unquoted parameters
                    param_pairs = re.findall(r'(\w+)=(["\']?)([^,")]*)\2', params_str)
                    for key, _, value in param_pairs:
                        params[key] = value
                
                tool_calls.append({
                    "tool": tool_name,
                    "parameters": params
                })
        
        return tool_calls
    
    async def _execute_tools(self, tool_calls: List[Dict]) -> Dict[str, Any]:
        """Execute tool calls"""
        results = {}
        for call in tool_calls:
            tool_name = call["tool"]
            parameters = call["parameters"]
            
            if tool_name in self.general_tools:
                func = self.general_tools[tool_name]["function"]
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(**parameters)
                    else:
                        result = func(**parameters)
                    results[tool_name] = result
                except Exception as e:
                    logger.error(f"Tool execution error for {tool_name}: {e}")
                    results[tool_name] = f"Error: {str(e)}"
        
        return results
    
    def _enhance_response_with_tools(self, response_text: str, tool_results: Dict[str, Any]) -> str:
        """Enhance response text with tool results"""
        if not tool_results:
            return response_text
        
        enhanced_parts = [response_text]
        
        for tool_name, result in tool_results.items():
            if tool_name == "get_time":
                enhanced_parts.append(f"The current time is {result}.")
            elif tool_name == "calculate":
                enhanced_parts.append(f"The calculation result is {result}.")
            elif tool_name == "get_weather":
                enhanced_parts.append(f"Weather info: {result}")
            elif tool_name == "web_search":
                enhanced_parts.append(f"Here's what I found: {result}")
        
        return " ".join(enhanced_parts)
    
    def _clean_response_text(self, response: str, tool_results: Dict[str, Any]) -> str:
        """Clean response text and integrate tool results"""
        # Remove tool call syntax
        clean_response = re.sub(r'TOOL_CALL:\s*\w+\([^)]*\)', "", response).strip()
        
        # Integrate tool results naturally
        if tool_results:
            result_parts = []
            for tool_name, result in tool_results.items():
                if tool_name == "get_time":
                    result_parts.append(f"The current time is {result}")
                elif tool_name == "calculate":
                    result_parts.append(f"The answer is {result}")
                elif tool_name == "get_weather":
                    result_parts.append(f"{result}")
                elif tool_name == "web_search":
                    result_parts.append(f"{result}")
            
            if result_parts:
                if clean_response:
                    clean_response += " " + " ".join(result_parts)
                else:
                    clean_response = " ".join(result_parts)
        
        return clean_response or "I'll help you with that."
    
    def _update_conversation_history(self, user_input: str, result: UnifiedResult):
        """Update conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        self.conversation_history.append({
            "role": "assistant", 
            "content": result.response,
            "type": result.type
        })
        
        # Keep manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    # Tool implementations
    async def _web_search(self, query: str) -> str:
        """Search the web using DuckDuckGo"""
        try:
            # Simple web search simulation
            # In production, would use actual web search API
            return f"Search results for '{query}': Found relevant information about {query}."
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _get_time(self) -> str:
        """Get current time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _calculate(self, expression: str) -> str:
        """Safe mathematical calculation"""
        try:
            # Safe evaluation - only allow math operations
            allowed_chars = set("0123456789+-*/.() ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return str(result)
            else:
                return "Invalid expression"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    async def _get_weather(self, location: str) -> str:
        """Get weather information"""
        try:
            # Weather API simulation
            # In production, would use actual weather API
            return f"Weather in {location}: Sunny, 72°F with light clouds"
        except Exception as e:
            return f"Weather error: {str(e)}" 