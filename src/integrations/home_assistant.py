import requests
import json
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class HomeAssistantClient:
    """Client for interacting with Home Assistant"""
    
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Test connection
        if not self.test_connection():
            logger.error("Failed to connect to Home Assistant")
    
    def test_connection(self) -> bool:
        """Test connection to Home Assistant"""
        try:
            response = requests.get(f"{self.url}/api/", headers=self.headers, timeout=5)
            if response.status_code == 200:
                logger.info("Successfully connected to Home Assistant")
                return True
            else:
                logger.error(f"Home Assistant connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Home Assistant connection error: {e}")
            return False
    
    def get_states(self) -> List[Dict]:
        """Get all entity states"""
        try:
            response = requests.get(f"{self.url}/api/states", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting states: {e}")
            return []
    
    def get_entity_state(self, entity_id: str) -> Optional[Dict]:
        """Get state of specific entity"""
        try:
            response = requests.get(f"{self.url}/api/states/{entity_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting entity state for {entity_id}: {e}")
            return None
    
    def call_service(self, domain: str, service: str, entity_id: Optional[str] = None, 
                    service_data: Optional[Dict] = None) -> bool:
        """Call a Home Assistant service"""
        try:
            data = service_data or {}
            if entity_id:
                data['entity_id'] = entity_id
            
            response = requests.post(
                f"{self.url}/api/services/{domain}/{service}",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            logger.info(f"Successfully called service {domain}.{service}")
            return True
        except Exception as e:
            logger.error(f"Error calling service {domain}.{service}: {e}")
            return False
    
    def turn_on_light(self, entity_id: str, brightness: Optional[int] = None, 
                     color: Optional[str] = None) -> bool:
        """Turn on a light with optional brightness and color"""
        service_data = {}
        if brightness is not None:
            service_data['brightness'] = max(0, min(255, brightness))
        if color:
            # Convert color name to RGB if needed
            service_data['color_name'] = color
        
        return self.call_service('light', 'turn_on', entity_id, service_data)
    
    def turn_off_light(self, entity_id: str) -> bool:
        """Turn off a light"""
        return self.call_service('light', 'turn_off', entity_id)
    
    def set_light_brightness(self, entity_id: str, brightness: int) -> bool:
        """Set light brightness (0-255)"""
        brightness = max(0, min(255, brightness))
        return self.call_service('light', 'turn_on', entity_id, {'brightness': brightness})
    
    def get_lights(self) -> List[Dict]:
        """Get all light entities"""
        states = self.get_states()
        return [state for state in states if state['entity_id'].startswith('light.')]
    
    def get_lights_in_room(self, room: str) -> List[Dict]:
        """Get lights in a specific room"""
        lights = self.get_lights()
        room_lights = []
        for light in lights:
            # Check if room name is in entity_id or friendly_name
            entity_id = light['entity_id'].lower()
            friendly_name = light.get('attributes', {}).get('friendly_name', '').lower()
            if room.lower() in entity_id or room.lower() in friendly_name:
                room_lights.append(light)
        return room_lights
    
    def turn_on_room_lights(self, room: str, brightness: Optional[int] = None) -> bool:
        """Turn on all lights in a room"""
        lights = self.get_lights_in_room(room)
        if not lights:
            logger.warning(f"No lights found in room: {room}")
            return False
        
        success = True
        for light in lights:
            if not self.turn_on_light(light['entity_id'], brightness):
                success = False
        
        return success
    
    def turn_off_room_lights(self, room: str) -> bool:
        """Turn off all lights in a room"""
        lights = self.get_lights_in_room(room)
        if not lights:
            logger.warning(f"No lights found in room: {room}")
            return False
        
        success = True
        for light in lights:
            if not self.turn_off_light(light['entity_id']):
                success = False
        
        return success
    
    def get_switches(self) -> List[Dict]:
        """Get all switch entities"""
        states = self.get_states()
        return [state for state in states if state['entity_id'].startswith('switch.')]
    
    def turn_on_switch(self, entity_id: str) -> bool:
        """Turn on a switch"""
        return self.call_service('switch', 'turn_on', entity_id)
    
    def turn_off_switch(self, entity_id: str) -> bool:
        """Turn off a switch"""
        return self.call_service('switch', 'turn_off', entity_id)
    
    def get_media_players(self) -> List[Dict]:
        """Get all media player entities"""
        states = self.get_states()
        return [state for state in states if state['entity_id'].startswith('media_player.')]
    
    def play_media(self, entity_id: str, media_content_id: str, media_content_type: str = 'music') -> bool:
        """Play media on a media player"""
        service_data = {
            'media_content_id': media_content_id,
            'media_content_type': media_content_type
        }
        return self.call_service('media_player', 'play_media', entity_id, service_data)
    
    def set_volume(self, entity_id: str, volume: float) -> bool:
        """Set volume for media player (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        return self.call_service('media_player', 'volume_set', entity_id, {'volume_level': volume}) 