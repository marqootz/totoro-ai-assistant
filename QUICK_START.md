# Quick Start Guide - Fluid Expression System

## 🎉 System Status: RUNNING ✅

Your Big Hero 6-style fluid expression system is now successfully running with **automatic server cleanup**!

## 🌐 Access the Demo

**Main Demo Page:** http://localhost:3000/

**API Endpoints:**
- Status: http://localhost:3000/api/status
- Sentiment Analysis: POST http://localhost:3000/api/analyze_sentiment
- Set Emotion: POST http://localhost:3000/api/set_emotion
- Performance Metrics: http://localhost:3000/api/performance_metrics
- Sentiment History: http://localhost:3000/api/sentiment_history

## 🚀 Features Currently Active

### ✅ Working Features
- **Real-time Sentiment Analysis** - Analyzes text and determines emotions
- **Manual Emotion Control** - Set avatar emotions directly
- **Performance Monitoring** - Tracks system performance
- **RESTful API** - Full API for integration
- **Big Hero 6 Style Avatar** - Minimalistic design with fluid expressions
- **🆕 Automatic Server Cleanup** - Kills existing servers before starting

### 🎭 Available Emotions
- `neutral` - Default resting state
- `happy` - Positive, excited expressions
- `sad` - Disappointed, upset expressions  
- `surprised` - Wide-eyed, amazed expressions
- `thinking` - Contemplative, analytical expressions
- `speaking` - Active communication expressions

## 🧪 Test the System

### Test Sentiment Analysis
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"I am so excited about this amazing project!"}' \
  http://localhost:3000/api/analyze_sentiment
```

### Set Manual Emotion
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"emotion":"surprised","immediate":true}' \
  http://localhost:3000/api/set_emotion
```

### Check System Status
```bash
curl http://localhost:3000/api/status
```

## 🔧 Technical Implementation

### Core Technologies
- **Flask** - Web framework
- **TextBlob** - Sentiment analysis
- **SVG Morphing** - Fluid facial expressions
- **GSAP** - Animation timing
- **Real-time Analysis** - Live emotion detection

### Performance Optimizations
- **<20 control points** per facial shape
- **<60fps** animation monitoring
- **Relative quadratic Bézier curves** for smooth morphing
- **Limited simultaneous morphing** to 3 elements max

## 🎨 Expression System Architecture

```
Text Input → Sentiment Analysis → Emotion Classification → SVG Morphing → Fluid Animation
```

### Emotion Detection Pipeline
1. **Text Analysis** - TextBlob sentiment analysis
2. **Keyword Matching** - Emotion-specific word detection
3. **Confidence Scoring** - Weighted emotion confidence
4. **Expression Mapping** - Emotion to visual expression
5. **Smooth Transitions** - Fluid morphing between states

## 🔄 Next Steps

1. **Open the demo page** at http://localhost:3000/
2. **Test the sentiment analysis** with different text inputs
3. **Try manual emotion controls** to see immediate changes
4. **Monitor performance metrics** for optimization
5. **Integrate with your Totoro assistant** for real-time responses

## 🛠️ Server Management

### Start Server (Auto-Cleanup Enabled)
```bash
cd frontend
python basic_demo_server.py
```
**✨ The server automatically kills existing instances before starting!**

### Stop Server
```bash
pkill -f basic_demo_server
```

### Change Port
```bash
PORT=8080 python basic_demo_server.py
```

## 🆕 Auto-Cleanup Features

The `basic_demo_server.py` now includes:

- **🔄 Automatic Process Termination** - Kills existing demo servers before starting
- **🎯 Port Conflict Resolution** - Automatically frees up ports in use
- **🧹 Clean Startup** - Ensures no conflicts with previous instances
- **📋 Process Pattern Matching** - Identifies and terminates related server processes

### What Gets Cleaned Up
- `demo_expression_server` processes
- `simple_demo_server` processes  
- `basic_demo_server` processes
- `enhanced_totoro_server` processes
- Any process using the target port

## 📊 Current Configuration

- **Server:** Basic Flask (no SocketIO for stability)
- **Port:** 3000 (configurable via PORT env var)
- **Mode:** Demo mode with sentiment analysis
- **Performance:** 60fps target, real-time processing
- **Compatibility:** macOS optimized, cross-platform ready
- **Cleanup:** Automatic server conflict resolution

---

**🎭 Your Big Hero 6-style avatar expression system is ready for action!**

Navigate to http://localhost:3000/ to see the fluid expressions in action.

**💡 Pro Tip:** You can now run `python basic_demo_server.py` multiple times without worrying about port conflicts - the server will automatically clean up previous instances! 