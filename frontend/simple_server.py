#!/usr/bin/env python3
"""
Simple Totoro Frontend Server (Standalone)
A lightweight version that doesn't require the full assistant
"""

import time
import threading
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

class SimpleFrontendManager:
    def __init__(self):
        self.current_state = 'idle'
        self.state_lock = threading.Lock()
    
    def set_state(self, state):
        """Set the current visual state"""
        with self.state_lock:
            self.current_state = state
            print(f"State changed to: {state}")
    
    def get_state(self):
        """Get the current visual state"""
        with self.state_lock:
            return self.current_state

# Global frontend manager
frontend_manager = SimpleFrontendManager()

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
    return jsonify({
        'state': frontend_manager.get_state(),
        'assistant_available': False,
        'is_running': False,
        'timestamp': time.time()
    })

@app.route('/api/state/<state>')
def set_state(state):
    """Set state manually"""
    valid_states = ['idle', 'awake', 'thinking', 'speaking']
    if state in valid_states:
        frontend_manager.set_state(state)
        return jsonify({'success': True, 'state': state})
    else:
        return jsonify({'success': False, 'error': f'Invalid state. Valid states: {valid_states}'}), 400

@app.route('/api/demo')
def start_demo():
    """Start demo mode with cycling states"""
    def demo_cycle():
        states = ['idle', 'awake', 'thinking', 'speaking']
        for cycle in range(5):  # Run for 5 cycles
            for state in states:
                frontend_manager.set_state(state)
                time.sleep(3)
    
    thread = threading.Thread(target=demo_cycle, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Demo mode started - cycling through states'})

if __name__ == '__main__':
    print("🎭 Starting Simple Totoro Frontend Server...")
    print("🌐 Frontend available at: http://localhost:5001")
    print("🔧 API endpoints:")
    print("   GET  /api/status - Get current state")
    print("   GET  /api/state/<state> - Set state (idle/awake/thinking/speaking)")
    print("   GET  /api/demo - Start demo mode")
    print("\n🎬 Test the interface:")
    print("   http://localhost:5001 - Main interface")
    print("   http://localhost:5001?demo=true - Auto-demo mode")
    print("\n✨ This is a standalone version for testing the frontend!")
    
    # Start the web server
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True) 