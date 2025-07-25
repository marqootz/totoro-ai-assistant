# 🎭 Voice-Reactive Morphing Rings

A stunning visual interface that connects your morphing rings animation to voice input, TTS output, and AI thinking states. The rings dynamically react to your voice, animate while the AI thinks, and provide visual feedback during responses.

## ✨ Features

### 🎙️ **Voice Input Integration**
- **Real-time Audio Analysis**: Rings react to microphone input with dynamic morphing
- **Speech Recognition**: Automatic transcription of voice commands
- **Audio Visualization**: Live frequency bars showing voice activity
- **Voice Level Meter**: Real-time audio level indicator

### 🤖 **AI State Visualization**
- **Listening State**: Blue rings with voice-reactive animations
- **Thinking State**: Golden rings with complex processing animations  
- **Speaking State**: Magenta rings synchronized with TTS output
- **Idle State**: Subtle ambient animations

### 🗣️ **TTS Integration**
- **Backend TTS**: Connects to your existing Coqui/K2-SO voice system
- **Fallback TTS**: Browser-based speech synthesis when backend unavailable
- **Speech Synchronization**: Rings animate in sync with AI responses
- **Dynamic Timing**: Animation intensity matches speech patterns

### 🌐 **Seamless Integration**
- **WebSocket Communication**: Real-time connection between frontend and backend
- **Totoro Integration**: Works with your existing voice and AI systems
- **Fallback Mode**: Continues working even if backend is unavailable
- **Auto-Reconnection**: Automatically reconnects to backend when available

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
# Install voice-reactive rings requirements
pip install -r requirements-voice-rings.txt

# Or install manually:
pip install websockets pygame numpy
```

### 2. **Start the System**
```bash
# Simple startup (recommended)
python start_voice_rings.py

# Or run manually
python voice_ring_integration.py
```

### 3. **Open the Interface**
- Navigate to: `http://localhost:8000/voice-reactive-rings.html`
- Click **"Start Listening"** to enable voice input
- Speak to see the rings react to your voice
- Use the TTS panel to test AI speech synthesis

## 🎮 Controls

### **Mouse Controls**
- **Start/Stop Listening**: Enable/disable voice input
- **Test Thinking**: Trigger thinking animation
- **Test Speaking**: Trigger speaking animation
- **Speak Text**: Use TTS with custom text

### **Keyboard Shortcuts**
- **Spacebar**: Toggle voice listening
- **1**: Set to idle state
- **2**: Start listening
- **3**: Test thinking animation
- **4**: Test speaking animation

## 🔧 Configuration

### **Backend Integration**
The system automatically detects and integrates with your existing Totoro components:

```python
# Automatically detected if available:
from src.voice import VoiceRecognizer, TextToSpeech
from src.assistant import TotoroAssistant
```

### **Standalone Mode**
If Totoro components aren't available, the system runs in demo mode with:
- Browser-based speech recognition
- Local TTS synthesis
- Simulated AI responses

### **WebSocket Settings**
Modify connection settings in `voice_ring_integration.py`:
```python
server = VoiceRingServer(host="localhost", port=8765)
```

## 🎨 Visual States

### **🔵 Listening State**
- **Color**: Cyan/Blue gradient
- **Animation**: Voice-reactive ring morphing
- **Glow**: Blue drop-shadow effect
- **Behavior**: Responds to microphone input levels

### **🟡 Thinking State**  
- **Color**: Gold/Orange gradient
- **Animation**: Complex multi-frequency oscillations
- **Glow**: Golden drop-shadow effect
- **Behavior**: Random variations simulating processing

### **🔴 Speaking State**
- **Color**: Magenta/Pink gradient
- **Animation**: Synchronized with TTS output
- **Glow**: Magenta drop-shadow effect
- **Behavior**: Amplitude matches speech patterns

### **⚫ Idle State**
- **Color**: Gray gradient
- **Animation**: Subtle ambient morphing
- **Glow**: No glow effect
- **Behavior**: Minimal, calming movement

