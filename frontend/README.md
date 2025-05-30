# Totoro Assistant Frontend

A beautiful animated face interface for the Totoro voice assistant that provides visual feedback for different assistant states.

## Features

🎭 **Animated Face with Emotional States:**
- **Idle**: Calm blue glow, gentle blinking, eyes occasionally look around
- **Awake**: Bright green glow, alert eyes, responsive pupils  
- **Thinking**: Orange glow, rotating dashed ring, pupils moving in patterns
- **Speaking**: Red glow, bouncing animation, active eye movements

## Quick Start

### 1. Install Dependencies
```bash
pip install flask flask-cors
```

### 2. Start the Frontend Server
```bash
cd frontend
python server.py
```

### 3. Open Your Browser
Visit: `http://localhost:5001`

## Visual States

### 🔵 Idle State
- **Color**: Blue (#4a9eff)
- **Animation**: Gentle breathing effect, occasional blinking
- **When**: Assistant is listening for wake word

### 🟢 Awake State  
- **Color**: Green (#00ff88)
- **Animation**: Eyes widen, alert posture
- **When**: Wake word detected, ready for command

### 🟠 Thinking State
- **Color**: Orange (#ffa500)
- **Animation**: Rotating dashed ring, pupils moving in patterns
- **When**: Processing your command

### 🔴 Speaking State
- **Color**: Red (#ff4757)  
- **Animation**: Gentle bouncing, active eye movements
- **When**: Assistant is speaking response

## API Endpoints

### Get Status
```bash
curl http://localhost:5001/api/status
```

### Set State Manually
```bash
curl http://localhost:5001/api/state/thinking
```

### Start Demo Mode
```bash
curl http://localhost:5001/api/demo
```

### Send Command (if assistant connected)
```bash
curl http://localhost:5001/api/command/what%20time%20is%20it
```

## Testing Modes

### 1. Standalone Mode (No Assistant)
Just open `http://localhost:5001` and use the test buttons to see different states.

### 2. Demo Mode
Visit `http://localhost:5001?demo=true` for automatic state cycling.

### 3. Connected Mode  
When the full Totoro assistant is running, the face automatically syncs with the assistant's actual state.

## Integration with Main Assistant

The frontend automatically connects to your Totoro assistant when available:

1. **Automatic State Sync**: Face state updates in real-time based on assistant activity
2. **Voice Command Feedback**: Visual feedback during wake word detection, processing, and speaking
3. **Error Handling**: Gracefully handles assistant disconnection

## Customization

### Modify Colors
Edit `style.css` and change the color values:
```css
.state-idle .head {
    border-color: #your-color;
}
```

### Adjust Animations
Modify keyframe animations in `style.css`:
```css
@keyframes your-animation {
    /* Your custom animation */
}
```

### Add New States
1. Add CSS classes in `style.css`
2. Update JavaScript state handling in `script.js`
3. Update valid states in `server.py`

## Troubleshooting

### Frontend Won't Start
- Check if Flask is installed: `pip install flask flask-cors`
- Ensure port 5001 is available
- Check for Python path issues

### No Assistant Connection
- This is normal for standalone testing
- Check that the main assistant is running
- Verify the assistant imports work: `python -c "from src.assistant import TotoroAssistant"`

### States Not Updating
- Check browser console for JavaScript errors
- Verify API endpoints are responding: `curl http://localhost:5001/api/status`
- Check server logs for backend errors

## Development

### File Structure
```
frontend/
├── index.html      # Main HTML interface
├── style.css       # Styling and animations
├── script.js       # JavaScript state management
├── server.py       # Flask backend server
└── README.md       # This file
```

### Adding Features
1. **New Visual Elements**: Add to `index.html` and style in `style.css`
2. **New Animations**: Create keyframes in `style.css`
3. **New API Endpoints**: Add routes to `server.py`
4. **State Logic**: Update `script.js` and assistant integration

## Mobile Support

The interface is responsive and works on mobile devices:
- Touch-friendly controls
- Scaled animations for smaller screens
- Optimized for portrait and landscape

Enjoy your new Totoro assistant interface! 🦙✨ 