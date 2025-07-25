#!/usr/bin/env python3
"""
Voice-Reactive Rings Startup Script
Launches both HTTP server and WebSocket backend
"""

import asyncio
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_existing_processes():
    """Kill any existing processes using ports 8000 or 8765"""
    try:
        logger.info("🔪 Checking for existing processes on ports 8000 and 8765...")
        result = subprocess.run(
            "lsof -i :8000,8765 | grep LISTEN | awk '{print $2}' | xargs kill -9",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            logger.info(f"Killed processes: {result.stdout.strip()}")
        else:
            logger.info("No existing processes found")
    except Exception as e:
        logger.warning(f"Could not kill existing processes: {e}")

def check_requirements():
    """Check if required packages are installed"""
    required_packages = {
        'websockets': 'websockets',
        'numpy': 'numpy',
        'torch': 'torch',
        'TTS': 'TTS',
        'pygame': 'pygame'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            logger.info(f"✅ {package} available")
        except ImportError:
            logger.error(f"❌ {package} not found")
            missing_packages.append(pip_name)
    
    if missing_packages:
        logger.error("\n💡 Install missing packages with:")
        logger.error(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def launch_servers():
    """Launch the voice-reactive rings system"""
    print("\n🎭 VOICE-REACTIVE MORPHING RINGS")
    print("=" * 50)
    
    # Kill any existing processes first
    kill_existing_processes()
    
    if not check_requirements():
        return
    
    logger.info("\n🚀 Starting servers...")
    
    # Start the voice ring integration server
    try:
        from voice_ring_integration import VoiceRingServer, create_simple_http_server
        
        # Create HTTP server for static files
        create_simple_http_server()
        
        # Create and start the voice ring server
        server = VoiceRingServer()
        
        async def run_server():
            try:
                websocket_server = await server.start_server()
                logger.info("✅ Server started successfully")
                logger.info("📱 Open your browser to: http://localhost:8000/voice-reactive-rings.html")
                
                # Keep the server running
                await websocket_server.wait_closed()
            except Exception as e:
                logger.error(f"Server error: {e}")
                raise
        
        # Run the server
        asyncio.run(run_server())
        
    except ImportError as e:
        logger.error(f"❌ Could not import voice ring integration: {e}")
        logger.error("\n💡 Make sure all dependencies are installed:")
        logger.error("pip install -r requirements-voice-rings.txt")
        
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down...")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    launch_servers() 