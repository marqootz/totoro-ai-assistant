#!/usr/bin/env python3
"""
Totoro Frontend Server
Serves the animated face interface and provides API for state management
"""

import os
import sys
import threading
import time
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path to access the assistant
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import the assistant (optional for standalone frontend testing)
try:
    from src.assistant import TotoroAssistant
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    print("Assistant not available - running in demo mode")

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

class FrontendManager:
    def __init__(self):
        self.current_state = 'idle'
        self.assistant = None
        self.state_lock = threading.Lock()
        
        if ASSISTANT_AVAILABLE:
            try:
                self.assistant = TotoroAssistant()
                # Register callback to sync assistant state with frontend
                self.assistant.register_state_callback(self.on_assistant_state_change)
                print("Assistant connected to frontend")
            except Exception as e:
                print(f"Failed to initialize assistant: {e}")
    
    def on_assistant_state_change(self, state):
        """Callback when assistant state changes"""
        self.set_state(state)
    
    def set_state(self, state):
        """Set the current visual state"""
        with self.state_lock:
            self.current_state = state
            print(f"Frontend state changed to: {state}")
    
    def get_state(self):
        """Get the current visual state"""
        with self.state_lock:
            return self.current_state
    
    def get_assistant_state(self):
        """Get state directly from assistant if available"""
        if self.assistant:
            return self.assistant.get_visual_state()
        return self.current_state
    
    def start_assistant_integration(self):
        """Start a background thread to monitor assistant state"""
        if not self.assistant:
            return
            
        def monitor_assistant():
            while True:
                try:
                    # Sync state from assistant to frontend
                    assistant_state = self.assistant.get_visual_state()
                    if assistant_state != self.current_state:
                        self.set_state(assistant_state)
                    
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error monitoring assistant: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=monitor_assistant, daemon=True)
        thread.start()
        print("Assistant integration started")

# Global frontend manager
frontend_manager = FrontendManager()

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
    """Get current assistant status"""
    # Get the most up-to-date state
    current_state = frontend_manager.get_assistant_state()
    
    return jsonify({
        'state': current_state,
        'assistant_available': ASSISTANT_AVAILABLE,
        'is_running': frontend_manager.assistant.is_running if frontend_manager.assistant else False,
        'timestamp': time.time()
    })

@app.route('/api/state/<state>')
def set_state(state):
    """Set assistant state"""
    valid_states = ['idle', 'awake', 'thinking', 'speaking']
    if state in valid_states:
        frontend_manager.set_state(state)
        
        # Also update assistant state if available
        if frontend_manager.assistant:
            frontend_manager.assistant.set_visual_state(state)
        
        return jsonify({'success': True, 'state': state})
    else:
        return jsonify({'success': False, 'error': f'Invalid state. Valid states: {valid_states}'}), 400

@app.route('/api/demo')
def start_demo():
    """Start demo mode with cycling states"""
    def demo_cycle():
        states = ['idle', 'awake', 'thinking', 'speaking']
        for _ in range(20):  # Run for 20 cycles
            for state in states:
                frontend_manager.set_state(state)
                if frontend_manager.assistant:
                    frontend_manager.assistant.set_visual_state(state)
                time.sleep(2)
    
    thread = threading.Thread(target=demo_cycle, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Demo mode started'})

@app.route('/api/command/<command>')
def send_command(command):
    """Send a command to the assistant"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        # Process the command (this will automatically update visual states)
        response = frontend_manager.assistant.process_command(command)
        return jsonify({
            'success': True, 
            'response': response,
            'state': frontend_manager.get_assistant_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🎭 Starting Totoro Frontend Server...")
    print("🌐 Frontend will be available at: http://localhost:5001")
    print("🔧 API endpoints:")
    print("   GET  /api/status - Get current state")
    print("   GET  /api/state/<state> - Set state (idle/awake/thinking/speaking)")
    print("   GET  /api/demo - Start demo mode")
    print("   GET  /api/command/<command> - Send command to assistant")
    print("\n🎬 Test the interface:")
    print("   http://localhost:5001 - Main interface")
    print("   http://localhost:5001?demo=true - Auto-demo mode")
    
    # Start assistant integration if available
    frontend_manager.start_assistant_integration()
    
    # Start the web server
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True) 