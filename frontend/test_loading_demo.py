#!/usr/bin/env python3
"""
Loading Demo Script
Simulates loading progress for frontend testing
"""

import requests
import time
import sys

def simulate_loading_progress():
    """Simulate neural model loading progress"""
    base_url = "http://localhost:5001"
    
    print("🎭 Simulating Neural Model Loading Progress...")
    print("👀 Watch your browser at: http://localhost:5001")
    print()
    
    # Set to loading state
    try:
        response = requests.get(f"{base_url}/api/state/loading")
        if response.status_code != 200:
            print("❌ Server not responding")
            return
    except:
        print("❌ Server not responding")
        return
    
    # Simulate different loading stages
    stages = [
        ("Starting up...", 5),
        ("Importing modules...", 10),
        ("Loading PyTorch...", 20),
        ("Initializing neural models...", 30),
        ("Loading TTS models...", 50),
        ("Warming up neural networks...", 70),
        ("Finalizing initialization...", 90),
        ("Assistant ready!", 100)
    ]
    
    for stage, progress in stages:
        print(f"📊 {stage} ({progress}%)")
        
        # In a real implementation, this would be updated by the server
        # For demo purposes, we'll just show the visual progression
        
        time.sleep(2)
    
    # Switch to idle state when done
    print("\n✅ Loading complete! Switching to idle state...")
    try:
        response = requests.get(f"{base_url}/api/state/idle")
        print("🔵 Now in idle state - ready for voice commands!")
    except:
        print("❌ Error switching to idle")

def test_all_states():
    """Test all visual states including loading"""
    base_url = "http://localhost:5001"
    
    print("🎨 Testing All Visual States...")
    print("👀 Watch your browser at: http://localhost:5001")
    print()
    
    states = [
        ("loading", "🟣 Loading state - purple glow with progress"),
        ("idle", "🔵 Idle state - blue glow, gentle breathing"),
        ("awake", "🟢 Awake state - green glow, alert eyes"),
        ("thinking", "🟠 Thinking state - orange glow, rotating ring"),
        ("speaking", "🔴 Speaking state - red glow, bouncing"),
        ("error", "⚠️ Error state - red warning indicators")
    ]
    
    for state, description in states:
        print(f"{description}")
        try:
            response = requests.get(f"{base_url}/api/state/{state}")
            if response.status_code == 200:
                print(f"   ✅ {state.title()} state activated")
            else:
                print(f"   ❌ Failed to set {state} state")
        except:
            print(f"   ❌ Server error for {state} state")
        
        time.sleep(3)
    
    print("\n🎉 All states tested!")

def check_real_loading_progress():
    """Check actual loading progress from the server"""
    base_url = "http://localhost:5001"
    
    print("📊 Monitoring Real Loading Progress...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            try:
                response = requests.get(f"{base_url}/api/status")
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('loading', {}).get('is_loading'):
                        loading = data['loading']
                        print(f"🔄 {loading['stage']} ({loading['progress']}%)")
                    else:
                        print(f"✅ Loading complete! State: {data.get('state', 'unknown')}")
                        if data.get('assistant_available'):
                            print("🎤 Assistant is ready for voice commands!")
                            break
                        
                else:
                    print("❌ Server error")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped!")

def main():
    print("🎭 Totoro Loading Progress Demo")
    print("=" * 40)
    
    print("\nWhat would you like to test?")
    print("1. Simulate loading progress (demo)")
    print("2. Test all visual states")
    print("3. Monitor real loading progress")
    print("4. Quick loading demo")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            simulate_loading_progress()
        elif choice == '2':
            test_all_states()
        elif choice == '3':
            check_real_loading_progress()
        elif choice == '4':
            requests.get("http://localhost:5001/api/state/loading")
            time.sleep(3)
            requests.get("http://localhost:5001/api/state/idle")
            print("✅ Quick loading demo complete!")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 