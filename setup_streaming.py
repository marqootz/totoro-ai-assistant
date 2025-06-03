#!/usr/bin/env python3
"""
Setup script for K2-SO streaming synthesis
Installs dependencies and runs initial tests
"""

import subprocess
import sys
import os

def install_pygame():
    """Install pygame for audio playback"""
    print("🔧 Installing pygame for streaming audio playback...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("✅ pygame installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install pygame: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking streaming synthesis dependencies...")
    
    required_packages = [
        ("pygame", "Audio playback"),
        ("numpy", "Audio processing"), 
        ("wave", "Audio file handling"),
        ("threading", "Parallel processing"),
        ("queue", "Audio chunk buffering")
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package:<12} - {description}")
        except ImportError:
            print(f"   ❌ {package:<12} - {description} (MISSING)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        
        if 'pygame' in missing_packages:
            if install_pygame():
                missing_packages.remove('pygame')
        
        if missing_packages:
            print(f"❌ Still missing: {', '.join(missing_packages)}")
            return False
    
    print("✅ All dependencies available!")
    return True

def test_streaming_basic():
    """Run basic streaming test"""
    print("\n🧪 Running basic streaming synthesis test...")
    
    try:
        from streaming_synthesis_phase1 import K2SOStreamingSynthesis
        
        # Initialize streaming TTS
        streaming_tts = K2SOStreamingSynthesis()
        
        # Test short phrase
        result = streaming_tts.speak_streaming("I am K2-SO")
        
        if result['success']:
            metrics = result['metrics']
            print(f"✅ Basic test successful!")
            print(f"   Perceived latency: {metrics['perceived_latency']:.2f}s")
            print(f"   Improvement: {metrics['improvement']:.1f}% vs baseline")
            return True
        else:
            print(f"❌ Basic test failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main setup and test routine"""
    print("🚀 K2-SO STREAMING SYNTHESIS SETUP")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Setup failed - missing dependencies")
        return False
    
    # Step 2: Verify assets
    print("\n📁 Checking audio assets...")
    
    optimized_asset = "assets/k2so-voice-samples-optimized.mp3"
    original_asset = "assets/k2so-voice-samples.mp3"
    
    if os.path.exists(optimized_asset):
        print(f"   ✅ Optimized K2-SO samples found: {optimized_asset}")
        asset_path = optimized_asset
    elif os.path.exists(original_asset):
        print(f"   ⚠️ Using original K2-SO samples: {original_asset}")
        print("   💡 Consider running advanced_performance_optimization.py to create optimized version")
        asset_path = original_asset
    else:
        print(f"   ❌ No K2-SO audio samples found!")
        print(f"   Expected: {optimized_asset} or {original_asset}")
        return False
    
    # Step 3: Run basic test
    if test_streaming_basic():
        print(f"\n🎉 STREAMING SYNTHESIS READY!")
        print(f"   Run: python streaming_synthesis_phase1.py --test")
        print(f"   Or: python streaming_synthesis_phase1.py \"Your text here\"")
        return True
    else:
        print(f"\n❌ Setup completed but streaming test failed")
        print(f"   Check your TTS installation and try again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 