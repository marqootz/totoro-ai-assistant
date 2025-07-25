# Woman's Voice Setup Guide

## Overview
You can absolutely use a woman's voice in her mid-30s! The voice synthesis system supports voice cloning from any audio sample, so you just need to provide a voice sample of the woman speaking.

## 🎤 Voice Sample Requirements

### What You Need
- **Audio file** of the woman speaking (MP3, WAV, or other formats)
- **Duration**: 5-30 seconds of clear speech
- **Quality**: High-quality recording with minimal background noise
- **Content**: Natural speech (not singing, not music, not effects)

### Ideal Voice Sample Characteristics
- **Clear pronunciation** - Easy to understand words
- **Natural speech patterns** - Normal conversation pace
- **Consistent volume** - No sudden loud/quiet parts
- **Minimal background noise** - No music, traffic, or other sounds
- **Good microphone quality** - Clear audio recording

## 🚀 Quick Start

### Step 1: Prepare Your Voice Sample
1. Record the woman speaking clearly for 10-20 seconds
2. Save as MP3 or WAV file (e.g., `woman_voice_sample.mp3`)
3. Place the file in your project directory

### Step 2: Create WAV Files
```bash
# Using the provided script
python create_woman_voice.py "Hello! This is a test of the woman's voice." output.wav woman_voice_sample.mp3
```

### Step 3: Python Code Example
```python
from src.voice.text_to_speech import TextToSpeech

# Initialize TTS
tts = TextToSpeech(voice_preference="coqui")

# Create WAV file with woman's voice
tts.coqui_tts.tts_to_file(
    text="Hello! This is a test of the woman's voice synthesis.",
    speaker_wav="woman_voice_sample.mp3",  # Your woman's voice sample
    language="en",
    file_path="woman_voice_output.wav",
    speed=1.0
)
```

## 📝 Voice Sample Recording Tips

### Recording Setup
- **Quiet environment** - No background noise
- **Good microphone** - USB microphone or smartphone with good mic
- **Consistent distance** - Keep same distance from microphone
- **Natural speech** - Speak as you normally would

### What to Record
```
Good examples:
- "Hello, my name is Sarah and I'm excited to help you today."
- "Welcome to our system. I'm here to assist you with any questions."
- "The weather is beautiful today. I hope you're having a great day."

Avoid:
- Singing or musical content
- Background music or noise
- Very fast or very slow speech
- Whispering or shouting
```

### Recording Length
- **Minimum**: 5 seconds
- **Optimal**: 10-20 seconds
- **Maximum**: 30 seconds

## 🛠️ Advanced Usage

### Batch Processing with Woman's Voice
```python
from src.voice.text_to_speech import TextToSpeech

tts = TextToSpeech(voice_preference="coqui")
woman_voice_sample = "woman_voice_sample.mp3"

# Multiple phrases
phrases = [
    "Hello, welcome to our system!",
    "I'm here to help you with any questions.",
    "Thank you for using our service today.",
    "Have a wonderful day!"
]

for i, phrase in enumerate(phrases):
    output_file = f"woman_voice_{i+1}.wav"
    tts.coqui_tts.tts_to_file(
        text=phrase,
        speaker_wav=woman_voice_sample,
        language="en",
        file_path=output_file,
        speed=1.0
    )
    print(f"Created: {output_file}")
```

### Speed and Tone Control
```python
# Slower, more deliberate speech
tts.coqui_tts.tts_to_file(
    text="This is spoken more slowly and deliberately.",
    speaker_wav="woman_voice_sample.mp3",
    language="en",
    file_path="slow_speech.wav",
    speed=0.8  # 20% slower
)

# Faster, more energetic speech
tts.coqui_tts.tts_to_file(
    text="This is spoken more quickly and energetically!",
    speaker_wav="woman_voice_sample.mp3",
    language="en",
    file_path="fast_speech.wav",
    speed=1.2  # 20% faster
)
```

## 🎯 Voice Characteristics for Mid-30s Woman

### Typical Characteristics
- **Pitch**: Medium to slightly lower than younger voices
- **Pace**: Natural, conversational speed
- **Tone**: Warm, professional, confident
- **Clarity**: Clear pronunciation and articulation

### Adjusting for Age-Appropriate Speech
```python
# Professional, mature tone
tts.coqui_tts.tts_to_file(
    text="As an experienced professional, I understand the importance of clear communication.",
    speaker_wav="woman_voice_sample.mp3",
    language="en",
    file_path="professional_tone.wav",
    speed=0.9  # Slightly slower for more mature feel
)

# Warm, friendly tone
tts.coqui_tts.tts_to_file(
    text="I'm here to help you with a warm, friendly approach.",
    speaker_wav="woman_voice_sample.mp3",
    language="en",
    file_path="friendly_tone.wav",
    speed=1.0
)
```

## 🔧 Troubleshooting

### Common Issues

1. **"Voice sample not found"**
   - Check file path is correct
   - Ensure file exists in the specified location

2. **Poor voice quality**
   - Re-record with better microphone
   - Reduce background noise
   - Use longer voice sample (10-20 seconds)

3. **Voice doesn't sound like the original**
   - Ensure voice sample is clear and natural
   - Try different speech content in the sample
   - Check that sample is not too short

4. **Processing errors**
   - Verify Coqui TTS is installed: `pip install TTS`
   - Check that model is downloaded
   - Ensure sufficient disk space

### Voice Sample Optimization
```python
# Test different voice samples
voice_samples = [
    "woman_voice_sample_1.mp3",
    "woman_voice_sample_2.mp3", 
    "woman_voice_sample_3.mp3"
]

test_text = "Hello, this is a test of the voice synthesis."

for sample in voice_samples:
    if os.path.exists(sample):
        output_file = f"test_{sample.replace('.mp3', '.wav')}"
        tts.coqui_tts.tts_to_file(
            text=test_text,
            speaker_wav=sample,
            language="en",
            file_path=output_file,
            speed=1.0
        )
        print(f"Tested: {sample} -> {output_file}")
```

## 📊 Performance Expectations

### Processing Time
- **First run**: 10-15 seconds (model loading)
- **Subsequent runs**: 8-12 seconds per phrase
- **Real-time factor**: ~1.8x (good performance)

### File Sizes
- **Typical**: 250-300KB per 10-15 second phrase
- **Format**: WAV (uncompressed)
- **Quality**: High-quality neural synthesis

## 🎉 Example Use Cases

### Professional Applications
- **Customer service** - Warm, helpful voice
- **Training videos** - Clear, instructional tone
- **Audiobooks** - Engaging, natural narration
- **Podcasts** - Professional presentation

### Personal Projects
- **Personal assistant** - Friendly, helpful voice
- **Gaming** - Character voice acting
- **Content creation** - YouTube videos, presentations
- **Accessibility** - Text-to-speech for reading

## Summary

✅ **Yes, you can use a woman's voice in her mid-30s!**  
✅ **Just provide a voice sample of her speaking**  
✅ **High-quality neural voice cloning**  
✅ **Professional, natural-sounding results**  
✅ **Easy to set up and use**  

The system will clone the woman's voice characteristics and create natural-sounding speech that matches her age, tone, and speaking style. Just make sure to provide a good quality voice sample for the best results! 