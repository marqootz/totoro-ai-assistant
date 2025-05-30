#!/usr/bin/env python3
"""
Audio Echo Fix for Totoro Assistant
Diagnoses and fixes double voice response issues
"""

import subprocess
import sys
import os

def check_audio_processes():
    """Check for multiple audio/TTS processes"""
    print("🎵 Checking for conflicting audio processes...")
    
    try:
        # Check for TTS processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        tts_processes = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['tts', 'speech', 'say', 'espeak', 'sirittsd']):
                if 'grep' not in line and line.strip():
                    tts_processes.append(line)
        
        if tts_processes:
            print(f"Found {len(tts_processes)} TTS-related processes:")
            for proc in tts_processes[:5]:  # Show first 5
                print(f"   📢 {proc.split()[1]}: {proc.split()[-1] if proc.split() else 'unknown'}")
            if len(tts_processes) > 5:
                print(f"   ... and {len(tts_processes) - 5} more")
        else:
            print("✅ No conflicting TTS processes found")
            
    except Exception as e:
        print(f"❌ Error checking processes: {e}")

def check_audio_config():
    """Check system audio configuration"""
    print("\n🔊 Checking audio configuration...")
    
    try:
        # Check default audio device
        result = subprocess.run(['system_profiler', 'SPAudioDataType'], 
                              capture_output=True, text=True, timeout=10)
        
        if 'Built-in Output' in result.stdout:
            print("✅ Built-in audio output available")
        if 'Built-in Microphone' in result.stdout:
            print("✅ Built-in microphone available")
            
    except subprocess.TimeoutExpired:
        print("⏰ Audio check timed out")
    except Exception as e:
        print(f"❌ Error checking audio: {e}")

def fix_common_issues():
    """Fix common audio echo issues"""
    print("\n🔧 Applying audio fixes...")
    
    fixes = [
        {
            'name': 'Kill duplicate Siri TTS processes',
            'command': ['pkill', '-f', 'sirittsd'],
            'safe': False
        },
        {
            'name': 'Reset audio subsystem', 
            'command': ['sudo', 'launchctl', 'stop', 'com.apple.audio.coreaudiod'],
            'safe': False
        }
    ]
    
    print("Available fixes:")
    for i, fix in enumerate(fixes, 1):
        safety = "⚠️ REQUIRES ADMIN" if not fix['safe'] else "✅ Safe"
        print(f"   {i}. {fix['name']} ({safety})")
    
    print("\n💡 Recommended manual fixes:")
    print("   1. Close other audio apps (Discord, Zoom, etc.)")
    print("   2. Check System Preferences > Sound > Output")
    print("   3. Restart your Totoro assistant")

def check_totoro_config():
    """Check Totoro TTS configuration"""
    print("\n🦙 Checking Totoro configuration...")
    
    config_files = [
        '../config.py',
        '../src/config.py', 
        'config.env'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ Found config: {config_file}")
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    if 'TTS' in content or 'voice' in content.lower():
                        print(f"   📝 Contains TTS/voice settings")
            except Exception as e:
                print(f"   ❌ Error reading: {e}")
        else:
            print(f"❌ Missing: {config_file}")

def suggest_solutions():
    """Suggest solutions for echo issues"""
    print("\n💡 SOLUTIONS FOR AUDIO ECHO:")
    print("=" * 50)
    
    print("\n🎯 IMMEDIATE FIXES:")
    print("1. **Restart Totoro Assistant**:")
    print("   pkill -f 'python.*main'")
    print("   python main.py --test  # Test without voice first")
    
    print("\n2. **Check for Multiple TTS:**")
    print("   ps aux | grep -i tts")
    print("   pkill -f sirittsd  # If multiple found")
    
    print("\n3. **Test TTS Directly:**")
    print("   say 'Hello, this is a test'  # System TTS")
    print("   # Should have no echo")
    
    print("\n🔧 CONFIGURATION FIXES:")
    print("1. **Single TTS Engine**: Ensure only one TTS engine is active")
    print("2. **Audio Device**: Check System Preferences > Sound")
    print("3. **Neural TTS**: May be conflicting with system TTS")
    
    print("\n⚡ ENHANCED FRONTEND:")
    print("• Enhanced server provides better visual feedback")
    print("• Shows: Awake → Thinking → Speaking → Idle")
    print("• Test at: http://localhost:5002 (when loaded)")

def main():
    print("🎭 Totoro Audio Echo Diagnostic Tool")
    print("=" * 40)
    
    check_audio_processes()
    check_audio_config() 
    check_totoro_config()
    suggest_solutions()
    
    print(f"\n🌐 Enhanced frontend loading at: http://localhost:5002")
    print("📊 Check loading progress and test visual feedback!")

if __name__ == "__main__":
    main() 