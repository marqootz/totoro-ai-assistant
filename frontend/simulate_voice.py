#!/usr/bin/env python3
"""
Voice Simulation Script
Simulates voice interactions to test the frontend visual states
"""

import requests
import time
import sys

def simulate_voice_interaction():
    """Simulate a complete voice interaction cycle"""
    base_url = "http://localhost:5001"
    
    print("🎤 Simulating voice interaction...")
    print("👀 Watch your browser at: http://localhost:5001")
    print()
    
    # Step 1: Idle state (listening for wake word)
    print("1️⃣ IDLE: Listening for wake word...")
    try:
        response = requests.get(f"{base_url}/api/state/idle")
        if response.status_code == 200:
            print("   🔵 Blue glow, gentle blinking")
        time.sleep(3)
    except:
        print("❌ Server not responding")
        return
    
    # Step 2: Awake state (wake word detected)
    print("2️⃣ AWAKE: Wake word detected!")
    try:
        response = requests.get(f"{base_url}/api/state/awake")
        if response.status_code == 200:
            print("   🟢 Green glow, alert eyes")
        time.sleep(2)
    except:
        print("❌ Error setting awake state")
        return
    
    # Step 3: Thinking state (processing command)
    print("3️⃣ THINKING: Processing your command...")
    try:
        response = requests.get(f"{base_url}/api/state/thinking")
        if response.status_code == 200:
            print("   🟠 Orange glow, rotating ring")
        time.sleep(4)
    except:
        print("❌ Error setting thinking state")
        return
    
    # Step 4: Speaking state (giving response)
    print("4️⃣ SPEAKING: Giving response...")
    try:
        response = requests.get(f"{base_url}/api/state/speaking")
        if response.status_code == 200:
            print("   🔴 Red glow, bouncing animation")
        time.sleep(3)
    except:
        print("❌ Error setting speaking state")
        return
    
    # Step 5: Back to idle
    print("5️⃣ IDLE: Back to listening...")
    try:
        response = requests.get(f"{base_url}/api/state/idle")
        if response.status_code == 200:
            print("   🔵 Back to calm state")
    except:
        print("❌ Error returning to idle")
        return
    
    print("\n✨ Voice interaction simulation complete!")
    print("🎭 This is how your frontend will look when you speak to Totoro!")

def continuous_simulation():
    """Run continuous voice simulations"""
    print("🔄 Starting continuous voice simulation...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            simulate_voice_interaction()
            print("\n⏱️  Waiting 5 seconds before next simulation...\n")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n👋 Simulation stopped!")

def test_server():
    """Test if the server is responding"""
    try:
        response = requests.get("http://localhost:5001/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is responding")
            print(f"📊 Current state: {data.get('state', 'unknown')}")
            print(f"🤖 Assistant available: {data.get('assistant_available', False)}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend server")
        print("   Make sure to run: python simple_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎭 Totoro Voice Interaction Simulator")
    print("=" * 40)
    
    # Test server connection
    if not test_server():
        sys.exit(1)
    
    print("\nWhat would you like to do?")
    print("1. Single voice interaction simulation")
    print("2. Continuous simulation (Ctrl+C to stop)")
    print("3. Just test server status")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            simulate_voice_interaction()
        elif choice == '2':
            continuous_simulation()
        elif choice == '3':
            print("✅ Server test complete")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 