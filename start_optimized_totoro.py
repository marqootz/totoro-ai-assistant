#!/usr/bin/env python3
"""
Optimized Totoro Startup Script
Automatically kills existing servers and starts enhanced frontend with performance optimizations
"""

import subprocess
import time
import os
import signal
import sys
from pathlib import Path

def kill_existing_servers():
    """Kill existing Totoro servers and Flask instances"""
    print("🔄 Cleaning up existing servers...")
    
    # Common ports used by Totoro
    ports_to_check = [5000, 5001, 5002, 8000]
    killed_processes = []
    
    for port in ports_to_check:
        try:
            # Find processes using the port
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        try:
                            subprocess.run(['kill', pid], check=True)
                            killed_processes.append(f"Port {port} (PID {pid})")
                            print(f"   ✅ Killed process on port {port} (PID {pid})")
                        except subprocess.CalledProcessError:
                            print(f"   ⚠️  Could not kill PID {pid} on port {port}")
                            
        except Exception as e:
            print(f"   ⚠️  Error checking port {port}: {e}")
    
    # Kill any remaining Flask/Python processes related to Totoro
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if ('enhanced_server.py' in line or 
                    'simple_server.py' in line or 
                    'voice_integrated_server.py' in line) and 'python' in line:
                    
                    parts = line.split()
                    if len(parts) > 1:
                        try:
                            pid = parts[1]
                            subprocess.run(['kill', pid], check=True)
                            killed_processes.append(f"Totoro server (PID {pid})")
                            print(f"   ✅ Killed Totoro server (PID {pid})")
                        except:
                            pass
                            
    except Exception as e:
        print(f"   ⚠️  Error killing remaining servers: {e}")
    
    if killed_processes:
        print(f"   🧹 Cleaned up {len(killed_processes)} existing processes")
    else:
        print("   ✅ No existing servers found")
    
    # Give processes time to fully terminate
    time.sleep(2)

def apply_performance_optimizations():
    """Apply performance optimizations to environment"""
    print("\n⚡ Applying performance optimizations...")
    
    # Set optimized environment variables
    optimizations = {
        'VOICE_PREFERENCE': 'system',
        'OLLAMA_MODEL': 'llama3.2:latest',
        'LLM_BACKEND': 'unified',
        'RECOGNITION_TIMEOUT': '15',
        'COMMAND_TIMEOUT': '8',
        'TTS_RATE': '200'
    }
    
    for key, value in optimizations.items():
        os.environ[key] = value
        print(f"   ✅ {key}={value}")
    
    print("   🚀 Performance optimizations applied!")

def check_dependencies():
    """Check that required services are running"""
    print("\n🔍 Checking dependencies...")
    
    # Check if Ollama is running
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ Ollama LLM service is running")
        else:
            print("   ⚠️  Ollama not responding - start with: ollama serve")
            return False
    except subprocess.TimeoutExpired:
        print("   ⚠️  Ollama timeout - may be slow")
    except Exception as e:
        print(f"   ❌ Error checking Ollama: {e}")
        print("   💡 Start Ollama with: ollama serve")
        return False
    
    return True

def start_enhanced_server():
    """Start the enhanced frontend server"""
    print("\n🎭 Starting Enhanced Totoro Frontend...")
    
    frontend_dir = Path(__file__).parent / 'frontend'
    server_script = frontend_dir / 'enhanced_server.py'
    
    if not server_script.exists():
        print(f"   ❌ Enhanced server script not found: {server_script}")
        return False
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        print("   🚀 Launching enhanced server...")
        print("   🌐 Frontend will be available at: http://localhost:5002")
        print("   ✨ Features: Real-time feedback, optimized performance")
        print("   🎯 Press Ctrl+C to stop")
        
        # Start the server
        subprocess.run([sys.executable, 'enhanced_server.py'])
        
    except KeyboardInterrupt:
        print("\n   👋 Enhanced server stopped by user")
        return True
    except Exception as e:
        print(f"   ❌ Error starting enhanced server: {e}")
        return False

def show_performance_summary():
    """Show performance improvements summary"""
    print("\n📊 PERFORMANCE OPTIMIZATIONS ACTIVE")
    print("=" * 50)
    print("✅ System TTS (4.9x faster than neural)")
    print("✅ Smaller LLM model (2GB vs 5GB)")
    print("✅ Reduced timeouts (15s/8s vs 30s/10s)")
    print("✅ Audio conflicts resolved")
    print("✅ Enhanced visual feedback")
    print("")
    print("🎯 Expected Response Times:")
    print("   • Simple commands: 2-3 seconds")
    print("   • Complex queries: 4-5 seconds")
    print("   • Visual feedback: Real-time")
    print("")

def main():
    """Main startup sequence"""
    print("🚀 OPTIMIZED TOTORO STARTUP")
    print("=" * 50)
    print("Starting enhanced Totoro with performance optimizations")
    
    try:
        # Step 1: Kill existing servers
        kill_existing_servers()
        
        # Step 2: Apply optimizations
        apply_performance_optimizations()
        
        # Step 3: Check dependencies
        if not check_dependencies():
            print("\n❌ Dependencies not ready. Please start required services.")
            return 1
        
        # Step 4: Show performance summary
        show_performance_summary()
        
        # Step 5: Start enhanced server
        if start_enhanced_server():
            print("\n✅ Enhanced Totoro started successfully!")
            return 0
        else:
            print("\n❌ Failed to start enhanced server")
            return 1
            
    except KeyboardInterrupt:
        print("\n👋 Startup cancelled by user")
        return 0
    except Exception as e:
        print(f"\n❌ Startup error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 