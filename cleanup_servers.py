#!/usr/bin/env python3
"""
Server Cleanup Script for Totoro Assistant
Kills existing servers and Flask instances to prevent port conflicts
"""

import subprocess
import time

def cleanup_servers():
    """Kill all existing Totoro servers and related processes"""
    print("🧹 TOTORO SERVER CLEANUP")
    print("=" * 40)
    
    # Ports commonly used by Totoro
    ports = [5000, 5001, 5002, 8000, 8080]
    killed_count = 0
    
    print("🔍 Checking for processes on common ports...")
    for port in ports:
        try:
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        try:
                            subprocess.run(['kill', pid], check=True)
                            print(f"   ✅ Killed process on port {port} (PID {pid})")
                            killed_count += 1
                        except subprocess.CalledProcessError:
                            print(f"   ⚠️  Could not kill PID {pid} on port {port}")
                            
        except Exception as e:
            print(f"   ⚠️  Error checking port {port}: {e}")
    
    print("\n🔍 Checking for Totoro server processes...")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                # Look for Totoro-related Python processes
                totoro_servers = [
                    'enhanced_server.py',
                    'simple_server.py', 
                    'voice_integrated_server.py',
                    'loading_aware_server.py',
                    'fast_voice_backend.py'
                ]
                
                if any(server in line for server in totoro_servers) and 'python' in line:
                    parts = line.split()
                    if len(parts) > 1:
                        try:
                            pid = parts[1]
                            subprocess.run(['kill', pid], check=True)
                            print(f"   ✅ Killed Totoro server (PID {pid})")
                            killed_count += 1
                        except:
                            pass
                            
    except Exception as e:
        print(f"   ⚠️  Error killing server processes: {e}")
    
    # Give processes time to terminate
    if killed_count > 0:
        print(f"\n⏳ Waiting for {killed_count} processes to terminate...")
        time.sleep(3)
    
    print(f"\n✅ Cleanup complete! Killed {killed_count} processes")
    print("🚀 Ready to start fresh servers")

if __name__ == "__main__":
    cleanup_servers() 