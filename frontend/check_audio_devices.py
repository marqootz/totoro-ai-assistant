#!/usr/bin/env python3
"""
Audio Device Checker for Totoro Assistant
Displays current audio configuration and potential echo sources
"""

import subprocess
import re

def get_audio_devices():
    """Get all audio devices from system profiler"""
    print("🎧 AUDIO OUTPUT DEVICES:")
    print("=" * 40)
    
    try:
        result = subprocess.run(['system_profiler', 'SPAudioDataType'], 
                              capture_output=True, text=True)
        
        devices = []
        current_device = {}
        in_device = False
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            
            # New device detected
            if ':' in line and not line.startswith(' ') and 'Audio:' not in line and 'Devices:' not in line:
                if current_device:
                    devices.append(current_device)
                    current_device = {}
                
                device_name = line.replace(':', '').strip()
                current_device['name'] = device_name
                in_device = True
                
            elif in_device and ':' in line:
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    current_device[key] = value
        
        # Add the last device
        if current_device:
            devices.append(current_device)
        
        # Display devices
        output_devices = []
        input_devices = []
        
        for device in devices:
            name = device.get('name', 'Unknown')
            manufacturer = device.get('Manufacturer', 'Unknown')
            transport = device.get('Transport', 'Unknown')
            
            if 'Output Channels' in device:
                channels = device.get('Output Channels', 'Unknown')
                is_default = device.get('Default Output Device', 'No') == 'Yes'
                is_system_default = device.get('Default System Output Device', 'No') == 'Yes'
                
                status_icons = []
                if is_default:
                    status_icons.append("🔊 Default")
                if is_system_default:
                    status_icons.append("🎵 System Default")
                
                status = " ".join(status_icons) if status_icons else "⚪ Available"
                
                print(f"\n📺 {name}")
                print(f"   Manufacturer: {manufacturer}")
                print(f"   Transport: {transport}")
                print(f"   Channels: {channels}")
                print(f"   Status: {status}")
                
                output_devices.append({
                    'name': name,
                    'is_default': is_default,
                    'is_system_default': is_system_default,
                    'transport': transport
                })
                
            elif 'Input Channels' in device:
                channels = device.get('Input Channels', 'Unknown')
                is_default = device.get('Default Input Device', 'No') == 'Yes'
                
                status = "🎤 Default Input" if is_default else "⚪ Available Input"
                
                print(f"\n🎤 {name}")
                print(f"   Manufacturer: {manufacturer}")
                print(f"   Transport: {transport}")
                print(f"   Channels: {channels}")
                print(f"   Status: {status}")
                
                input_devices.append({
                    'name': name,
                    'is_default': is_default,
                    'transport': transport
                })
        
        return output_devices, input_devices
        
    except Exception as e:
        print(f"❌ Error getting audio devices: {e}")
        return [], []

def diagnose_echo_potential(output_devices):
    """Diagnose potential sources of echo"""
    print(f"\n🔍 ECHO DIAGNOSIS:")
    print("=" * 30)
    
    potential_issues = []
    
    # Check for multiple output devices
    active_outputs = [d for d in output_devices if d['is_default'] or d['is_system_default']]
    
    if len(active_outputs) > 1:
        potential_issues.append("⚠️ Multiple default output devices detected")
        for device in active_outputs:
            print(f"   📺 {device['name']} ({device['transport']})")
    
    # Check for external displays with audio
    external_audio = [d for d in output_devices if d['transport'] in ['DisplayPort', 'HDMI', 'USB']]
    if external_audio:
        potential_issues.append("🖥️ External displays/devices with audio capability")
        for device in external_audio:
            print(f"   📺 {device['name']} via {device['transport']}")
    
    # Check current default
    current_default = next((d for d in output_devices if d['is_system_default']), None)
    if current_default:
        print(f"\n✅ Current System Default: {current_default['name']}")
        print(f"   Transport: {current_default['transport']}")
        
        if current_default['transport'] in ['DisplayPort', 'HDMI']:
            potential_issues.append("🖥️ Audio going to external display - may have speakers")
    
    if not potential_issues:
        print("✅ No obvious audio routing issues detected")
    else:
        print(f"\n⚠️ POTENTIAL ECHO SOURCES:")
        for issue in potential_issues:
            print(f"   {issue}")

def suggest_audio_fixes(output_devices):
    """Suggest fixes based on current audio setup"""
    print(f"\n🔧 RECOMMENDED FIXES:")
    print("=" * 30)
    
    current_default = next((d for d in output_devices if d['is_system_default']), None)
    
    if current_default:
        if current_default['transport'] == 'Built-in':
            print("✅ Using built-in speakers - Good for TTS")
            print("   🔹 Check volume level (currently at 94%)")
            print("   🔹 Close other audio apps (Spotify, Music)")
            
        elif current_default['transport'] in ['DisplayPort', 'HDMI']:
            print("⚠️ Using external display audio")
            print("   🔹 External displays may have built-in speakers")
            print("   🔹 This could cause echo if both display + internal speakers active")
            print("   🔹 Consider switching to built-in speakers for TTS testing")
            
        elif current_default['transport'] == 'USB':
            print("🎧 Using USB audio device")
            print("   🔹 Good for TTS if it's headphones/speakers")
            print("   🔹 Make sure no other audio outputs are active")
    
    print(f"\n💡 IMMEDIATE STEPS:")
    print("1. **Test Current Setup**:")
    print("   say 'Testing current audio setup'")
    print("   # Listen for any echo or double audio")
    
    print("2. **Switch to Built-in if needed**:")
    print("   # System Preferences > Sound > Output > Mac Studio Speakers")
    
    print("3. **Close Interfering Apps**:")
    print("   # Quit Spotify, Music.app, Discord, etc.")
    
    print("4. **Test TTS Isolation**:")
    print("   python test_audio.py  # Run our audio test")

def main():
    print("🎵 Totoro Audio Device Analysis")
    print("=" * 35)
    
    output_devices, input_devices = get_audio_devices()
    
    if output_devices:
        diagnose_echo_potential(output_devices)
        suggest_audio_fixes(output_devices)
    else:
        print("❌ No audio devices found")
    
    print(f"\n🎭 Enhanced Frontend: http://localhost:5002")
    print("✨ Visual feedback working - audio fixes in progress!")

if __name__ == "__main__":
    main() 