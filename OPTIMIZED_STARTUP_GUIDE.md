# Optimized Totoro Startup Guide

## 🚀 Quick Start (Recommended)

### **One-Command Startup:**
```bash
python start_optimized_totoro.py
```

This automatically:
- ✅ Kills existing servers on ports 5000, 5001, 5002, 8000
- ✅ Cleans up lingering Totoro processes
- ✅ Applies performance optimizations 
- ✅ Starts enhanced frontend with visual feedback
- ✅ Validates all dependencies

## 🛠️ Manual Server Management

### **Clean Up Existing Servers:**
```bash
python cleanup_servers.py
```

### **Start Enhanced Frontend (after cleanup):**
```bash
cd frontend && python enhanced_server.py
```

### **Test Fast Voice Backend:**
```bash
python fast_voice_backend.py
```

## ⚡ Performance Optimizations Applied

The startup script automatically applies these optimizations:

| Setting | Optimized Value | Impact |
|---------|-----------------|--------|
| `VOICE_PREFERENCE` | `system` | 4.9x faster TTS |
| `OLLAMA_MODEL` | `llama3.2:latest` | 2.5x faster LLM |
| `RECOGNITION_TIMEOUT` | `15` | Faster failure detection |
| `COMMAND_TIMEOUT` | `8` | Responsive interactions |
| `TTS_RATE` | `200` | Faster speech output |

## 🎯 Expected Performance

### **Response Times:**
- **Simple commands** ("what time is it"): 2-3 seconds
- **Smart home** ("turn on lights"): 3-4 seconds  
- **Complex queries** ("tell me a joke"): 4-5 seconds

### **Visual Feedback:**
- Real-time state transitions: Idle → Awake → Thinking → Speaking
- Loading progress for neural model initialization
- Mouse-responsive eye tracking

## 🔧 Troubleshooting

### **Port Conflicts:**
```bash
# If you get "Address already in use" errors:
python cleanup_servers.py
# Then restart
python start_optimized_totoro.py
```

### **Slow Performance:**
```bash
# Check if optimizations are applied:
echo $VOICE_PREFERENCE  # Should be "system"
echo $OLLAMA_MODEL      # Should be "llama3.2:latest"

# Force apply optimizations:
export VOICE_PREFERENCE=system
export OLLAMA_MODEL=llama3.2:latest
```

### **Dependencies Not Ready:**
```bash
# Start Ollama LLM service:
ollama serve

# Check Ollama is running:
curl -s http://localhost:11434/api/tags
```

### **Audio Issues:**
```bash
# Close conflicting audio apps:
osascript -e 'tell application "iTunes" to quit'
osascript -e 'tell application "Spotify" to quit'
osascript -e 'tell application "Music" to quit'
```

## 📊 Server Status Monitoring

### **Check Running Servers:**
```bash
# See what's running on Totoro ports:
lsof -i :5000 -i :5001 -i :5002 -i :8000

# Check enhanced server specifically:
curl -s http://localhost:5002/ | head -5
```

### **Performance Testing:**
```bash
# Test current response speeds:
python test_response_speed.py

# Full performance analysis:
python optimize_voice_performance.py

# Voice delay diagnostics:
python diagnose_voice_delays.py
```

## 🎮 Frontend Features

### **Enhanced Visual Interface:**
- **Animated Totoro face** with expressive eyes
- **Real-time state indicators**: 
  - 🔵 Idle (breathing, blinking)
  - 🟢 Awake (alert, ready)  
  - 🟠 Thinking (rotating ring)
  - 🔴 Speaking (bouncing animation)
  - 🟣 Loading (progress bar)
  - ❌ Error (shake animation)

### **Interactive Controls:**
- Manual state testing buttons
- Voice mode start/stop controls
- Real-time command processing
- Mouse-responsive eye tracking

## 🔄 Startup Sequence

The optimized startup script follows this sequence:

1. **🧹 Cleanup Phase** (2-3 seconds)
   - Scan ports 5000, 5001, 5002, 8000
   - Kill existing Flask/Python servers
   - Wait for clean termination

2. **⚡ Optimization Phase** (1 second)
   - Set performance environment variables
   - Configure fast TTS and LLM settings

3. **🔍 Validation Phase** (2-5 seconds)
   - Check Ollama LLM service
   - Validate network connectivity
   - Confirm model availability

4. **🎭 Launch Phase** (3-5 seconds)
   - Start enhanced frontend server
   - Initialize visual components
   - Ready for voice interactions

**Total startup time: 8-14 seconds**

## 💡 Tips for Best Performance

### **System Optimization:**
- Close unnecessary applications (especially audio apps)
- Ensure good internet connection for speech recognition
- Use wired microphone for better voice detection
- Keep Ollama running in background for faster startup

### **Voice Interaction Tips:**
- Speak clearly: "Totoro, [command]"
- Wait for visual feedback before next command
- Use simple, direct language
- Keep commands under 8 seconds

### **Model Selection:**
```bash
# Fastest (recommended):
export OLLAMA_MODEL=llama3.2:latest  # 2GB

# Higher quality (slower):
export OLLAMA_MODEL=llama3.1:8b      # 5GB
```

## 🎯 Next Steps

1. **Start Totoro**: `python start_optimized_totoro.py`
2. **Visit Frontend**: http://localhost:5002
3. **Test Voice**: Click "Start Voice" and say "Totoro, what time is it?"
4. **Monitor Performance**: Watch visual feedback and response times

Your Totoro assistant is now optimized for **sub-5 second responses** with beautiful visual feedback! 🎭✨ 