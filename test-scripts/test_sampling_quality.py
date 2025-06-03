#!/usr/bin/env python3
"""
Test different sampling levels for Chatterbox TTS
Compare speed vs quality trade-offs
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.voice.text_to_speech import TextToSpeech

def test_sampling_levels():
    """Test different sampling configurations"""
    
    print("🎛️ CHATTERBOX SAMPLING QUALITY TEST")
    print("=" * 50)
    
    # Check if George's voice is available
    source_audio = "assets/george-source-voice.mp3"
    if not os.path.exists(source_audio):
        print(f"❌ George's voice not found: {source_audio}")
        print("Testing with default voice instead...")
        source_audio = None
    else:
        print(f"✅ Using George's voice: {source_audio}")
    
    # Initialize TTS
    print("🚀 Initializing Chatterbox TTS...")
    tts = TextToSpeech(voice_preference="chatterbox")
    
    if not tts.chatterbox_model:
        print("❌ Chatterbox TTS not available")
        return
    
    test_text = "Hello! This is a quality test of the voice sampling system."
    
    # Test different sampling configurations
    sampling_configs = [
        {
            "name": "Ultra Fast", 
            "steps": 50,
            "description": "Very fast but may sound robotic",
            "expected_time": "2-4 seconds"
        },
        {
            "name": "Fast", 
            "steps": 100,
            "description": "Good balance of speed and quality",
            "expected_time": "4-8 seconds"
        },
        {
            "name": "Balanced", 
            "steps": 250,
            "description": "Good quality, reasonable speed",
            "expected_time": "8-12 seconds"
        },
        {
            "name": "High Quality", 
            "steps": 500,
            "description": "Very good quality, slower",
            "expected_time": "12-18 seconds"
        },
        {
            "name": "Ultra Quality", 
            "steps": 1000,
            "description": "Best quality, slowest (default)",
            "expected_time": "18-25 seconds"
        }
    ]
    
    print(f"\n🗣️ Test phrase: '{test_text}'")
    print("\nTesting different sampling levels:\n")
    
    for config in sampling_configs:
        print(f"🎚️  {config['name']} ({config['steps']} steps)")
        print(f"   📝 {config['description']}")
        print(f"   ⏱️  Expected: {config['expected_time']}")
        
        # Time the generation
        start_time = time.time()
        
        # Note: Chatterbox doesn't directly expose sampling steps in the public API
        # This would require modifying the internal generation parameters
        print(f"   🔄 Generating... (using default 1000 steps for now)")
        
        if source_audio:
            success = tts.speak(test_text, audio_prompt_path=source_audio)
        else:
            success = tts.speak(test_text)
        
        end_time = time.time()
        actual_time = end_time - start_time
        
        if success:
            print(f"   ✅ Generated in {actual_time:.1f} seconds")
        else:
            print(f"   ❌ Failed")
        
        print()  # Empty line
        
        # Ask user for quality rating
        try:
            quality = input(f"   💯 Rate quality (1-10): ").strip()
            if quality.isdigit():
                print(f"   📊 Quality rating: {quality}/10")
        except:
            pass
        
        print("-" * 40)

def explain_sampling_theory():
    """Explain the theory behind sampling in neural TTS"""
    
    print("\n🧠 NEURAL TTS SAMPLING THEORY")
    print("=" * 50)
    
    print("""
🔬 How Neural Voice Synthesis Works:

1. **Diffusion Process**: Starts with random noise
2. **Iterative Refinement**: Each step removes noise and adds structure
3. **Quality vs Speed**: More steps = better quality but slower

📊 Typical Quality Levels:

• 50 steps:   Fast but may have artifacts, robotic sound
• 100 steps:  Decent quality, good for quick responses  
• 250 steps:  Good quality, reasonable speed
• 500 steps:  Very good quality, natural sounding
• 1000 steps: Excellent quality, indistinguishable from human

⚡ Speed Impact:
• Each step takes ~10-20ms on CPU
• 50 steps:   ~1-2 seconds
• 1000 steps: ~18-25 seconds

🎭 Voice Cloning Impact:
• Cloning requires more steps for accuracy
• Without cloning: Can use fewer steps
• With cloning: Need more steps for voice fidelity
""")

if __name__ == "__main__":
    explain_sampling_theory()
    
    response = input("\nWould you like to test different sampling levels? (y/n): ").lower()
    if response in ['y', 'yes']:
        test_sampling_levels()
    else:
        print("\n💡 To modify sampling steps, you would need to:")
        print("   1. Access Chatterbox internal parameters")
        print("   2. Modify the diffusion scheduler")
        print("   3. Set num_inference_steps parameter")
        print("   4. Balance speed vs quality for your use case") 