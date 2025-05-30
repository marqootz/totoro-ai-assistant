#!/usr/bin/env python3
"""
Test script for the Totoro Frontend
Demonstrates all the different animated states
"""

import requests
import time
import sys

BASE_URL = "http://localhost:5001"

def test_api():
    """Test if the API is responding"""
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            print("✅ API is responding")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the frontend server")
        print("   Make sure to run: cd frontend && python simple_server.py")
        return False

def set_state(state):
    """Set the face state"""
    try:
        response = requests.get(f"{BASE_URL}/api/state/{state}")
        if response.status_code == 200:
            print(f"✅ Set state to: {state}")
            return True
        else:
            print(f"❌ Failed to set state to {state}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error setting state: {e}")
        return False

def get_current_state():
    """Get the current state"""
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            return data.get('state', 'unknown')
        else:
            return 'unknown'
    except requests.exceptions.RequestException:
        return 'unknown'

def demo_states():
    """Demonstrate all states with descriptions"""
    states = [
        ('idle', 'Calm blue glow, gentle blinking - listening for wake word'),
        ('awake', 'Bright green glow, alert eyes - wake word detected!'),
        ('thinking', 'Orange glow, rotating ring - processing your command'),
        ('speaking', 'Red glow, bouncing animation - speaking response')
    ]
    
    print("\n🎭 Demonstrating Totoro Face States:")
    print("=" * 50)
    
    for state, description in states:
        print(f"\n🔄 Setting state: {state.upper()}")
        print(f"   {description}")
        
        if set_state(state):
            print(f"   👀 Check your browser at: {BASE_URL}")
            print("   ⏱️  Waiting 4 seconds...")
            time.sleep(4)
        else:
            print("   ❌ Failed to set state")
            break
    
    print(f"\n✨ Demo complete! Current state: {get_current_state()}")

def start_auto_demo():
    """Start automatic demo mode"""
    try:
        response = requests.get(f"{BASE_URL}/api/demo")
        if response.status_code == 200:
            print("🎬 Started automatic demo mode!")
            print("   The face will cycle through all states automatically")
            print(f"   Watch at: {BASE_URL}")
            return True
        else:
            print("❌ Failed to start demo mode")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error starting demo: {e}")
        return False

def main():
    print("🦙 Totoro Frontend Test Script")
    print("=" * 40)
    
    # Test API connection
    if not test_api():
        sys.exit(1)
    
    print(f"\n🌐 Frontend URL: {BASE_URL}")
    print(f"📊 Current state: {get_current_state()}")
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Manual state demo (step through each state)")
    print("2. Automatic demo (continuous cycling)")
    print("3. Set specific state")
    print("4. Just show current status")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            demo_states()
        elif choice == '2':
            start_auto_demo()
        elif choice == '3':
            print("\nAvailable states: idle, awake, thinking, speaking")
            state = input("Enter state: ").strip().lower()
            if state in ['idle', 'awake', 'thinking', 'speaking']:
                set_state(state)
                print(f"✅ Set to {state}. Check your browser!")
            else:
                print("❌ Invalid state")
        elif choice == '4':
            status_response = requests.get(f"{BASE_URL}/api/status")
            print(f"\n📊 Full status: {status_response.json()}")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 