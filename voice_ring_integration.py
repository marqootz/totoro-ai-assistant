#!/usr/bin/env python3
"""
Voice-Reactive Rings Integration
Connects the morphing rings interface with Totoro's voice capabilities
"""

import asyncio
import json
import logging
import time
import threading
from typing import Dict, Any, Optional
import websockets
import queue
from dataclasses import dataclass
from enum import Enum
import os

# Import your existing voice components
try:
    from src.voice import VoiceRecognizer, TextToSpeech
    from src.assistant import TotoroAssistant
    from src.config import Config
except ImportError:
    print("⚠️ Totoro voice modules not found. Using demo mode.")
    VoiceRecognizer = None
    TextToSpeech = None
    TotoroAssistant = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RingState(Enum):
    IDLE = "idle"
    LISTENING = "listening" 
    THINKING = "thinking"
    SPEAKING = "speaking"

@dataclass
class VoiceEvent:
    event_type: str
    data: Dict[str, Any]
    timestamp: float

class VoiceRingServer:
    """WebSocket server that bridges voice processing with ring animations"""
    
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        
        # Voice components
        self.voice_recognizer = None
        self.tts = None
        self.assistant = None
        
        # State management
        self.current_state = RingState.IDLE
        self.is_listening = False
        self.is_speaking = False
        self.is_thinking = False
        
        # Event queue for processing
        self.event_queue = queue.Queue()
        self.audio_data_queue = queue.Queue()
        
        # Initialize voice systems
        self.init_voice_systems()
        
    def init_voice_systems(self):
        """Initialize voice recognition and TTS systems"""
        try:
            if VoiceRecognizer:
                logger.info("🎤 Initializing voice recognizer...")
                self.voice_recognizer = VoiceRecognizer(
                    wake_word="totoro",
                    callback=self.on_voice_command
                )
                
            if TextToSpeech:
                logger.info("🗣️ Initializing TTS system...")
                self.tts = TextToSpeech(voice_preference="coqui")
                
            if TotoroAssistant:
                logger.info("🤖 Initializing AI assistant...")
                self.assistant = TotoroAssistant()
                
            logger.info("✅ Voice systems initialized successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize voice systems: {e}")
            logger.info("Running in demo mode without voice integration")
    
    async def register_client(self, websocket):
        """Handle new WebSocket client connection"""
        try:
            print("DEBUG: register_client CALLED with websocket")
            self.clients.add(websocket)
            logger.info(f"📱 Client connected. Total clients: {len(self.clients)}")
            
            # Send initial state
            await self.send_to_client(websocket, {
                "type": "state_update",
                "state": self.current_state.value,
                "timestamp": time.time()
            })
            
            try:
                async for message in websocket:
                    try:
                        await self.handle_client_message(websocket, message)
                    except Exception as e:
                        logger.error(f"Error handling client message: {e}")
                        await self.send_to_client(websocket, {
                            "type": "error",
                            "message": f"Error processing message: {str(e)}",
                            "timestamp": time.time()
                        })
            except websockets.exceptions.ConnectionClosed as e:
                logger.info(f"Client disconnected normally: {e.code} {e.reason}")
            except Exception as e:
                logger.error(f"Unexpected error in client connection: {e}")
        finally:
            self.clients.remove(websocket)
            logger.info(f"📱 Client disconnected. Total clients: {len(self.clients)}")
    
    async def handle_client_message(self, websocket, message):
        """Handle incoming messages from clients"""
        try:
            data = json.loads(message)
            command = data.get("command")
            
            if command == "start_listening":
                await self.start_listening()
            elif command == "stop_listening":
                await self.stop_listening()
            elif command == "speak_text":
                text = data.get("text", "")
                await self.speak_text(text)
            elif command == "stop_speaking":
                await self.stop_speaking()
            elif command == "test_thinking":
                await self.test_thinking()
            elif command == "get_status":
                await self.send_status_update(websocket)
            else:
                logger.warning(f"Unknown command: {command}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from client")
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    async def send_to_client(self, websocket, data):
        """Send data to a specific client"""
        try:
            await websocket.send(json.dumps(data))
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Client disconnected during send")
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
    
    async def broadcast_to_all_clients(self, data):
        """Broadcast data to all connected clients"""
        if not self.clients:
            return
            
        # Send to all clients concurrently
        await asyncio.gather(
            *[self.send_to_client(client, data) for client in self.clients],
            return_exceptions=True
        )
    
    async def set_state(self, new_state: RingState):
        """Update the current state and notify clients"""
        if self.current_state == new_state:
            return
            
        old_state = self.current_state
        self.current_state = new_state
        
        logger.info(f"🔄 State change: {old_state.value} → {new_state.value}")
        
        # Broadcast state change to all clients
        await self.broadcast_to_all_clients({
            "type": "state_change",
            "old_state": old_state.value,
            "new_state": new_state.value,
            "timestamp": time.time()
        })
    
    async def start_listening(self):
        """Start voice recognition"""
        if self.is_listening:
            return
            
        logger.info("🎤 Starting voice recognition...")
        
        try:
            if self.voice_recognizer:
                # Start voice recognition in background thread
                threading.Thread(
                    target=self._voice_recognition_worker,
                    daemon=True
                ).start()
                
                # Wait a moment for the recognizer to start
                await asyncio.sleep(0.5)
                
                # Start listening for wake word
                if self.voice_recognizer.listen_for_wake_word(timeout=30):
                    logger.info("Wake word detected!")
                    # Listen for command
                    command = self.voice_recognizer.listen_for_command(timeout=10)
                    if command:
                        await self.process_voice_command(command)
                    else:
                        await self.speak_text("I didn't catch that. Could you try again?")
            
            self.is_listening = True
            await self.set_state(RingState.LISTENING)
            
            await self.broadcast_to_all_clients({
                "type": "listening_started",
                "timestamp": time.time()
            })
            
        except Exception as e:
            logger.error(f"Error starting voice recognition: {e}")
            await self.broadcast_to_all_clients({
                "type": "error",
                "message": f"Failed to start listening: {e}",
                "timestamp": time.time()
            })
    
    async def stop_listening(self):
        """Stop voice recognition"""
        if not self.is_listening:
            return
            
        logger.info("🔇 Stopping voice recognition...")
        
        self.is_listening = False
        
        if self.voice_recognizer:
            self.voice_recognizer.stop_listening()
        
        await self.set_state(RingState.IDLE)
        
        await self.broadcast_to_all_clients({
            "type": "listening_stopped",
            "timestamp": time.time()
        })
    
    def _voice_recognition_worker(self):
        """Background worker for voice recognition"""
        try:
            if self.voice_recognizer:
                self.voice_recognizer.start_listening()
        except Exception as e:
            logger.error(f"Voice recognition worker error: {e}")
    
    def on_voice_command(self, command: str):
        """Callback for when voice command is recognized"""
        logger.info(f"🗣️ Voice command received: '{command}'")
        
        # Queue the voice event for async processing
        event = VoiceEvent(
            event_type="voice_command",
            data={"transcript": command},
            timestamp=time.time()
        )
        self.event_queue.put(event)
    
    async def process_voice_command(self, transcript: str):
        """Process a voice command with AI assistance"""
        await self.broadcast_to_all_clients({
            "type": "speech_recognized",
            "transcript": transcript,
            "timestamp": time.time()
        })
        
        # Enter thinking state
        await self.set_state(RingState.THINKING)
        self.is_thinking = True
        
        try:
            # Process with AI assistant if available
            if self.assistant:
                logger.info("🤖 Processing with AI assistant...")
                
                # Simulate thinking time for better UX
                thinking_time = 1.0 + len(transcript.split()) * 0.1  # Dynamic thinking time
                await asyncio.sleep(min(thinking_time, 3.0))
                
                response = await self._get_ai_response(transcript)
            else:
                # Fallback demo response with echo
                logger.info("⚠️ AI assistant not available, using echo mode")
                await asyncio.sleep(1.0)
                response = f"I heard you say: {transcript}"
            
            self.is_thinking = False
            
            # Speak the response
            await self.speak_text(response)
            
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            self.is_thinking = False
            await self.set_state(RingState.LISTENING if self.is_listening else RingState.IDLE)
            
            # Provide a fallback response even if there's an error
            await self.speak_text("I'm having trouble processing that right now. Could you try again?")
            
            await self.broadcast_to_all_clients({
                "type": "error",
                "message": f"Error processing command: {e}",
                "timestamp": time.time()
            })
    
    async def _get_ai_response(self, text: str) -> str:
        """Get AI response (async wrapper for sync AI call)"""
        try:
            # Run AI processing in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                self.assistant.process_command,
                text
            )
            return response
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            return f"I'm sorry, I had trouble processing that. Could you try rephrasing?"
    
    async def speak_text(self, text: str):
        """Speak text using TTS with ring animation"""
        if self.is_speaking:
            logger.warning("Already speaking, cancelling previous speech")
            await self.stop_speaking()
        
        logger.info(f"🗣️ Speaking: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        self.is_speaking = True
        await self.set_state(RingState.SPEAKING)
        
        await self.broadcast_to_all_clients({
            "type": "speech_started",
            "text": text,
            "timestamp": time.time()
        })
        
        try:
            if self.tts:
                # Run TTS in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                success = await loop.run_in_executor(
                    None,
                    self.tts.speak,
                    text
                )
                
                if success:
                    logger.info("✅ TTS completed successfully")
                else:
                    logger.error("❌ TTS failed, trying system TTS")
                    # Fallback to system TTS
                    try:
                        import pyttsx3
                        engine = pyttsx3.init()
                        engine.say(text)
                        engine.runAndWait()
                        logger.info("✅ System TTS completed successfully")
                    except Exception as e:
                        logger.error(f"System TTS failed: {e}")
                        # Last resort: use simple text-to-speech
                        try:
                            import os
                            os.system(f'say "{text}"')
                            logger.info("✅ System say command completed successfully")
                        except Exception as e:
                            logger.error(f"System say command failed: {e}")
            else:
                # Demo mode - simulate speaking time
                logger.info("⚠️ TTS not available, using simulated speech")
                speaking_time = max(2.0, len(text.split()) * 0.3)
                await asyncio.sleep(speaking_time)
            
            self.is_speaking = False
            await self.set_state(RingState.LISTENING if self.is_listening else RingState.IDLE)
            
            await self.broadcast_to_all_clients({
                "type": "speech_ended",
                "timestamp": time.time()
            })
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            self.is_speaking = False
            await self.set_state(RingState.LISTENING if self.is_listening else RingState.IDLE)
            
            await self.broadcast_to_all_clients({
                "type": "error",
                "message": f"TTS error: {e}",
                "timestamp": time.time()
            })
    
    async def stop_speaking(self):
        """Stop current TTS"""
        if not self.is_speaking:
            return
            
        logger.info("🛑 Stopping speech...")
        
        # Note: Stopping TTS mid-speech is tricky and depends on the TTS system
        # For now, we'll just update the state
        self.is_speaking = False
        await self.set_state(RingState.LISTENING if self.is_listening else RingState.IDLE)
        
        await self.broadcast_to_all_clients({
            "type": "speech_stopped",
            "timestamp": time.time()
        })
    
    async def test_thinking(self):
        """Test thinking animation"""
        logger.info("🧠 Testing thinking animation...")
        
        await self.set_state(RingState.THINKING)
        await asyncio.sleep(3.0)
        await self.set_state(RingState.LISTENING if self.is_listening else RingState.IDLE)
    
    async def send_status_update(self, websocket):
        """Send current status to a client"""
        status = {
            "type": "status_update",
            "state": self.current_state.value,
            "is_listening": self.is_listening,
            "is_speaking": self.is_speaking,
            "is_thinking": self.is_thinking,
            "voice_available": self.voice_recognizer is not None,
            "tts_available": self.tts is not None,
            "ai_available": self.assistant is not None,
            "timestamp": time.time()
        }
        
        await self.send_to_client(websocket, status)
    
    async def event_processor(self):
        """Process queued events asynchronously"""
        while True:
            try:
                # Check for events with timeout
                try:
                    event = self.event_queue.get(timeout=0.1)
                    
                    if event.event_type == "voice_command":
                        await self.process_voice_command(event.data["transcript"])
                    
                    self.event_queue.task_done()
                    
                except queue.Empty:
                    pass
                
                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logger.error(f"Event processor error: {e}")
                await asyncio.sleep(1.0)
    
    async def start_server(self):
        print("DEBUG: Starting websockets.serve with handler:", self.register_client)
        logger.info(f"🚀 Starting Voice-Reactive Rings server on {self.host}:{self.port}")
        
        # Start event processor
        asyncio.create_task(self.event_processor())
        
        # Start WebSocket server with proper error handling
        try:
            server = await websockets.serve(
                self.register_client,
                self.host,
                self.port,
                ping_interval=20,  # Send ping every 20 seconds
                ping_timeout=10,   # Wait 10 seconds for pong response
                close_timeout=5,   # Wait 5 seconds for clean close
                max_size=2**20,    # 1MB max message size
                max_queue=32,      # Max number of queued messages
                compression=None   # Disable compression for better performance
            )
            
            logger.info("✅ Server started successfully")
            logger.info(f"📱 Open your browser to: http://{self.host}:{8000}/voice-reactive-rings.html")
            logger.info("🎤 Voice commands will be processed and sent to connected clients")
            
            return server
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise

def create_simple_http_server():
    """Create a simple HTTP server to serve the HTML files"""
    import http.server
    import socketserver
    import threading
    import json
    
    # Change to the frontend directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'frontend'))
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Handle API endpoints
            if self.path.startswith('/api/'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                if self.path == '/api/status':
                    response = {
                        'status': 'running',
                        'timestamp': time.time()
                    }
                else:
                    response = {
                        'error': 'Not found',
                        'path': self.path
                    }
                
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Handle static files
            if self.path == '/':
                self.path = '/voice-reactive-rings.html'
            elif not self.path.startswith('/'):
                self.path = '/' + self.path
                
            return super().do_GET()
    
    def run_server():
        with socketserver.TCPServer(("", 8000), Handler) as httpd:
            logger.info("📁 HTTP server running on http://localhost:8000")
            httpd.serve_forever()
    
    threading.Thread(target=run_server, daemon=True).start()

async def main():
    """Main function to run the voice-reactive rings server"""
    print("🎭 VOICE-REACTIVE MORPHING RINGS SERVER")
    print("=" * 50)
    
    # Create HTTP server for static files
    create_simple_http_server()
    
    # Create and start the voice ring server
    server = VoiceRingServer()
    
    try:
        websocket_server = await server.start_server()
        await websocket_server.wait_closed()
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        if 'websocket_server' in locals():
            websocket_server.close()
            await websocket_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main()) 