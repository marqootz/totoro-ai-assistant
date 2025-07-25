# Woman's Voice Quick Start Guide

## ✅ **Yes, you can absolutely use a woman's voice in her mid-30s!**

The voice synthesis system supports voice cloning from any audio sample. Here's everything you need to know:

## 🎤 **What You Need**

### 1. Voice Sample Requirements
- **Audio file** of the woman speaking (MP3, WAV, or other formats)
- **Duration**: 5-30 seconds of clear speech
- **Quality**: High-quality recording with minimal background noise
- **Content**: Natural speech (not singing, not music, not effects)

### 2. Recording Tips
- **Quiet environment** - No background noise
- **Good microphone** - USB microphone or smartphone with good mic
- **Natural speech** - Speak as you normally would
- **Clear pronunciation** - Easy to understand words

## 🚀 **Quick Start (3 Steps)**

### Step 1: Record Voice Sample
Record the woman speaking clearly for 10-20 seconds:
```
Example: "Hello, my name is Sarah and I'm excited to help you today. 
I have experience in customer service and I'm here to assist you 
with any questions you might have."
```

### Step 2: Save and Place File
- Save as `woman_voice_sample.mp3` or `woman_voice_sample.wav`
- Place in your project directory

### Step 3: Create WAV Files
```bash
# Command line usage
python create_woman_voice.py "Hello! This is a test." output.wav woman_voice_sample.mp3
```

## 💻 **Code Examples**

### Basic Usage
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

### Batch Processing
```python
phrases = [
    "Hello, welcome to our system!",
    "I'm here to help you with any questions.",
    "Thank you for using our service today."
]

for i, phrase in enumerate(phrases):
    output_file = f"woman_voice_{i+1}.wav"
    tts.coqui_tts.tts_to_file(
        text=phrase,
        speaker_wav="woman_voice_sample.mp3",
        language="en",
        file_path=output_file,
        speed=1.0
    )
```

## 🎯 **Voice Characteristics for Mid-30s Woman**

### Typical Characteristics
- **Pitch**: Medium to slightly lower than younger voices
- **Pace**: Natural, conversational speed
- **Tone**: Warm, professional, confident
- **Clarity**: Clear pronunciation and articulation

### Speed Control Examples
```python
# Professional, mature tone (slightly slower)
tts.coqui_tts.tts_to_file(..., speed=0.9)

# Normal conversational speed
tts.coqui_tts.tts_to_file(..., speed=1.0)

# More energetic speech
tts.coqui_tts.tts_to_file(..., speed=1.1)
```

## 📊 **Performance Expectations**

### Processing Time
- **First run**: 10-15 seconds (model loading)
- **Subsequent runs**: 8-12 seconds per phrase
- **Real-time factor**: ~1.8x (good performance)

### File Sizes
- **Typical**: 250-300KB per 10-15 second phrase
- **Format**: WAV (uncompressed)
- **Quality**: High-quality neural synthesis

## 🛠️ **Available Tools**

### 1. `create_woman_voice.py` - Command Line Tool
```bash
python create_woman_voice.py "Your text here" output.wav voice_sample.mp3
```

### 2. `test_woman_voice.py` - Setup Test
```bash
python test_woman_voice.py
```
This will check if you have voice samples and test the setup.

### 3. `simple_wav_creator.py` - Basic Example
```bash
python simple_wav_creator.py
```

## 🎉 **Example Use Cases**

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

## 🔧 **Troubleshooting**

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

## 📝 **Voice Sample Recording Script**

Here's a good script for recording the woman's voice sample:

```
"Hello, my name is [Name] and I'm excited to help you today. 
I have experience in customer service and I'm here to assist you 
with any questions you might have. I hope you're having a wonderful day!"
```

## ✅ **Summary**

**Yes, you can use a woman's voice in her mid-30s!** 

✅ **Just provide a voice sample of her speaking**  
✅ **High-quality neural voice cloning**  
✅ **Professional, natural-sounding results**  
✅ **Easy to set up and use**  
✅ **Supports batch processing**  
✅ **Speed and tone control**  

The system will clone the woman's voice characteristics and create natural-sounding speech that matches her age, tone, and speaking style. Just make sure to provide a good quality voice sample for the best results! 