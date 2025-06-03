# Fluid Expression System for Big Hero 6-Style Avatars

A comprehensive real-time expression system that combines SVG morphing, sentiment analysis, and performance optimization to create fluid, responsive avatar animations for your Totoro assistant.

## 🎯 Features

### Core Animation System
- **SVG Path Morphing**: Smooth transitions between facial expressions using Flubber.js
- **Performance Optimized**: WebWorker-based sentiment analysis with <60fps monitoring
- **Big Hero 6 Style**: Minimalistic design with <20 control points per shape
- **Real-time Analysis**: Live sentiment detection from LLM responses

### Expression Types
- **Neutral**: Default resting state
- **Happy**: Upward curved mouth, crescent eyes
- **Sad**: Downward mouth, drooping eyes
- **Surprised**: Wide eyes, open mouth
- **Thinking**: Slightly offset eyes, subtle mouth
- **Speaking**: Animated mouth with lip movements

### Technical Implementation
- **Flubber.js**: Path interpolation with relative quadratic Bézier curves
- **GSAP**: High-performance animation timing and easing
- **Socket.IO**: Real-time communication between frontend and backend
- **Sentiment.js**: WebWorker-based text analysis
- **Canvas Fallback**: Mobile device optimization

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install the enhanced requirements
pip install -r requirements-expression-system.txt

# Install Node.js dependencies (for development)
npm install -g live-server  # Optional: for local development
```

### 2. Start the Enhanced Server

```bash
# Start the enhanced Totoro server with expression system
python frontend/enhanced_totoro_server.py
```

### 3. Open the Demo

Navigate to `http://localhost:5000` to see the fluid expression system in action.

## 📁 File Structure

```
frontend/
├── avatar-expression-system.js    # Core expression system
├── avatar-demo.html              # Demo interface
├── enhanced_totoro_server.py     # Backend with WebSocket support
└── style.css                     # Existing styles

requirements-expression-system.txt # Additional dependencies
EXPRESSION_SYSTEM_GUIDE.md         # This guide
```

## 🔧 Configuration Options

### FluidExpressionSystem Options

```javascript
const expressionSystem = new FluidExpressionSystem('containerId', {
    enableSentimentAnalysis: true,    // Enable real-time text analysis
    useWebWorkers: true,              // Use WebWorkers for performance
    fallbackToCanvas: false,          // Canvas fallback for mobile
    maxControlPoints: 20,             // SVG complexity limit
    maxSimultaneousMorphs: 3,         // Performance optimization
    animationDuration: 800            // Animation speed (ms)
});
```

### Performance Guidelines

#### Optimal Settings
- **Desktop**: All features enabled, 60fps target
- **Mobile**: Canvas fallback, reduced morphs
- **Low-end devices**: Disable WebWorkers, immediate transitions

#### Memory Management
- Sentiment history limited to 50 entries
- Animation queue processing with confidence prioritization
- Automatic cleanup on component destruction

## 🎨 Expression Design Guidelines

### SVG Path Requirements
- **Control Points**: Maximum 20 per shape
- **Curve Type**: Relative quadratic Bézier curves preferred
- **Morphing Limits**: Maximum 3 simultaneous element transitions
- **Optimization**: Pre-calculated interpolation functions

### Animation Principles
- **Natural Feel**: Slight stagger between facial elements (50ms)
- **Confidence-based Duration**: Higher confidence = faster transitions
- **Queue Management**: Priority-based expression processing
- **Auto-return**: Neutral state after response completion

## 🔌 API Integration

### REST Endpoints

```bash
# Analyze sentiment
POST /api/analyze_sentiment
{
    "text": "I'm really excited about this!"
}

# Set emotion manually
POST /api/set_emotion
{
    "emotion": "happy",
    "immediate": false
}

# Get performance metrics
GET /api/performance_metrics

# Get sentiment history
GET /api/sentiment_history?limit=20
```

### WebSocket Events

```javascript
// Listen for emotion changes
socket.on('emotion_change', (data) => {
    console.log(`Emotion: ${data.emotion}, Confidence: ${data.confidence}`);
});

// Send text for analysis
socket.emit('analyze_text', {
    text: 'Your message here'
});

// Listen for LLM response chunks
socket.on('llm_response_chunk', (data) => {
    // Real-time expression updates
});
```

## 🧠 Sentiment Analysis

### Emotion Detection Logic

