import openai
import json
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """Represents a single task to be executed"""
    action: str
    target: str
    parameters: Dict[str, Any]
    room: Optional[str] = None
    priority: int = 1

@dataclass
class CommandResult:
    """Result of command processing"""
    success: bool
    tasks: List[Task]
    response: str
    error: Optional[str] = None

class CommandProcessor:
    """Processes voice commands using LLM and generates task chains"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
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
                "parameters": ["query", "device", "type"]  # type: track, artist, playlist
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
        
        logger.info("Command processor initialized")
    
    def process_command(self, command: str, current_room: Optional[str] = None) -> CommandResult:
        """Process a voice command and return tasks to execute"""
        try:
            # Create system prompt with available actions
            system_prompt = self._create_system_prompt(current_room)
            
            # Send to LLM for processing
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ],
                temperature=0.1
            )
            
            # Parse LLM response
            llm_response = response.choices[0].message.content
            return self._parse_llm_response(llm_response, command)
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return CommandResult(
                success=False,
                tasks=[],
                response="Sorry, I couldn't understand that command.",
                error=str(e)
            )
    
    def _create_system_prompt(self, current_room: Optional[str] = None) -> str:
        """Create system prompt for LLM"""
        actions_desc = "\n".join([
            f"- {action}: {info['description']} (parameters: {', '.join(info['parameters'])})"
            for action, info in self.available_actions.items()
        ])
        
        room_context = f"The user is currently in the {current_room}." if current_room else "Room context unknown."
        
        return f"""You are Totoro, a helpful personal assistant that controls smart home devices and music.

{room_context}

Available actions:
{actions_desc}

When the user gives a command, analyze it and respond with a JSON object containing:
1. "tasks": Array of tasks to execute, each with:
   - "action": One of the available actions
   - "target": The specific target (room name, device name, etc.)
   - "parameters": Object with action parameters
   - "room": Room context (if applicable)
   - "priority": Execution priority (1=highest, 5=lowest)
2. "response": A friendly response to the user
3. "success": Boolean indicating if the command was understood

Examples:
User: "Turn on the living room lights"
Response: {{
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

User: "Play some jazz music in the kitchen and dim the lights"
Response: {{
  "tasks": [
    {{
      "action": "play_music",
      "target": "kitchen_speaker",
      "parameters": {{"query": "jazz", "device": "kitchen", "type": "genre"}},
      "room": "kitchen",
      "priority": 1
    }},
    {{
      "action": "turn_on_lights",
      "target": "kitchen",
      "parameters": {{"room": "kitchen", "brightness": 128}},
      "room": "kitchen",
      "priority": 2
    }}
  ],
  "response": "I'll play some jazz music in the kitchen and dim the lights for you.",
  "success": true
}}

Always respond with valid JSON. If you can't understand the command, set success to false and provide a helpful response."""
    
    def _parse_llm_response(self, llm_response: str, original_command: str) -> CommandResult:
        """Parse LLM response into CommandResult"""
        try:
            # Try to extract JSON from response
            response_data = json.loads(llm_response)
            
            # Validate response structure
            if not isinstance(response_data, dict):
                raise ValueError("Response is not a JSON object")
            
            success = response_data.get("success", False)
            response_text = response_data.get("response", "Command processed.")
            tasks_data = response_data.get("tasks", [])
            
            # Convert tasks data to Task objects
            tasks = []
            for task_data in tasks_data:
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
                response=response_text
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return CommandResult(
                success=False,
                tasks=[],
                response="I'm having trouble understanding that command. Could you try rephrasing it?",
                error=f"JSON parse error: {e}"
            )
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return CommandResult(
                success=False,
                tasks=[],
                response="Sorry, I encountered an error processing your command.",
                error=str(e)
            )
    
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
    
    def remove_action(self, action_name: str):
        """Remove an available action"""
        if action_name in self.available_actions:
            del self.available_actions[action_name]
            logger.info(f"Removed action: {action_name}")
        else:
            logger.warning(f"Action not found: {action_name}") 