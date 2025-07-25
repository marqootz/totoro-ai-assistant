# ElevenLabs Voices Guide

## 🎉 **New Voice Options Available!**

You now have access to two high-quality ElevenLabs voice samples:
- **Julia** - Professional woman's voice
- **Sarah** - Warm, friendly woman's voice

## 📁 **Available Voice Files**

### ElevenLabs Voices
- `assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3` (311,842 bytes)
- `assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3` (334,830 bytes)

### Other Available Voices
- `assets/george-source-voice-clean.mp3` - Human male voice
- `assets/k2so-voice-samples.mp3` - Robot voice

## 🚀 **Quick Start with ElevenLabs Voices**

### Command Line Usage
```bash
# Using Julia voice
python create_woman_voice.py "Hello! This is Julia speaking." julia_output.wav assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3

# Using Sarah voice
python create_woman_voice.py "Hello! This is Sarah speaking." sarah_output.wav assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3
```

### Python Code
```python
from src.voice.text_to_speech import TextToSpeech

# Initialize TTS
tts = TextToSpeech(voice_preference="coqui")

# Using Julia voice
tts.coqui_tts.tts_to_file(
    text="Hello! This is Julia speaking. I'm here to help you today.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
    language="en",
    file_path="julia_greeting.wav",
    speed=1.0
)

# Using Sarah voice
tts.coqui_tts.tts_to_file(
    text="Hello! This is Sarah speaking. I'm here to help you today.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3",
    language="en",
    file_path="sarah_greeting.wav",
    speed=1.0
)
```

## 🎯 **Voice Characteristics**

### Julia Voice
- **Style**: Professional, clear, confident
- **Best for**: Business presentations, customer service, formal communications
- **Tone**: Warm but professional
- **Age**: Mid-30s professional woman

### Sarah Voice
- **Style**: Friendly, approachable, warm
- **Best for**: Casual conversations, friendly customer service, personal assistant
- **Tone**: Warm and welcoming
- **Age**: Mid-30s friendly woman

## 📊 **Performance Results**

### Julia Voice Test
- **Processing Time**: 10.85 seconds
- **Real-time Factor**: 1.68x
- **File Size**: 284,780 bytes
- **Quality**: Excellent professional voice

### Sarah Voice Test
- **Processing Time**: 8.89 seconds
- **Real-time Factor**: 1.73x
- **File Size**: 226,924 bytes
- **Quality**: Excellent friendly voice

## 🛠️ **Advanced Usage Examples**

### Batch Processing with Both Voices
```python
from src.voice.text_to_speech import TextToSpeech

tts = TextToSpeech(voice_preference="coqui")

# Phrases to generate
phrases = [
    "Hello, welcome to our system!",
    "I'm here to help you with any questions.",
    "Thank you for using our service today.",
    "Have a wonderful day!"
]

# Voice options
voices = {
    "julia": "assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
    "sarah": "assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3"
}

# Generate all combinations
for voice_name, voice_path in voices.items():
    for i, phrase in enumerate(phrases):
        output_file = f"{voice_name}_phrase_{i+1}.wav"
        tts.coqui_tts.tts_to_file(
            text=phrase,
            speaker_wav=voice_path,
            language="en",
            file_path=output_file,
            speed=1.0
        )
        print(f"Created: {output_file}")
```

### Speed Variations
```python
# Professional Julia (slightly slower)
tts.coqui_tts.tts_to_file(
    text="As a professional, I understand the importance of clear communication.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
    language="en",
    file_path="julia_professional.wav",
    speed=0.9  # 10% slower for more deliberate speech
)

# Energetic Sarah (slightly faster)
tts.coqui_tts.tts_to_file(
    text="I'm so excited to help you with your project today!",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3",
    language="en",
    file_path="sarah_energetic.wav",
    speed=1.1  # 10% faster for more energy
)
```

### Different Content Types
```python
# Customer service greeting (Julia)
tts.coqui_tts.tts_to_file(
    text="Thank you for calling our customer service department. My name is Julia, and I'm here to assist you today.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Julia.mp3",
    language="en",
    file_path="julia_customer_service.wav",
    speed=1.0
)

# Friendly greeting (Sarah)
tts.coqui_tts.tts_to_file(
    text="Hi there! I'm Sarah, your personal assistant. I'm here to make your day easier and more enjoyable.",
    speaker_wav="assets/ElevenLabs_Text_to_Speech_audio_Sarah.mp3",
    language="en",
    file_path="sarah_personal_assistant.wav",
    speed=1.0
)
```

## 🎉 **Use Case Examples**

### Professional Applications (Julia)
- **Customer service** - Professional, trustworthy voice
- **Training videos** - Clear, instructional tone
- **Business presentations** - Confident, authoritative
- **Audiobooks** - Engaging, professional narration

### Friendly Applications (Sarah)
- **Personal assistant** - Warm, helpful voice
- **Casual customer service** - Approachable, friendly
- **Educational content** - Encouraging, supportive
- **Gaming** - Friendly character voices

## 🔧 **Testing and Verification**

### Run the Test Script
```bash
python test_woman_voice.py
```

This will:
- ✅ Check all available voice samples
- ✅ Test voice synthesis with Julia voice
- ✅ Show usage examples
- ✅ Verify system is working correctly

### Check Generated Files
```bash
ls -la *.wav | grep -E "(julia|sarah|voice)"
```

## 📝 **Voice Sample Information**

### Julia Voice Sample
- **Source**: ElevenLabs Text-to-Speech
- **Duration**: ~15-20 seconds
- **Quality**: High-quality professional recording
- **Content**: Professional speech sample

### Sarah Voice Sample
- **Source**: ElevenLabs Text-to-Speech
- **Duration**: ~15-20 seconds
- **Quality**: High-quality friendly recording
- **Content**: Warm, approachable speech sample

## 🎯 **Best Practices**

### For Julia Voice
- Use for professional, business contexts
- Slightly slower speed (0.9-1.0) for more authority
- Clear, structured content
- Professional greetings and formal communications

### For Sarah Voice
- Use for friendly, personal contexts
- Normal to slightly faster speed (1.0-1.1) for energy
- Conversational, casual content
- Warm greetings and personal interactions

## ✅ **Summary**

**You now have excellent woman's voice options!**

✅ **Julia** - Professional, confident voice for business use  
✅ **Sarah** - Warm, friendly voice for personal use  
✅ **High-quality ElevenLabs samples** - Excellent voice cloning  
✅ **Easy to use** - Simple command-line and Python interfaces  
✅ **Batch processing** - Create multiple files efficiently  
✅ **Speed control** - Adjust for different contexts  

Both voices are perfect for creating professional-quality WAV files with woman's voices in their mid-30s. The system will clone their voice characteristics and create natural-sounding speech that matches their professional and friendly styles respectively. 