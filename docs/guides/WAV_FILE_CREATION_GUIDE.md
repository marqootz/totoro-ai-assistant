# WAV File Creation Guide

## Overview
Yes, you can absolutely use the voice synthesizing functionality to create audio .wav files! The system uses Coqui TTS (XTTS v2) for high-quality neural voice synthesis with voice cloning capabilities.

## Quick Start

### Basic Usage
```python
from src.voice.text_to_speech import TextToSpeech

# Initialize TTS
tts = TextToSpeech(voice_preference="coqui")

# Create WAV file
tts.coqui_tts.tts_to_file(
    text="Hello! This is a test of the voice synthesis system.",
    speaker_wav="assets/k2so-voice-samples.mp3",  # Voice sample for cloning
    language="en",
    file_path="output.wav",
    speed=1.0
)
```

### Simple Script Example
Run the provided script to create WAV files:
```bash
python simple_wav_creator.py
```

This will create:
- `test_output.wav` - Basic voice synthesis
- `k2so_test.wav` - K2-SO voice cloning (if voice sample available)

## Available Voice Options

### 1. K2-SO Voice (Robot Voice)
- **File**: `assets/k2so-voice-samples.mp3`
- **Characteristics**: Robotic, monotone, Star Wars droid voice
- **Usage**: Perfect for sci-fi or robotic character voices

### 2. George Voice (Human Voice)
- **File**: `assets/george-source-voice.mp3`
- **Characteristics**: Natural human voice
- **Usage**: General purpose, natural speech

### 3. Default Voice
- **File**: `assets/default_voice.wav`
- **Characteristics**: System default voice
- **Usage**: Fallback option

## Advanced Usage

### Custom Voice Cloning
```python
def create_custom_voice_wav(text, output_path, voice_sample_path):
    """Create WAV file with custom voice cloning"""
    tts = TextToSpeech(voice_preference="coqui")
    
    tts.coqui_tts.tts_to_file(
        text=text,
        speaker_wav=voice_sample_path,  # Your custom voice sample
        language="en",
        file_path=output_path,
        speed=1.0  # Adjust speed (0.5-2.0)
    )
```

### Batch Processing
```python
# Create multiple WAV files
texts = {
    "greeting.wav": "Hello, welcome!",
    "weather.wav": "The weather is sunny today.",
    "farewell.wav": "Goodbye and have a great day!"
}

for output_path, text in texts.items():
    tts.coqui_tts.tts_to_file(
        text=text,
        speaker_wav="assets/k2so-voice-samples.mp3",
        language="en",
        file_path=output_path,
        speed=1.0
    )
```

## Performance Characteristics

### Processing Time
- **Typical**: 10-12 seconds per phrase
- **Real-time Factor**: ~1.8x (good performance)
- **Quality**: High-quality neural synthesis

### File Sizes
- **Typical**: 250-300KB per 10-15 second phrase
- **Format**: WAV (uncompressed)
- **Sample Rate**: 22050 Hz
- **Channels**: Mono

## Configuration Options

### Speed Control
```python
# Slower speech (0.5x speed)
tts.coqui_tts.tts_to_file(..., speed=0.5)

# Normal speech (1.0x speed)
tts.coqui_tts.tts_to_file(..., speed=1.0)

# Faster speech (2.0x speed)
tts.coqui_tts.tts_to_file(..., speed=2.0)
```

### Language Support
```python
# English (default)
tts.coqui_tts.tts_to_file(..., language="en")

# Other languages supported by XTTS v2
tts.coqui_tts.tts_to_file(..., language="es")  # Spanish
tts.coqui_tts.tts_to_file(..., language="fr")  # French
tts.coqui_tts.tts_to_file(..., language="de")  # German
```

## Troubleshooting

### Common Issues

1. **"Coqui TTS requires a speaker voice file"**
   - Solution: Provide a valid voice sample file path
   - Ensure the file exists and is accessible

2. **"Coqui TTS not available"**
   - Solution: Install Coqui TTS: `pip install TTS`
   - Check that the model is downloaded

3. **Large file sizes**
   - Solution: Consider post-processing to compress WAV files
   - Use lower sample rates if quality allows

4. **Slow processing**
   - Solution: This is normal for neural TTS
   - Consider batch processing for multiple files

### Voice Sample Requirements
- **Format**: MP3, WAV, or other audio formats
- **Duration**: 5-30 seconds of clear speech
- **Quality**: High-quality, minimal background noise
- **Content**: Natural speech, not music or effects

## Examples

### Example 1: Create K2-SO Voice WAV
```python
from src.voice.text_to_speech import TextToSpeech

tts = TextToSpeech(voice_preference="coqui")
tts.coqui_tts.tts_to_file(
    text="I am K2-SO, a reprogrammed Imperial droid.",
    speaker_wav="assets/k2so-voice-samples.mp3",
    language="en",
    file_path="k2so_greeting.wav",
    speed=1.0
)
```

### Example 2: Create Multiple Files
```python
import os
from src.voice.text_to_speech import TextToSpeech

tts = TextToSpeech(voice_preference="coqui")
voice_sample = "assets/k2so-voice-samples.mp3"

phrases = [
    "Hello, I am your assistant.",
    "The weather is sunny today.",
    "Thank you for using our system."
]

for i, phrase in enumerate(phrases):
    output_file = f"phrase_{i+1}.wav"
    tts.coqui_tts.tts_to_file(
        text=phrase,
        speaker_wav=voice_sample,
        language="en",
        file_path=output_file,
        speed=1.0
    )
    print(f"Created: {output_file}")
```

## Integration with Other Systems

### Audio Processing
```python
# Convert to different formats
import librosa
import soundfile as sf

# Load generated WAV
audio, sr = librosa.load("output.wav", sr=22050)

# Save as MP3
sf.write("output.mp3", audio, sr, format="mp3")

# Save as lower quality WAV
sf.write("output_compressed.wav", audio, 16000, format="wav")
```

### Web Integration
```python
# For web applications, serve WAV files
from flask import send_file

@app.route('/generate_speech/<text>')
def generate_speech(text):
    output_path = f"generated_{hash(text)}.wav"
    tts.coqui_tts.tts_to_file(
        text=text,
        speaker_wav="assets/k2so-voice-samples.mp3",
        language="en",
        file_path=output_path,
        speed=1.0
    )
    return send_file(output_path, mimetype="audio/wav")
```

## Summary

The voice synthesis system provides powerful capabilities for creating high-quality WAV files:

✅ **High-quality neural voice synthesis**  
✅ **Voice cloning with custom samples**  
✅ **Multiple voice options (K2-SO, George, Default)**  
✅ **Speed and language control**  
✅ **Batch processing support**  
✅ **Easy integration with other systems**  

The system is ready to use and can create professional-quality audio files for various applications including games, applications, content creation, and more. 