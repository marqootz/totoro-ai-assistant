#!/usr/bin/env python3
"""
Enhanced Totoro Frontend Server
Provides proper visual feedback during command processing
"""

import os
import sys
import threading
import time
import asyncio
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path to access the assistant
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

class EnhancedFrontendManager:
    def __init__(self):
        self.current_state = 'loading'
        self.assistant = None
        self.state_lock = threading.Lock()
        self.loading_progress = 0
        self.loading_stage = "Starting up..."
        
        # Start assistant initialization
        self.initialize_assistant()
    
    def initialize_assistant(self):
        """Initialize assistant with progress tracking"""
        def initialize():
            self.set_loading_state("Importing modules...", 5)
            
            try:
                from src.assistant import TotoroAssistant
                self.set_loading_state("Modules imported successfully", 10)
                
                self.set_loading_state("Initializing neural models...", 15)
                self.assistant = TotoroAssistant()
                
                self.set_loading_state("Assistant ready!", 100)
                self.set_state('idle')
                
                # Register state callback
                self.assistant.register_state_callback(self.on_assistant_state_change)
                print("✅ Enhanced assistant ready with visual feedback!")
                
            except Exception as e:
                self.set_loading_state(f"Error: {e}", 0)
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
    
    def process_command_with_feedback(self, command):
        """Process command with proper visual feedback"""
        if not self.assistant:
            return {"error": "Assistant not available", "success": False}
        
        try:
            # Step 1: Show awake state (command received)
            self.set_state('awake')
            time.sleep(0.5)  # Brief awake state
            
            # Step 2: Show thinking state (processing)
            self.set_state('thinking')
            
            # Process the command
            response = self.assistant.process_command(command)
            
            # Step 3: Show speaking state (giving response)
            self.set_state('speaking')
            time.sleep(1.5)  # Speaking duration
            
            # Step 4: Return to idle
            self.set_state('idle')
            
            return {
                "response": response,
                "success": True,
                "state": "idle"
            }
            
        except Exception as e:
            self.set_state('error')
            time.sleep(1)
            self.set_state('idle')
            return {"error": str(e), "success": False}

# Global manager
frontend_manager = EnhancedFrontendManager()

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
    current_state = frontend_manager.get_state()
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
        return jsonify({'success': True, 'state': state})
    else:
        return jsonify({'success': False, 'error': f'Invalid state. Valid states: {valid_states}'}), 400

@app.route('/api/command/<command>')
def send_command_with_feedback(command):
    """Send command with proper visual feedback"""
    if not frontend_manager.assistant:
        loading_info = frontend_manager.get_loading_info()
        return jsonify({
            'success': False, 
            'error': 'Assistant not available', 
            'loading': loading_info
        }), 400
    
    # Process command with visual feedback
    result = frontend_manager.process_command_with_feedback(command)
    return jsonify(result)

