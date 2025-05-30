#!/usr/bin/env python3
"""
Simple Status Monitor
Shows when Totoro is ready for voice commands
"""

import requests
import time
import sys

def check_system_status():
    """Check and display system readiness"""
    try:
        response = requests.get("http://localhost:5001/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            print("🎭 TOTORO SYSTEM STATUS")
            print("=" * 40)
            
            # Loading status
            loading = data.get('loading', {})
            if loading.get('is_loading'):
                print(f"🔄 LOADING: {loading.get('stage', 'Unknown')} ({loading.get('progress', 0)}%)")
                print("⏳ Status: NOT READY - Still loading neural models")
                return False
            else:
                print("✅ LOADING: Complete (100%)")
            
            # Assistant availability
            if data.get('assistant_available'):
                print("✅ NEURAL MODELS: Loaded and ready")
            else:
                print("❌ NEURAL MODELS: Not available")
                return False
            
            # Voice recognition status  
            if data.get('is_running'):
                print("🎤 VOICE RECOGNITION: ACTIVE (listening for wake word)")
                print("🌟 STATUS: FULLY READY FOR VOICE COMMANDS!")
                return True
            else:
                print("🔇 VOICE RECOGNITION: Not active")
                print("💡 ACTION NEEDED: Click 'Start Voice' button in browser")
                
            # Visual state
            state = data.get('state', 'unknown')
            state_colors = {
                'idle': '🔵 Blue (ready to listen)',
                'awake': '🟢 Green (wake word detected)', 
                'thinking': '🟠 Orange (processing)',
                'speaking': '🔴 Red (responding)',
                'loading': '🟣 Purple (loading)',
                'error': '⚠️ Red (error)'
            }
            print(f"🎨 VISUAL STATE: {state_colors.get(state, f'❓ {state}')}")
            
            print()
            print("🌐 Frontend: http://localhost:5001")
            
            return data.get('assistant_available') and not loading.get('is_loading')
            
        else:
            print("❌ Server not responding")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def monitor_until_ready():
    """Monitor status until system is ready"""
    print("🔍 Monitoring system status... (Press Ctrl+C to stop)")
    
    try:
        while True:
            ready = check_system_status()
            
            if ready:
                print("\n🎉 SYSTEM IS READY!")
                print("💡 Next steps:")
                print("   1. Open http://localhost:5001 in browser")
                print("   2. Click green 'Start Voice' button")
                print("   3. Say your wake word and watch the face react!")
                break
            else:
                print("⏳ Waiting 5 seconds before next check...")
                print()
                time.sleep(5)
                
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        monitor_until_ready()
    else:
        check_system_status() 