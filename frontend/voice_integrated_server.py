#!/usr/bin/env python3
"""
Totoro Voice-Integrated Frontend Server
Connects to the assistant with proper error handling
"""

import os
import sys
import threading
import time
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path to access the assistant
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

class VoiceIntegratedManager:
    def __init__(self):
        self.current_state = 'idle'
        self.assistant = None
        self.state_lock = threading.Lock()
        
        # Try to initialize assistant with better error handling
        self.initialize_assistant()
    
    def initialize_assistant(self):
        """Initialize assistant with better error handling"""
        try:
            print("🔄 Attempting to initialize Totoro assistant...")
            
            # Import with error handling
            try:
                from src.assistant import TotoroAssistant
                print("✅ Successfully imported TotoroAssistant")
            except ImportError as e:
                print(f"❌ Failed to import TotoroAssistant: {e}")
                return False
            
            # Initialize with error handling
            try:
                self.assistant = TotoroAssistant()
                print("✅ Assistant initialized successfully")
                
                # Register state callback
                self.assistant.register_state_callback(self.on_assistant_state_change)
                print("✅ State callback registered")
                
                return True
                
            except Exception as e:
                print(f"❌ Failed to initialize assistant: {e}")
                print("🔧 Continuing in demo mode...")
                return False
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def on_assistant_state_change(self, state):
        """Callback when assistant state changes"""
        print(f"🎭 Assistant state changed to: {state}")
        self.set_state(state)
    
    def set_state(self, state):
        """Set the current visual state"""
        with self.state_lock:
            if self.current_state != state:
                self.current_state = state
                print(f"🎨 Frontend state updated to: {state}")
    
    def get_state(self):
        """Get the current visual state"""
        with self.state_lock:
            return self.current_state
    
    def get_assistant_state(self):
        """Get state directly from assistant if available"""
        if self.assistant:
            try:
                return self.assistant.get_visual_state()
            except Exception as e:
                print(f"❌ Error getting assistant state: {e}")
        return self.current_state
    
    def process_command(self, command):
        """Process a command through the assistant"""
        if not self.assistant:
            return "Assistant not available"
        
        try:
            return self.assistant.process_command(command)
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            return f"Error: {e}"

# Global manager
frontend_manager = VoiceIntegratedManager()

@app.route('/')
def index():
    """Serve the main interface"""
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    """Serve CSS file"""
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/api/status')
def get_status():
    """Get current status"""
    current_state = frontend_manager.get_assistant_state()
    
    return jsonify({
        'state': current_state,
        'assistant_available': frontend_manager.assistant is not None,
        'is_running': frontend_manager.assistant.is_running if frontend_manager.assistant else False,
        'timestamp': time.time()
    })

@app.route('/api/state/<state>')
def set_state(state):
    """Set state manually"""
    valid_states = ['idle', 'awake', 'thinking', 'speaking']
    if state in valid_states:
        frontend_manager.set_state(state)
        
        # Also update assistant state if available
        if frontend_manager.assistant:
            try:
                frontend_manager.assistant.set_visual_state(state)
            except Exception as e:
                print(f"❌ Error setting assistant state: {e}")
        
        return jsonify({'success': True, 'state': state})
    else:
        return jsonify({'success': False, 'error': f'Invalid state. Valid states: {valid_states}'}), 400

@app.route('/api/demo')
def start_demo():
    """Start demo mode"""
    def demo_cycle():
        states = ['idle', 'awake', 'thinking', 'speaking']
        for cycle in range(3):  # Run for 3 cycles
            for state in states:
                frontend_manager.set_state(state)
                if frontend_manager.assistant:
                    try:
                        frontend_manager.assistant.set_visual_state(state)
                    except Exception as e:
                        print(f"❌ Error in demo: {e}")
                time.sleep(3)
    
    thread = threading.Thread(target=demo_cycle, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Demo mode started'})

@app.route('/api/command/<command>')
def send_command(command):
    """Send a command to the assistant"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        response = frontend_manager.process_command(command)
        return jsonify({
            'success': True, 
            'response': response,
            'state': frontend_manager.get_assistant_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test_voice')
def test_voice():
    """Test voice command simulation"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    # Simulate a voice command processing cycle
    try:
        frontend_manager.assistant.set_visual_state('awake')
        time.sleep(1)
        frontend_manager.assistant.set_visual_state('thinking')
        time.sleep(2)
        frontend_manager.assistant.set_visual_state('speaking')
        time.sleep(2)
        frontend_manager.assistant.set_visual_state('idle')
        
        return jsonify({'success': True, 'message': 'Voice test completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🎭 Starting Voice-Integrated Totoro Frontend Server...")
    print("🌐 Frontend available at: http://localhost:5001")
    print("🔧 API endpoints:")
    print("   GET  /api/status - Get current state")
    print("   GET  /api/state/<state> - Set state manually")
    print("   GET  /api/demo - Start demo mode")
    print("   GET  /api/command/<command> - Send command to assistant")
    print("   GET  /api/test_voice - Simulate voice interaction")
    
    if frontend_manager.assistant:
        print("✅ Assistant connected - frontend will react to voice!")
    else:
        print("⚠️  Assistant not connected - running in demo mode")
    
    print(f"\n🎬 Test the interface: http://localhost:5001")
    
    # Start the web server
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True) 