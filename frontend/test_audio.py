#!/usr/bin/env python3
"""
Audio Test Tool for Totoro Assistant
Helps identify source of echo in TTS responses
"""

import subprocess
import time
import sys
import os

def test_system_tts():
    """Test system TTS for echo"""
    print("🔊 Testing system TTS...")
    
    # Test 1: Simple system say
    print("1. Testing system 'say' command...")
    subprocess.run(['say', 'Testing system text to speech, number one'])
    time.sleep(2)
    
    # Test 2: Multiple rapid calls (to check for overlap)
    print("2. Testing rapid TTS calls...")
    subprocess.Popen(['say', 'First message'])
    time.sleep(0.5)
    subprocess.Popen(['say', 'Second message'])
    time.sleep(3)

def check_audio_output():
    """Check current audio output device"""
    print("\n🎧 Checking audio output...")
    
    try:
        # Get current audio output
        result = subprocess.run(['osascript', '-e', 
                               'tell application "System Events" to get the value of slider "output volume" of tab "Output" of pane "Sound" of application process "System Preferences"'],
                              capture_output=True, text=True)
        print(f"System volume level detected")
        
        # Check if multiple audio apps are running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        audio_apps = []
        for line in result.stdout.split('\n'):
            if any(app in line.lower() for app in ['spotify', 'discord', 'zoom', 'teams', 'music']):
                if 'grep' not in line and line.strip():
                    audio_apps.append(line.split()[-1])
        
        if audio_apps:
            print(f"⚠️ Found other audio apps: {', '.join(set(audio_apps))}")
            print("These might interfere with TTS")
        else:
            print("✅ No conflicting audio apps detected")
            
    except Exception as e:
        print(f"Error checking audio: {e}")

def test_neural_tts():
    """Test if neural TTS is causing the echo"""
    print("\n🧠 Testing neural TTS configuration...")
    
    # Check if we can import the assistant
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from src.config import Config
        
        print("✅ Config imported successfully")
        
        # Check TTS settings
        if hasattr(Config, 'USE_NEURAL_TTS'):
            print(f"Neural TTS enabled: {Config.USE_NEURAL_TTS}")
        if hasattr(Config, 'TTS_ENGINE'):
            print(f"TTS Engine: {Config.TTS_ENGINE}")
        if hasattr(Config, 'VOICE_MODEL'):
            print(f"Voice Model: {Config.VOICE_MODEL}")
            
    except Exception as e:
        print(f"❌ Error checking TTS config: {e}")

def suggest_echo_fixes():
    """Suggest specific fixes for echo issues"""
    print("\n🔧 ECHO DIAGNOSIS & FIXES:")
    print("=" * 40)
    
    print("\n📊 LIKELY CAUSES:")
    print("1. **Multiple TTS Engines**: Neural + System TTS both active")
    print("2. **Audio Buffering**: TTS audio being buffered and replayed")
    print("3. **SiriTTS Conflicts**: Multiple SiriTTS processes (found 16!)")
    print("4. **Audio App Interference**: Other apps using audio system")
    
    print("\n⚡ IMMEDIATE SOLUTIONS:")
    print("1. **Kill Siri TTS processes**:")
    print("   pkill -f 'SiriTTS'")
    print("   # This should reduce the 16 TTS processes")
    
    print("2. **Use single TTS engine**:")
    print("   # Edit config to disable either neural OR system TTS")
    
    print("3. **Test TTS isolation**:")
    print("   python -c \"import subprocess; subprocess.run(['say', 'test'])\"")
    
    print("4. **Check audio exclusivity**:")
    print("   # Close Discord, Spotify, Zoom, etc.")
    
    print("\n🎭 TEST WITH ENHANCED FRONTEND:")
    print("• Visual feedback now works: Awake → Thinking → Speaking → Idle")
    print("• Test at: http://localhost:5002")
    print("• Watch visual states during command processing")

def main():
    print("🎵 Totoro Audio Echo Test")
    print("=" * 30)
    
    test_system_tts()
    check_audio_output()
    test_neural_tts()
    suggest_echo_fixes()
    
    print(f"\n🌐 Enhanced Frontend: http://localhost:5002")
    print("✨ Visual feedback is now working!")
    print("🔧 Focus on fixing the audio echo next")

if __name__ == "__main__":
    main() 