#!/usr/bin/env python3
"""
Microphone Debug Tool - Find and fix microphone issues
"""

import speech_recognition as sr
import time
import sys

def test_microphone_access():
    """Test basic microphone access"""
    print("🔍 Step 1: Testing Basic Microphone Access")
    print("=" * 50)
    
    try:
        # List available microphones
        mics = sr.Microphone.list_microphone_names()
        print(f"✅ Found {len(mics)} microphones:")
        for i, mic in enumerate(mics):
            print(f"  {i}: {mic}")
        return mics
    except Exception as e:
        print(f"❌ Error listing microphones: {e}")
        return []

def test_specific_microphone(mic_index, mic_name):
    """Test a specific microphone"""
    print(f"\n🎤 Testing: {mic_name} (index {mic_index})")
    print("-" * 60)
    
    try:
        r = sr.Recognizer()
        
        # Test microphone access
        with sr.Microphone(device_index=mic_index) as source:
            print("✅ Microphone accessible")
            print("🔧 Adjusting for ambient noise (2 seconds)...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎙️ Please speak clearly for 4 seconds...")
            print("   (Say something like: 'Hello Totoro, testing microphone')")
            
            # Listen for audio
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            print("📡 Audio captured! Sending to Google Speech Recognition...")
        
        # Try to recognize speech
        text = r.recognize_google(audio, language='en-US')
        print(f"✅ SUCCESS! Recognized: '{text}'")
        return True
        
    except sr.WaitTimeoutError:
        print("⏰ Timeout - No speech detected")
        print("💡 Check: Is the microphone your system's default input?")
        return False
        
    except sr.UnknownValueError:
        print("❓ Audio was captured but speech couldn't be recognized")
        print("💡 Try speaking louder or closer to the microphone")
        return False
        
    except sr.RequestError as e:
        print(f"🌐 Google Speech Recognition error: {e}")
        print("💡 Check your internet connection")
        return False
        
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("💡 This microphone may not have proper permissions")
        return False

def check_system_audio_input():
    """Check system audio input settings"""
    print("\n🔊 Step 3: System Audio Input Check")
    print("=" * 50)
    print("📋 Manual checks needed:")
    print("1. 🍎 System Preferences > Sound > Input")
    print("   - Which microphone is selected?")
    print("   - Is the input level showing activity when you speak?")
    print("2. 🔒 System Preferences > Security & Privacy > Microphone")
    print("   - Is 'Terminal' checked? ✅")
    print("   - Is 'Python' or 'Python Launcher' checked? ✅")
    print("3. 🎤 Check if another app is using the microphone")

def main():
    print("🔧 TOTORO MICROPHONE DIAGNOSTIC TOOL")
    print("=" * 60)
    print("Diagnosing why voice input isn't working...\n")
    
    # Step 1: List microphones
    mics = test_microphone_access()
    if not mics:
        print("❌ No microphones detected. Check hardware connections.")
        return
    
    # Step 2: Test each microphone
    print(f"\n🧪 Step 2: Testing Each Microphone")
    print("=" * 50)
    
    working_mics = []
    priority_mics = [
        ("Logitech BRIO", 2),
        ("iPhone", 0), 
        ("BRIO", 2),
    ]
    
    # Test priority mics first
    for mic_name, expected_index in priority_mics:
        if expected_index < len(mics) and mic_name.lower() in mics[expected_index].lower():
            if test_specific_microphone(expected_index, mics[expected_index]):
                working_mics.append((expected_index, mics[expected_index]))
                print(f"🎉 FOUND WORKING MIC: {mics[expected_index]}")
                break
    
    # If no priority mics work, test all others
    if not working_mics:
        print("\n🔄 Testing all available microphones...")
        for i, mic in enumerate(mics):
            if 'speaker' not in mic.lower():  # Skip speakers
                if test_specific_microphone(i, mic):
                    working_mics.append((i, mic))
                    break
    
    # Step 3: System checks
    check_system_audio_input()
    
    # Results
    print(f"\n📊 RESULTS")
    print("=" * 50)
    
    if working_mics:
        mic_index, mic_name = working_mics[0]
        print(f"✅ WORKING MICROPHONE FOUND!")
        print(f"   Index: {mic_index}")
        print(f"   Name: {mic_name}")
        print(f"\n🚀 Voice input should work now!")
        print(f"   Try: python main.py")
        print(f"   Say: 'Totoro, what time is it?'")
    else:
        print("❌ NO WORKING MICROPHONES FOUND")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Check System Preferences > Security & Privacy > Microphone")
        print("   - Add 'Terminal' if not listed")
        print("   - Add 'Python' if not listed")
        print("2. Check System Preferences > Sound > Input")
        print("   - Select 'Logitech BRIO' or best available mic")
        print("   - Ensure input level shows activity when speaking")
        print("3. Restart Terminal and try again")
        print("4. Use text mode as fallback: python main.py --test")

if __name__ == "__main__":
    main() 