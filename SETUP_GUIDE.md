# 🎭 Totoro Personal Assistant - Quick Setup Guide

## ✅ Installation Complete!

Your Totoro Personal Assistant is now installed and ready for configuration. All core components have been tested and are working correctly.

## 🔧 Next Steps

### 1. Get Your API Keys

#### OpenAI API Key (Required)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

#### Home Assistant Token (Required)
1. Open your Home Assistant web interface
2. Click on your profile (bottom left)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Give it a name like "Totoro Assistant"
6. Copy the generated token

#### Spotify Credentials (Optional)
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy Client ID and Client Secret
4. Set redirect URI to `http://localhost:8888/callback`

### 2. Create Configuration File

Copy the example configuration:
```bash
cp config.env.example .env
```

Edit `.env` with your credentials:
```env
# Required
OPENAI_API_KEY=sk-your-actual-openai-key-here
HOME_ASSISTANT_URL=http://your-home-assistant-ip:8123
HOME_ASSISTANT_TOKEN=your-actual-home-assistant-token

# Optional (for Spotify)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

### 3. Test the System

#### Text Mode (Recommended First)
```bash
python main.py --test
```

#### Single Command Test
```bash
python main.py --command "turn on the living room lights"
```

#### Voice Mode (After text mode works)
```bash
python main.py
```

## 🏠 Home Assistant Setup Tips

### Entity Naming
For best results, name your entities with room prefixes:
- `light.living_room_main`
- `light.bedroom_ceiling`
- `light.kitchen_under_cabinet`
- `switch.living_room_fan`

### Finding Your Home Assistant IP
```bash
# On your network, find devices
nmap -sn 192.168.1.0/24 | grep -B2 -A2 "home"
```

Or check your router's admin panel for connected devices.

## 🎵 Spotify Setup

### Device Names
Make sure your Spotify devices have clear names:
- "Kitchen Speaker"
- "Living Room TV"
- "Bedroom Echo"
- "Office Computer"

### First Time Setup
The first time you use Spotify features, you'll need to authorize the app by visiting a URL and copying the redirect URL back.

## 🗣️ Voice Commands Examples

Once configured, try these commands:

- *"Totoro, turn on the living room lights"*
- *"Play some jazz music in the kitchen"*
- *"Dim the bedroom lights to 50%"*
- *"Turn off all the lights and pause the music"*
- *"Play my workout playlist on the office speakers"*

## 🔧 Troubleshooting

### Common Issues

1. **"Missing required configuration"**
   - Check your `.env` file exists and has the right values

2. **"Home Assistant connection failed"**
   - Verify the URL and token
   - Make sure Home Assistant is running
   - Check firewall settings

3. **"Could not understand audio"**
   - Speak clearly after saying "Totoro"
   - Check microphone permissions
   - Ensure good internet connection

4. **PyAudio errors on macOS**
   ```bash
   brew install portaudio
   pip uninstall pyaudio
   pip install pyaudio
   ```

### Getting Help

1. Check the logs in `totoro.log`
2. Run the basic test: `python test_basic.py`
3. Try text mode first: `python main.py --test`

## 🚀 Advanced Features

### Room Presence Detection
Configure Bluetooth devices in `.env`:
```env
BLUETOOTH_DEVICES=["AA:BB:CC:DD:EE:FF", "11:22:33:44:55:66"]
```

### Custom Wake Word
Change the wake word in `.env`:
```env
WAKE_WORD=jarvis
```

### Voice Settings
Adjust speech rate and volume:
```env
VOICE_RATE=180
VOICE_VOLUME=0.8
```

## 📝 Development

### Adding New Commands
1. Edit `src/llm/command_processor.py` to add new actions
2. Implement execution in `src/core/task_executor.py`
3. Test with `python main.py --test`

### Project Structure
```
totoro/
├── src/
│   ├── assistant.py          # Main coordinator
│   ├── voice/                # Speech & TTS
│   ├── llm/                  # Command processing
│   ├── integrations/         # Home Assistant & Spotify
│   ├── presence/             # Room detection
│   └── core/                 # Task execution
├── main.py                   # Entry point
└── test_basic.py            # Component tests
```

---

**🎉 You're all set! Your personal assistant is ready to help you control your smart home with voice commands.** 