```javascript
// Keyword-based detection
const emotionKeywords = {
    'happy': ['excited', 'amazing', 'fantastic', 'great'],
    'sad': ['disappointed', 'terrible', 'awful', 'bad'],
    'surprised': ['wow', 'incredible', 'unexpected'],
    'thinking': ['think', 'consider', 'analyze', 'hmm']
};

// Polarity-based fallback
if (polarity > 0.3) return 'happy';
if (polarity < -0.3) return 'sad';
if (Math.abs(polarity) > 0.1) return 'surprised';
```

### Confidence Calculation

```javascript
// Confidence based on polarity strength and text length
const confidence = Math.min(
    Math.abs(polarity) + 0.3,  // Base confidence from sentiment
    1.0                        // Maximum confidence cap
);

// Only trigger expression changes above 30% confidence
if (confidence > 0.3) {
    triggerExpressionChange(emotion, confidence);
}
```

## 🎮 Usage Examples

### Basic Integration

```javascript
// Initialize the expression system
const avatar = new FluidExpressionSystem('avatarContainer');

// Manual emotion control
avatar.setExpression('happy');

// Text analysis
avatar.analyzeSentiment('This is amazing!');

// Performance monitoring
setInterval(() => {
    const metrics = avatar.getPerformanceMetrics();
    console.log(`FPS: ${metrics.fps}, Queue: ${metrics.queueLength}`);
}, 1000);
```

### Advanced Configuration

```javascript
// Create with custom options
const avatar = new FluidExpressionSystem('container', {
    enableSentimentAnalysis: true,
    animationDuration: 600,
    maxSimultaneousMorphs: 2
});

// Connect to existing assistant
assistant.onResponse = (text, isComplete) => {
    avatar.analyzeSentiment(text);
    
    if (isComplete) {
        setTimeout(() => avatar.setExpression('neutral'), 3000);
    }
};

// Handle performance issues
avatar.onPerformanceWarning = (metrics) => {
    if (metrics.fps < 30) {
        avatar.options.fallbackToCanvas = true;
    }
};
```

### Real-time Integration

```javascript
// Connect to WebSocket for live updates
const socket = io();

socket.on('llm_response_chunk', (data) => {
    avatar.analyzeSentiment(data.text);
});

socket.on('user_speaking', () => {
    avatar.setExpression('thinking', false);
});

socket.on('assistant_speaking', () => {
    avatar.setExpression('speaking', false);
});
```

## 🔧 Troubleshooting

### Common Issues

#### Performance Problems
```javascript
// Check FPS
const metrics = avatar.getPerformanceMetrics();
if (metrics.fps < 30) {
    // Reduce simultaneous morphs
    avatar.options.maxSimultaneousMorphs = 1;
    
    // Or enable canvas fallback
    avatar.options.fallbackToCanvas = true;
}
```

#### WebWorker Issues
```javascript
// Fallback to main thread
if (!window.Worker) {
    avatar.options.useWebWorkers = false;
}
```

#### SVG Compatibility
```javascript
// Check SVG support
if (!document.createElementNS) {
    console.warn('SVG not supported, using fallback');
    avatar.switchToCanvasFallback();
}
```

### Debug Mode

```javascript
// Enable detailed logging
avatar.options.debug = true;

// Monitor all events
avatar.on('expressionChange', console.log);
avatar.on('sentimentAnalysis', console.log);
avatar.on('performanceUpdate', console.log);
```

## 🚀 Performance Optimization

### Best Practices

1. **Limit Concurrent Animations**: Max 3 simultaneous morphs
2. **Queue Management**: Priority-based with confidence sorting
3. **Memory Cleanup**: Regular history trimming and component cleanup
4. **Mobile Optimization**: Canvas fallback for devices <60fps

### Monitoring

```javascript
// Real-time performance tracking
setInterval(() => {
    const metrics = avatar.getPerformanceMetrics();
    
    if (metrics.fps < 30) {
        console.warn('Performance degradation detected');
        // Implement fallback strategies
    }
}, 5000);
```

## 🎯 Future Enhancements

### Planned Features
- **Lottie Integration**: Complex expression sequences
- **Voice Sync**: Lip-sync with TTS output
- **Custom Expressions**: User-defined emotion paths
- **3D Fallback**: Three.js integration for enhanced depth

### Extensibility
- **Plugin System**: Custom emotion analyzers
- **Theme Support**: Different avatar styles
- **Animation Presets**: Pre-configured expression sets

## 📝 License

This expression system is part of the Totoro Assistant project. See the main project license for details.

## 🤝 Contributing

Contributions are welcome! Please focus on:
- Performance optimizations
- New expression types
- Mobile device support
- Accessibility improvements

---

*Built with ❤️ for creating more expressive and engaging AI assistants* 