@app.route('/api/demo')
def start_demo():
    """Enhanced demo with realistic timing"""
    if frontend_manager.current_state == 'loading':
        return jsonify({'success': False, 'message': 'Cannot start demo while loading'})
    
    def demo_cycle():
        # Simulate realistic interaction
        print("🎭 Starting enhanced demo...")
        
        # Wake word detected
        frontend_manager.set_state('awake')
        time.sleep(1)
        
        # Processing command
        frontend_manager.set_state('thinking')
        time.sleep(3)
        
        # Giving response
        frontend_manager.set_state('speaking')
        time.sleep(2)
        
        # Back to listening
        frontend_manager.set_state('idle')
        
        print("✅ Enhanced demo complete!")
    
    thread = threading.Thread(target=demo_cycle, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Enhanced demo started'})

@app.route('/api/voice/start')
def start_voice_listening():
    """Start voice listening mode"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        # Start continuous voice mode
        def start_voice_thread():
            frontend_manager.assistant.start_voice_mode()
        
        voice_thread = threading.Thread(target=start_voice_thread, daemon=True)
        voice_thread.start()
        
        return jsonify({
            'success': True, 
            'message': 'Voice listening started',
            'wake_word': frontend_manager.assistant.voice_recognizer.wake_word if frontend_manager.assistant.voice_recognizer else 'totoro'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/stop')
def stop_voice_listening():
    """Stop voice listening mode"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        frontend_manager.assistant.stop_voice_mode()
        frontend_manager.set_state('idle')
        return jsonify({'success': True, 'message': 'Voice listening stopped'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/wake_session')
def start_wake_session():
    """Start a single wake word session"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        def wake_session_thread():
            frontend_manager.set_state('idle')
            response = frontend_manager.assistant.start_wake_word_session()
            return response
        
        session_thread = threading.Thread(target=wake_session_thread, daemon=True)
        session_thread.start()
        
        return jsonify({
            'success': True, 
            'message': 'Wake word session started',
            'timeout': 30
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/status')
def get_voice_status():
    """Get voice system status"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        voice_pref = 'unknown'
        wake_word = 'totoro'
        
        # Safely get voice preference
        if hasattr(frontend_manager.assistant, 'tts') and frontend_manager.assistant.tts:
            voice_pref = getattr(frontend_manager.assistant.tts, 'voice_preference', 'unknown')
        
        # Safely get wake word
        if hasattr(frontend_manager.assistant, 'voice_recognizer') and frontend_manager.assistant.voice_recognizer:
            wake_word = getattr(frontend_manager.assistant.voice_recognizer, 'wake_word', 'totoro')
        
        return jsonify({
            'success': True,
            'is_running': frontend_manager.assistant.is_running,
            'wake_word': wake_word,
            'voice_preference': voice_pref,
            'microphone_available': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/debug')
def voice_debug_info():
    """Get detailed voice system debug information"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        debug_info = {
            'success': True,
            'timestamp': time.time(),
            'assistant_status': {
                'is_running': frontend_manager.assistant.is_running,
                'visual_state': frontend_manager.assistant.get_visual_state(),
            },
            'voice_recognizer_status': {},
            'tts_status': {},
            'microphone_info': {}
        }
        
        # Voice recognizer info
        if hasattr(frontend_manager.assistant, 'voice_recognizer') and frontend_manager.assistant.voice_recognizer:
            vr = frontend_manager.assistant.voice_recognizer
            debug_info['voice_recognizer_status'] = {
                'wake_word': getattr(vr, 'wake_word', 'unknown'),
                'is_listening': getattr(vr, 'is_listening', False),
                'microphone_available': vr.microphone is not None,
            }
            
            # Try to get microphone names
            try:
                import speech_recognition as sr
                mic_names = sr.Microphone.list_microphone_names()
                debug_info['microphone_info'] = {
                    'available_microphones': mic_names,
                    'count': len(mic_names)
                }
            except Exception as e:
                debug_info['microphone_info'] = {'error': str(e)}
        
        # TTS info
        if hasattr(frontend_manager.assistant, 'tts') and frontend_manager.assistant.tts:
            tts = frontend_manager.assistant.tts
            debug_info['tts_status'] = {
                'voice_preference': getattr(tts, 'voice_preference', 'unknown'),
                'coqui_available': hasattr(tts, 'coqui_tts') and tts.coqui_tts is not None,
                'system_available': hasattr(tts, 'system_available') and tts.system_available,
            }
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/test_quick')
def quick_voice_test():
    """Quick voice recognition test"""
    if not frontend_manager.assistant:
        return jsonify({'success': False, 'error': 'Assistant not available'}), 400
    
    try:
        # Test microphone access
        import speech_recognition as sr
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        # Quick ambient noise adjustment
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
        
        return jsonify({
            'success': True, 
            'message': 'Quick voice test completed',
            'energy_threshold': r.energy_threshold,
            'microphone_ready': True
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🎭 Starting Enhanced Totoro Frontend Server...")
    print("🌐 Frontend available at: http://localhost:5002")
    print("✨ Enhanced features:")
    print("   📊 Real-time loading progress")
    print("   🎨 Proper visual state transitions")
    print("   ⚡ Responsive command feedback")
    print("   🔄 Awake → Thinking → Speaking → Idle cycle")
    
    print(f"\n🎬 Enhanced experience: http://localhost:5002")
    
    # Start the web server on different port to avoid conflicts
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True) 