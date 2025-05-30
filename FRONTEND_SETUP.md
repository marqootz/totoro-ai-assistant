# 🎭 Totoro Assistant Frontend Setup

You now have a beautiful animated face interface for your Totoro assistant! The frontend provides visual feedback for different assistant states with smooth animations and color changes.

## 🚀 Quick Start

### 1. Install Dependencies (if not already installed)
```bash
pip install flask flask-cors requests
```

### 2. Start the Frontend Server
```bash
cd frontend
python simple_server.py
```

### 3. Open Your Browser
Visit: **http://localhost:5001**

## 🎨 Visual States

Your Totoro face shows 4 different emotional states:

| State | Color | Animation | When It Appears |
|-------|-------|-----------|-----------------|
| **🔵 Idle** | Blue | Gentle breathing, blinking, eyes look around | Listening for wake word |
| **🟢 Awake** | Green | Eyes widen, alert posture | Wake word detected |
| **🟠 Thinking** | Orange | Rotating dashed ring, moving pupils | Processing command |
| **🔴 Speaking** | Red | Bouncing animation, active eyes | Speaking response |

## 🧪 Testing the Interface

### Option 1: Use the Test Script
```bash
cd frontend
python test_frontend.py
```

### Option 2: Manual API Testing
```bash
# Check status
curl http://localhost:5001/api/status

# Set specific states
curl http://localhost:5001/api/state/idle
curl http://localhost:5001/api/state/awake
curl http://localhost:5001/api/state/thinking
curl http://localhost:5001/api/state/speaking

# Start automatic demo
curl http://localhost:5001/api/demo
```

### Option 3: Browser Controls
- Open http://localhost:5001
- Use the test buttons at the bottom
- Or visit http://localhost:5001?demo=true for auto-cycling

## 🔗 Integration with Your Assistant

The frontend automatically integrates with your main Totoro assistant:

### Full Integration (server.py)
```bash
cd frontend
python server.py  # Connects to your full assistant
```

### Standalone Mode (simple_server.py)
```bash
cd frontend
python simple_server.py  # Works without assistant
```

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML interface
├── style.css           # Styling and animations
├── script.js           # JavaScript state management
├── server.py           # Full integration server
├── simple_server.py    # Standalone server
├── test_frontend.py    # Test script
└── README.md           # Detailed documentation
```

## 🎯 Key Features

✅ **Responsive Design** - Works on desktop and mobile  
✅ **Smooth Animations** - CSS keyframe animations  
✅ **Real-time State Sync** - Updates with assistant activity  
✅ **API Control** - RESTful endpoints for state management  
✅ **Standalone Mode** - Works without full assistant  
✅ **Demo Mode** - Automatic state cycling  
✅ **Mouse Tracking** - Eyes follow cursor when idle  

## 🔧 Customization

### Change Colors
Edit `frontend/style.css`:
```css
.state-idle .head {
    border-color: #your-color;
}
```

### Add New States
1. Update CSS in `style.css`
2. Add JavaScript handling in `script.js`
3. Update valid states in server files

### Modify Animations
Create new keyframe animations in `style.css`:
```css
@keyframes your-animation {
    0% { /* start state */ }
    100% { /* end state */ }
}
```

## 🐛 Troubleshooting

### Server Won't Start
- Check if port 5001 is available: `lsof -i :5001`
- Install dependencies: `pip install flask flask-cors`
- Try the simple server: `python simple_server.py`

### States Not Updating
- Check browser console for errors
- Verify API: `curl http://localhost:5001/api/status`
- Refresh the browser page

### Assistant Integration Issues
- Use standalone mode for testing: `python simple_server.py`
- Check assistant imports: `python -c "from src.assistant import TotoroAssistant"`

## 🎬 Demo Commands

```bash
# Quick demo of all states
cd frontend
python test_frontend.py

# Or manually:
curl http://localhost:5001/api/demo
# Then watch at http://localhost:5001
```

## 🚀 Next Steps

1. **Test the Interface**: Run the demo and see all states
2. **Integrate with Assistant**: Use `server.py` for full integration
3. **Customize**: Modify colors and animations to your liking
4. **Extend**: Add new states or visual elements

Your Totoro assistant now has a face! 🦙✨

---

**Need Help?** Check the detailed `frontend/README.md` or run the test script for troubleshooting. 