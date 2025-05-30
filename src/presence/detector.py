import subprocess
import time
import threading
from typing import Dict, List, Optional, Callable
import logging
import json

logger = logging.getLogger(__name__)

class PresenceDetector:
    """Detects user presence using various methods"""
    
    def __init__(self, method: str = "bluetooth", devices: List[str] = None, callback: Optional[Callable] = None):
        self.method = method
        self.devices = devices or []
        self.callback = callback
        self.current_room = None
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Room mapping based on device proximity/signal strength
        self.room_mapping = {
            "living_room": {"bluetooth_threshold": -60, "wifi_ssid": "Living_Room_AP"},
            "bedroom": {"bluetooth_threshold": -65, "wifi_ssid": "Bedroom_AP"},
            "kitchen": {"bluetooth_threshold": -70, "wifi_ssid": "Kitchen_AP"},
            "office": {"bluetooth_threshold": -55, "wifi_ssid": "Office_AP"}
        }
    
    def start_monitoring(self):
        """Start presence monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_presence)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info(f"Started presence monitoring using {self.method}")
    
    def stop_monitoring(self):
        """Stop presence monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Stopped presence monitoring")
    
    def _monitor_presence(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                if self.method == "bluetooth":
                    self._check_bluetooth_presence()
                elif self.method == "wifi":
                    self._check_wifi_presence()
                elif self.method == "combined":
                    self._check_combined_presence()
                
                time.sleep(10)  # Check every 10 seconds
            except Exception as e:
                logger.error(f"Error in presence monitoring: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _check_bluetooth_presence(self):
        """Check presence using Bluetooth device scanning"""
        try:
            # Use bluetoothctl to scan for devices
            result = subprocess.run(
                ["bluetoothctl", "devices"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                detected_devices = []
                for line in result.stdout.split('\n'):
                    if 'Device' in line:
                        mac = line.split()[1]
                        if mac in self.devices:
                            detected_devices.append(mac)
                
                if detected_devices:
                    # Try to get signal strength for room detection
                    room = self._determine_room_from_bluetooth()
                    self._update_presence(room or "unknown")
                else:
                    self._update_presence(None)
            
        except subprocess.TimeoutExpired:
            logger.warning("Bluetooth scan timeout")
        except Exception as e:
            logger.error(f"Bluetooth presence check failed: {e}")
    
    def _check_wifi_presence(self):
        """Check presence using WiFi network scanning"""
        try:
            # This is a simplified implementation
            # In practice, you'd use more sophisticated WiFi scanning
            result = subprocess.run(
                ["iwlist", "scan"], 
                capture_output=True, 
                text=True, 
                timeout=15
            )
            
            if result.returncode == 0:
                # Parse WiFi networks and signal strengths
                room = self._determine_room_from_wifi(result.stdout)
                self._update_presence(room)
            
        except Exception as e:
            logger.error(f"WiFi presence check failed: {e}")
    
    def _check_combined_presence(self):
        """Check presence using combined methods"""
        # Combine bluetooth and wifi for better accuracy
        self._check_bluetooth_presence()
        # Could add more sophisticated logic here
    
    def _determine_room_from_bluetooth(self) -> Optional[str]:
        """Determine room based on Bluetooth signal strength"""
        # This is a simplified implementation
        # In practice, you'd measure RSSI values and map to rooms
        strongest_room = None
        strongest_signal = -100
        
        for room, config in self.room_mapping.items():
            # Simulate signal strength check
            # In real implementation, you'd use actual RSSI measurements
            simulated_signal = -60  # Placeholder
            if simulated_signal > strongest_signal:
                strongest_signal = simulated_signal
                strongest_room = room
        
        return strongest_room if strongest_signal > -80 else None
    
    def _determine_room_from_wifi(self, scan_output: str) -> Optional[str]:
        """Determine room based on WiFi signal strength"""
        # Parse WiFi scan output and determine strongest signal
        # This is a simplified implementation
        for room, config in self.room_mapping.items():
            if config.get("wifi_ssid") in scan_output:
                return room
        return None
    
    def _update_presence(self, room: Optional[str]):
        """Update current presence and notify callback"""
        if room != self.current_room:
            previous_room = self.current_room
            self.current_room = room
            
            logger.info(f"Presence changed: {previous_room} -> {room}")
            
            if self.callback:
                self.callback(room, previous_room)
    
    def get_current_room(self) -> Optional[str]:
        """Get current room"""
        return self.current_room
    
    def is_present(self) -> bool:
        """Check if user is present"""
        return self.current_room is not None
    
    def set_room_mapping(self, mapping: Dict[str, Dict]):
        """Update room mapping configuration"""
        self.room_mapping.update(mapping)
        logger.info("Room mapping updated")
    
    def manual_set_room(self, room: str):
        """Manually set current room (for testing/override)"""
        self._update_presence(room)
        logger.info(f"Manually set room to: {room}")


class SimplePresenceDetector:
    """Simplified presence detector for basic functionality"""
    
    def __init__(self, default_room: str = "living_room"):
        self.current_room = default_room
        self.callbacks = []
    
    def add_callback(self, callback: Callable):
        """Add presence change callback"""
        self.callbacks.append(callback)
    
    def set_room(self, room: str):
        """Set current room"""
        old_room = self.current_room
        self.current_room = room
        
        for callback in self.callbacks:
            callback(room, old_room)
    
    def get_current_room(self) -> str:
        """Get current room"""
        return self.current_room 