## 🔗 Architecture

### **Frontend (HTML/JavaScript)**
- **SVG Morphing Rings**: Procedural animation system
- **WebSocket Client**: Real-time communication with backend
- **Audio Visualization**: Real-time frequency analysis
- **Fallback Systems**: Local TTS and speech recognition

### **Backend (Python/WebSocket)**
- **Voice Processing**: Integration with Totoro voice systems
- **State Management**: Synchronizes AI states across clients
- **Event Queue**: Asynchronous processing of voice events
- **Multi-Client**: Supports multiple simultaneous connections

### **Communication Protocol**
```json
// Frontend → Backend
{
  "command": "start_listening",
  "data": {...}
}

// Backend → Frontend  
{
  "type": "state_change",
  "new_state": "thinking",
  "timestamp": 1234567890
}
```

## 🎯 Use Cases

### **🏠 Smart Home Interface**
- Visual feedback for voice commands
- Status indication for home automation
- Ambient interface for always-on AI

### **🎤 Podcast/Streaming**
- Visual representation of AI responses
- Audience engagement during live streams
- Professional AI interview interface

### **🧠 AI Development**
- Debug interface for voice processing
- Visual feedback for model performance
- Real-time monitoring of AI states

### **🎨 Art Installation**
- Interactive voice-reactive art piece
- Dynamic visual meditation aid
- Responsive ambient display

## 🛠️ Customization

### **Ring Parameters**
Modify animation properties in the HTML:
```javascript
// Animation parameters
this.centerX = 150;
this.centerY = 150;
this.baseRadius = 100;
this.numPoints = 8;
```

### **Color Schemes**
Update gradients in the SVG definitions:
```html
<radialGradient id="listeningGradient">
  <stop offset="0%" style="stop-color:#51ABFA"/>
  <stop offset="100%" style="stop-color:#51ABFA"/>
</radialGradient>
```

### **Audio Sensitivity**
Adjust microphone settings:
```javascript
audio: { 
  echoCancellation: true,
  noiseSuppression: true,
  sampleRate: 44100
}
```

## 🔍 Troubleshooting

### **❌ Microphone Not Working**
- Check browser permissions for microphone access
- Ensure microphone is selected as default input device
- Try refreshing the page and granting permissions again

### **❌ Backend Connection Failed**
- Verify `voice_ring_integration.py` is running
- Check WebSocket port 8765 is not blocked
- Look for errors in Python console output

### **❌ No Voice Recognition**
- Ensure internet connection (Google Speech API required)
- Speak clearly and at normal volume
- Check microphone levels in system settings

### **❌ TTS Not Working**
- Verify your existing TTS system is functional
- Check browser console for error messages
- Try the fallback browser TTS by entering text manually

## 🤝 Integration with Existing Systems

### **Totoro Assistant**
- Automatically uses your existing `TotoroAssistant` class
- Preserves conversation context and memory
- Maintains your custom AI personality and responses

### **Voice Recognition**
- Integrates with your `VoiceRecognizer` configuration
- Respects wake word settings ("totoro")
- Uses your preferred microphone settings

### **TTS Systems**
- Connects to Coqui TTS with voice cloning
- Maintains your K2-SO voice character
- Falls back to system TTS if needed

## 🎊 What You've Built

You now have a **complete voice-reactive AI interface** that:

✅ **Reacts to your voice** with beautiful morphing ring animations  
✅ **Shows AI thinking** with dynamic visual feedback  
✅ **Animates during responses** synchronized with speech output  
✅ **Integrates seamlessly** with your existing Totoro infrastructure  
✅ **Works offline** with intelligent fallback systems  
✅ **Supports multiple clients** for collaborative experiences  
✅ **Provides real-time feedback** for voice processing states  

This creates an **immersive, futuristic AI interaction experience** that makes your voice conversations with AI feel magical and responsive!

---

*🎭 Created for the Totoro AI Assistant project - where technology meets artistry in voice interaction.* 