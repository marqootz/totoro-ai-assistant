#!/usr/bin/env python3
"""
Audio Preprocessing for Voice Cloning
Remove background noise and enhance voice samples for better cloning quality
"""

import os
import sys
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import wiener
import noisereduce as nr

def install_dependencies():
    """Install required dependencies for audio preprocessing"""
    import subprocess
    
    packages = [
        "librosa",
        "soundfile", 
        "noisereduce",
        "scipy"
    ]
    
    print("🔧 Installing audio preprocessing dependencies...")
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def analyze_audio(file_path):
    """Analyze audio file for noise characteristics"""
    print(f"🔍 Analyzing audio: {file_path}")
    
    # Load audio
    audio, sr = librosa.load(file_path, sr=None)
    
    # Basic audio statistics
    duration = len(audio) / sr
    rms_energy = np.sqrt(np.mean(audio**2))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(audio))
    
    print(f"📊 Audio Analysis:")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Sample Rate: {sr} Hz")
    print(f"   RMS Energy: {rms_energy:.4f}")
    print(f"   Zero Crossing Rate: {zero_crossing_rate:.4f}")
    
    # Detect silence/noise sections (first and last 0.5 seconds)
    noise_start = audio[:int(0.5 * sr)] if duration > 1.0 else audio[:int(0.1 * sr)]
    noise_end = audio[-int(0.5 * sr):] if duration > 1.0 else audio[-int(0.1 * sr):]
    
    return audio, sr, noise_start, noise_end

def remove_background_noise(audio, sr, method="spectral_subtraction"):
    """Remove background noise using various methods"""
    print(f"🧹 Removing background noise using {method}...")
    
    if method == "spectral_subtraction":
        # Use noisereduce library for spectral subtraction
        reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=False, prop_decrease=0.8)
        return reduced_noise
    
    elif method == "wiener_filter":
        # Apply Wiener filter
        filtered = wiener(audio, noise=None)
        return filtered
    
    elif method == "advanced_spectral":
        # Advanced spectral subtraction with noise profiling
        # Assume first 0.5 seconds contain primarily noise
        noise_sample = audio[:int(0.5 * sr)]
        reduced_noise = nr.reduce_noise(
            y=audio, 
            sr=sr, 
            y_noise=noise_sample,
            stationary=False,
            prop_decrease=0.9
        )
        return reduced_noise
    
    else:
        print(f"❌ Unknown method: {method}")
        return audio

def enhance_voice(audio, sr):
    """Enhance voice quality after noise reduction"""
    print("✨ Enhancing voice quality...")
    
    # Normalize audio
    audio = librosa.util.normalize(audio)
    
    # Apply gentle high-pass filter to remove low-frequency noise
    audio_filtered = librosa.effects.preemphasis(audio, coef=0.97)
    
    # Trim silence from beginning and end
    audio_trimmed, _ = librosa.effects.trim(audio_filtered, top_db=20)
    
    return audio_trimmed

def process_voice_sample(input_path, output_path, method="advanced_spectral"):
    """Complete voice sample preprocessing pipeline"""
    print(f"🎤 VOICE SAMPLE PREPROCESSING")
    print("=" * 50)
    
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return False
    
    try:
        # Analyze original audio
        audio, sr, noise_start, noise_end = analyze_audio(input_path)
        
        # Remove background noise
        clean_audio = remove_background_noise(audio, sr, method=method)
        
        # Enhance voice quality
        enhanced_audio = enhance_voice(clean_audio, sr)
        
        # Save processed audio
        sf.write(output_path, enhanced_audio, sr)
        
        print(f"✅ Processed audio saved to: {output_path}")
        
        # Compare before/after statistics
        print(f"\n📈 IMPROVEMENT ANALYSIS:")
        original_rms = np.sqrt(np.mean(audio**2))
        processed_rms = np.sqrt(np.mean(enhanced_audio**2))
        
        print(f"   Original RMS: {original_rms:.4f}")
        print(f"   Processed RMS: {processed_rms:.4f}")
        print(f"   Signal Enhancement: {processed_rms/original_rms:.2f}x")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing audio: {e}")
        return False

def process_k2so_voice():
    """Process K2-SO voice sample specifically"""
    input_file = "assets/k2so-voice-samples.mp3"
    output_file = "assets/k2so-voice-samples-clean.mp3"
    
    print("🤖 PROCESSING K2-SO VOICE SAMPLE")
    print("=" * 50)
    
    success = process_voice_sample(input_file, output_file, method="advanced_spectral")
    
    if success:
        print("\n💡 USAGE:")
        print(f"   Use the cleaned file for better voice cloning:")
        print(f"   python speak_as_k2so.py 'I am K2-SO.' --clean")
        print(f"   Or update your scripts to use: {output_file}")
        
        # Test comparison
        print(f"\n🧪 To compare voices:")
        print(f"   python compare_voice_quality.py")
    
    return success

def process_george_voice():
    """Process George voice sample if it exists"""
    input_file = "assets/george-source-voice.mp3"
    output_file = "assets/george-source-voice-clean.mp3"
    
    if not os.path.exists(input_file):
        print(f"⚠️ George voice file not found: {input_file}")
        return False
    
    print("👤 PROCESSING GEORGE VOICE SAMPLE")
    print("=" * 50)
    
    return process_voice_sample(input_file, output_file, method="advanced_spectral")

def main():
    """Main preprocessing function"""
    print("🎛️ VOICE SAMPLE AUDIO PREPROCESSING")
    print("=" * 60)
    
    # Install dependencies if needed
    try:
        import librosa, soundfile, noisereduce
    except ImportError:
        install_dependencies()
    
    # Process available voice samples
    k2so_success = process_k2so_voice()
    george_success = process_george_voice()
    
    print("\n" + "=" * 60)
    print("📋 PROCESSING SUMMARY:")
    print(f"   K2-SO voice: {'✅ Processed' if k2so_success else '❌ Failed'}")
    print(f"   George voice: {'✅ Processed' if george_success else '❌ Not found/Failed'}")
    
    if k2so_success:
        print(f"\n🎉 Voice preprocessing complete!")
        print(f"   Clean K2-SO sample ready for improved voice cloning!")

if __name__ == "__main__":
    main() 