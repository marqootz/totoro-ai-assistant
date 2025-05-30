#!/usr/bin/env python3
"""
Totoro Loading-Aware Frontend Server
Shows real-time neural model loading progress
"""

import os
import sys
import threading
import time
import re
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import signal

# Add parent directory to path to access the assistant
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

class LoadingAwareManager:
    def __init__(self):
        self.current_state = 'initializing'
        self.assistant = None
        self.state_lock = threading.Lock()
        self.loading_progress = 0
        self.loading_stage = "Starting up..."
        self.assistant_process = None
        
        # Start assistant initialization in background
        self.start_assistant_initialization()
    
    def start_assistant_initialization(self):
        """Start assistant initialization with progress tracking"""
        def initialize():
            self.set_loading_state("Importing modules...", 5)
            
            try:
                # Import with progress tracking
                from src.assistant import TotoroAssistant
                self.set_loading_state("Modules imported successfully", 10)
                
                # Initialize with progress tracking
                self.set_loading_state("Initializing neural models...", 15)
                
                # This is where the slow loading happens
                self.assistant = TotoroAssistant()
                
                self.set_loading_state("Assistant ready!", 100)
                self.set_state('idle')
                
                # Register state callback
                self.assistant.register_state_callback(self.on_assistant_state_change)
                print("✅ Assistant fully initialized and ready for voice!")
                
            except ImportError as e:
                self.set_loading_state(f"Import failed: {e}", 0)
                self.set_state('error')
            except Exception as e:
                self.set_loading_state(f"Initialization failed: {e}", 0) 
                self.set_state('error')
        
        thread = threading.Thread(target=initialize, daemon=True)
        thread.start()
    
    def set_loading_state(self, stage, progress):
        """Update loading progress"""
        with self.state_lock:
            self.loading_stage = stage
            self.loading_progress = progress
            if progress < 100:
                self.current_state = 'loading'
            print(f"🔄 {stage} ({progress}%)")
    
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
    
    def get_loading_info(self):
        """Get loading progress information"""
        with self.state_lock:
            return {
                'stage': self.loading_stage,
                'progress': self.loading_progress,
                'is_loading': self.current_state == 'loading'
            }
    
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
            return "Assistant not available - still loading"
        
        try:
            return self.assistant.process_command(command)
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            return f"Error: {e}"

# Global manager
frontend_manager = LoadingAwareManager()

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
    """Get current status with loading information"""
    current_state = frontend_manager.get_assistant_state()
    loading_info = frontend_manager.get_loading_info()
    
    return jsonify({
        'state': current_state,
        'assistant_available': frontend_manager.assistant is not None,
        'is_running': frontend_manager.assistant.is_running if frontend_manager.assistant else False,
        'loading': loading_info,
        'timestamp': time.time()
    })

@app.route('/api/state/<state>')
def set_state(state):
    """Set state manually"""
    valid_states = ['idle', 'awake', 'thinking', 'speaking', 'loading', 'error']
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
    if frontend_manager.current_state == 'loading':
        return jsonify({'success': False, 'message': 'Cannot start demo while loading'})
    
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
        loading_info = frontend_manager.get_loading_info()
        return jsonify({
            'success': False, 
            'error': 'Assistant not available', 
            'loading': loading_info
        }), 400
    
    try:
        response = frontend_manager.process_command(command)
        return jsonify({
            'success': True, 
            'response': response,
            'state': frontend_manager.get_assistant_state()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start_voice')
def start_voice_listening():
    """Start voice recognition"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        if hasattr(frontend_manager.assistant, 'start_listening'):
            frontend_manager.assistant.start_listening()
            return jsonify({'success': True, 'message': 'Voice recognition started'})
        elif hasattr(frontend_manager.assistant, 'run'):
            # Start the assistant main loop in background
            def start_assistant():
                frontend_manager.assistant.run()
            
            thread = threading.Thread(target=start_assistant, daemon=True)
            thread.start()
            return jsonify({'success': True, 'message': 'Assistant started listening'})
        else:
            return jsonify({'success': False, 'error': 'Assistant does not support voice activation'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stop_voice')
def stop_voice_listening():
    """Stop voice recognition"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        if hasattr(frontend_manager.assistant, 'stop_listening'):
            frontend_manager.assistant.stop_listening()
            return jsonify({'success': True, 'message': 'Voice recognition stopped'})
        else:
            return jsonify({'success': False, 'error': 'Assistant does not support voice stopping'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🔄 Starting Loading-Aware Totoro Frontend Server...")
    print("🌐 Frontend available at: http://localhost:5001")
    print("📊 Real-time loading progress will be displayed")
    print("🔧 API endpoints:")
    print("   GET  /api/status - Get current state with loading info")
    print("   GET  /api/state/<state> - Set state manually")
    print("   GET  /api/demo - Start demo mode (when loaded)")
    print("   GET  /api/command/<command> - Send command to assistant")
    print("   GET  /api/start_voice - Start voice recognition")
    print("   GET  /api/stop_voice - Stop voice recognition")
    
    print(f"\n🎬 Watch loading progress: http://localhost:5001")
    
    # Start the web server
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True) 