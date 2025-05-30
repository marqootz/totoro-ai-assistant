import requests
import json
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
from .command_processor import Task, CommandResult

logger = logging.getLogger(__name__)

class LocalLLMProcessor:
    """Processes voice commands using local LLM (Ollama, etc.)"""
    
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        
        # Define available actions and their parameters
        self.available_actions = {
            "turn_on_lights": {
                "description": "Turn on lights in a room or specific light",
                "parameters": ["room", "brightness", "color"]
            },
            "turn_off_lights": {
                "description": "Turn off lights in a room or specific light",
                "parameters": ["room"]
            },
            "play_music": {
                "description": "Play music on Spotify",
                "parameters": ["query", "device", "type"]
            },
            "pause_music": {
                "description": "Pause music playback",
                "parameters": ["device"]
            },
            "resume_music": {
                "description": "Resume music playback",
                "parameters": ["device"]
            },
            "set_volume": {
                "description": "Set volume for music or speakers",
                "parameters": ["device", "volume"]
            },
            "change_room": {
                "description": "Change current room context",
                "parameters": ["room"]
            }
        }
        
        # Test connection
        if not self._test_connection():
            logger.warning("Could not connect to local LLM. Make sure Ollama is running.")
        else:
            logger.info(f"Connected to local LLM: {model_name}")
    
    def _test_connection(self) -> bool:
        """Test connection to local LLM"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Local LLM connection error: {e}")
            return False
    
    def process_command(self, command: str, current_room: Optional[str] = None) -> CommandResult:
        """Process a voice command and return tasks to execute"""
        try:
            # Create system prompt
            system_prompt = self._create_system_prompt(current_room)
            
            # Send to local LLM
            response = self._call_local_llm(system_prompt, command)
            
            # Parse response
            return self._parse_llm_response(response, command)
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return CommandResult(
                success=False,
                tasks=[],
                response="Sorry, I couldn't understand that command.",
                error=str(e)
            )
    
    def _call_local_llm(self, system_prompt: str, user_message: str) -> str:
        """Call local LLM API with retry logic for better JSON consistency"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Ollama API format
                payload = {
                    "model": self.model_name,
                    "prompt": f"{system_prompt}\n\nUser: {user_message}\nAssistant:",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Lower temperature for more consistent responses
                        "top_p": 0.9,
                        "repeat_penalty": 1.1,  # Prevent repetition
                        "stop": ["\n\n", "User:", "Human:"]  # Stop at these tokens
                    }
                }
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                
                result = response.json()
                llm_response = result.get("response", "").strip()
                
                # Validate that response looks like JSON
                if self._is_valid_json_response(llm_response):
                    return llm_response
                else:
                    logger.warning(f"Attempt {attempt + 1}: Invalid JSON response, retrying...")
                    if attempt < max_retries - 1:
                        # Try with more explicit instruction
                        payload["prompt"] += " Remember: respond with valid JSON only."
                        continue
                
                return llm_response  # Return even if not perfect JSON on last attempt
                
            except Exception as e:
                logger.error(f"Local LLM API error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                
        return ""  # Fallback
    
    def _is_valid_json_response(self, response: str) -> bool:
        """Check if response looks like valid JSON"""
        response = response.strip()
        
        # Must start with { and end with }
        if not (response.startswith('{') and response.endswith('}')):
            return False
            
        # Try to parse as JSON
        try:
            json.loads(response)
            return True
        except json.JSONDecodeError:
            return False
    
    def _create_system_prompt(self, current_room: Optional[str] = None) -> str:
        """Create system prompt for local LLM"""
        actions_desc = "\n".join([
            f"- {action}: {info['description']} (parameters: {', '.join(info['parameters'])})"
            for action, info in self.available_actions.items()
        ])
        
        room_context = f"The user is currently in the {current_room}." if current_room else "Room context unknown."
        
        return f"""You are Totoro, a smart home assistant. You MUST respond with valid JSON only.

{room_context}

Available actions:
{actions_desc}

RESPONSE FORMAT (MANDATORY):
{{
  "tasks": [array of task objects],
  "response": "friendly response text",
  "success": true/false
}}

Each task object MUST have:
{{
  "action": "one of the available actions",
  "target": "room/device name", 
  "parameters": {{"key": "value"}},
  "room": "room name",
  "priority": 1-5
}}

EXAMPLES:

User: "Turn on the living room lights"
{{
  "tasks": [{{
    "action": "turn_on_lights",
    "target": "living_room", 
    "parameters": {{"room": "living_room"}},
    "room": "living_room",
    "priority": 1
  }}],
  "response": "I'll turn on the living room lights for you.",
  "success": true
}}

User: "Play jazz music and dim the bedroom lights"
{{
  "tasks": [{{
    "action": "play_music",
    "target": "default",
    "parameters": {{"query": "jazz", "type": "track"}},
    "priority": 1
  }}, {{
    "action": "turn_on_lights", 
    "target": "bedroom",
    "parameters": {{"room": "bedroom", "brightness": 64}},
    "room": "bedroom", 
    "priority": 2
  }}],
  "response": "I'll play jazz music and dim the bedroom lights for you.",
  "success": true
}}

User: "Turn off all the lights and pause music"
{{
  "tasks": [{{
    "action": "turn_off_lights",
    "target": "all",
    "parameters": {{"room": "all"}},
    "priority": 1
  }}, {{
    "action": "pause_music", 
    "target": "default",
    "parameters": {{}},
    "priority": 2
  }}],
  "response": "I'll turn off all lights and pause the music.",
  "success": true
}}

User: "What's the weather?"
{{
  "tasks": [],
  "response": "I can't check the weather, but I can control your lights and music.",
  "success": false
}}

IMPORTANT RULES:
1. ALWAYS respond with valid JSON only
2. Never include extra text before or after JSON
3. For multi-step commands, create multiple tasks with different priorities
4. If you can't understand, set success to false
5. Use "all" as target for commands affecting all devices
6. For brightness: 0-255 scale (25%=64, 50%=128, 75%=192)
7. Parse room names carefully (living room = living_room)"""
    
    def _parse_llm_response(self, llm_response: str, original_command: str) -> CommandResult:
        """Parse LLM response into CommandResult with enhanced error handling"""
        try:
            # Clean up response - remove common prefixes/suffixes
            response_text = llm_response.strip()
            
            # Remove common non-JSON prefixes
            prefixes_to_remove = [
                "Here's the JSON response:",
                "Here is the response:",
                "Response:",
                "JSON:",
                "```json",
                "```"
            ]
            
            for prefix in prefixes_to_remove:
                if response_text.startswith(prefix):
                    response_text = response_text[len(prefix):].strip()
            
            # Remove common suffixes
            suffixes_to_remove = ["```", "That's it!", "Done.", "Hope this helps!"]
            for suffix in suffixes_to_remove:
                if response_text.endswith(suffix):
                    response_text = response_text[:-len(suffix)].strip()
            
            # Try to find JSON in the response (multiple strategies)
            json_data = self._extract_json_from_response(response_text, original_command)
            
            if not json_data:
                # Fallback: try to create JSON from the natural language response
                return self._create_fallback_response(response_text, original_command)
            
            # Validate required fields
            success = json_data.get("success", True)
            response_msg = json_data.get("response", "Command processed.")
            tasks_data = json_data.get("tasks", [])
            
            # Convert tasks data to Task objects
            tasks = []
            for task_data in tasks_data:
                if isinstance(task_data, dict):
                    task = Task(
                        action=task_data.get("action", ""),
                        target=task_data.get("target", ""),
                        parameters=task_data.get("parameters", {}),
                        room=task_data.get("room"),
                        priority=task_data.get("priority", 1)
                    )
                    tasks.append(task)
            
            return CommandResult(
                success=success,
                tasks=tasks,
                response=response_msg
            )
            
        except Exception as e:
            logger.error(f"Error parsing local LLM response: {e}")
            logger.error(f"Response was: {llm_response}")
            return self._create_fallback_response(llm_response, original_command)
    
    def _extract_json_from_response(self, response_text: str, original_command: str) -> Optional[dict]:
        """Try multiple strategies to extract JSON from response"""
        
        # Strategy 1: Direct JSON parsing
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Find JSON block in text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            try:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass
        
        # Strategy 3: Look for JSON between markers
        import re
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, response_text)
        
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        return None
    
    def _create_fallback_response(self, response_text: str, original_command: str) -> CommandResult:
        """Create a reasonable response when JSON parsing fails"""
        command_lower = original_command.lower()
        
        # Try to parse common commands using keyword matching
        if "turn on" in command_lower and "light" in command_lower:
            room = self._extract_room_from_command(command_lower) or "living_room"
            task = Task(
                action="turn_on_lights",
                target=room,
                parameters={"room": room},
                room=room,
                priority=1
            )
            return CommandResult(
                success=True,
                tasks=[task],
                response=f"I'll turn on the {room.replace('_', ' ')} lights for you."
            )
        
        elif "turn off" in command_lower and "light" in command_lower:
            room = self._extract_room_from_command(command_lower) or "living_room"
            task = Task(
                action="turn_off_lights",
                target=room,
                parameters={"room": room},
                room=room,
                priority=1
            )
            return CommandResult(
                success=True,
                tasks=[task],
                response=f"I'll turn off the {room.replace('_', ' ')} lights for you."
            )
        
        elif "play" in command_lower and "music" in command_lower:
            query = command_lower.replace("play", "").replace("music", "").strip()
            task = Task(
                action="play_music",
                target="default",
                parameters={"query": query, "type": "track"},
                priority=1
            )
            return CommandResult(
                success=True,
                tasks=[task],
                response=f"I'll play {query} music for you."
            )
        
        # If we can't parse, return the model's response as-is
        return CommandResult(
            success=False,
            tasks=[],
            response=response_text if response_text else "I'm having trouble understanding that command. Could you try rephrasing it?",
            error="JSON parsing failed, used fallback"
        )
    
    def _extract_room_from_command(self, command: str) -> Optional[str]:
        """Extract room name from command text"""
        rooms = ["living room", "bedroom", "kitchen", "bathroom", "office", "dining room", "basement", "garage"]
        for room in rooms:
            if room in command:
                return room.replace(" ", "_")
        return None
    
    def get_available_actions(self) -> Dict[str, Dict]:
        """Get available actions and their descriptions"""
        return self.available_actions.copy()
    
    def add_action(self, action_name: str, description: str, parameters: List[str]):
        """Add a new available action"""
        self.available_actions[action_name] = {
            "description": description,
            "parameters": parameters
        }
        logger.info(f"Added new action: {action_name}")


class HuggingFaceLLMProcessor:
    """Alternative processor using Hugging Face Transformers"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.model.to(self.device)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Loaded Hugging Face model: {model_name} on {self.device}")
            
        except ImportError:
            logger.error("Hugging Face transformers not installed. Run: pip install transformers torch")
            raise
        except Exception as e:
            logger.error(f"Error loading Hugging Face model: {e}")
            raise
    
    def process_command(self, command: str, current_room: Optional[str] = None) -> CommandResult:
        """Process command using Hugging Face model"""
        # This is a simplified implementation
        # For production, you'd want to fine-tune the model for your specific use case
        
        try:
            # Simple command parsing based on keywords
            command_lower = command.lower()
            
            if "turn on" in command_lower and "light" in command_lower:
                room = self._extract_room(command_lower) or current_room or "living_room"
                task = Task(
                    action="turn_on_lights",
                    target=room,
                    parameters={"room": room},
                    room=room,
                    priority=1
                )
                return CommandResult(
                    success=True,
                    tasks=[task],
                    response=f"I'll turn on the {room} lights for you."
                )
            
            elif "turn off" in command_lower and "light" in command_lower:
                room = self._extract_room(command_lower) or current_room or "living_room"
                task = Task(
                    action="turn_off_lights",
                    target=room,
                    parameters={"room": room},
                    room=room,
                    priority=1
                )
                return CommandResult(
                    success=True,
                    tasks=[task],
                    response=f"I'll turn off the {room} lights for you."
                )
            
            elif "play" in command_lower and "music" in command_lower:
                query = command_lower.replace("play", "").replace("music", "").strip()
                task = Task(
                    action="play_music",
                    target="default",
                    parameters={"query": query, "type": "track"},
                    priority=1
                )
                return CommandResult(
                    success=True,
                    tasks=[task],
                    response=f"I'll play {query} music for you."
                )
            
            else:
                return CommandResult(
                    success=False,
                    tasks=[],
                    response="I'm not sure how to help with that. Try commands like 'turn on the lights' or 'play music'."
                )
                
        except Exception as e:
            logger.error(f"Error processing command with Hugging Face model: {e}")
            return CommandResult(
                success=False,
                tasks=[],
                response="Sorry, I encountered an error processing your command.",
                error=str(e)
            )
    
    def _extract_room(self, command: str) -> Optional[str]:
        """Extract room name from command"""
        rooms = ["living room", "bedroom", "kitchen", "bathroom", "office", "dining room"]
        for room in rooms:
            if room in command:
                return room.replace(" ", "_")
        return None 