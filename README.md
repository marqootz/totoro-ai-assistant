# Totoro Personal Assistant 🦙

A **unified AI assistant** combining smart home excellence with general AI capabilities. Control your smart home devices, get information, perform calculations, and handle complex tasks using natural language - all with complete privacy and zero ongoing costs.

## ✨ What Makes Totoro Special

🏠 **Smart Home Excellence** - Perfect JSON-based command processing with 100% reliability  
🤖 **General AI Capabilities** - Natural conversations, web search, calculations, and more  
🔀 **Unified Commands** - Handle mixed requests like "turn on lights and what time is it?"  
🔒 **Complete Privacy** - Runs entirely local with your own LLM (no cloud required)  
⚡ **Zero Ongoing Costs** - Use your own hardware, no subscription fees  
🎤 **Voice Control** - Natural wake word detection and continuous listening  

## 🎯 Example Commands

**Smart Home Control:**
- *"Turn on the living room lights"*
- *"Play jazz music and dim the bedroom lights to 30%"*
- *"Set the temperature to 72 degrees"*

**General AI Queries:**
- *"What time is it?"*
- *"Calculate 15 * 23 + 45"*
- *"What's the weather like in New York?"*

**Unified Commands (the magic!):**
- *"Turn on the lights and what time is it?"*
- *"Play music and calculate my electric bill: 150 watts * 8 hours"*
- *"Dim bedroom lights to 25% and search for relaxing music"*

## 🚀 Quick Start (3 Steps)

### 1. Clone and Install
```bash
git clone https://github.com/yourusername/totoro.git
cd totoro
pip install -r requirements.txt
```

### 2. Enable Unified Assistant
```bash
python enable_unified_assistant.py
```

### 3. Test Your Assistant
```bash
# Interactive test mode
python main.py --test

# Try these commands:
# - Turn on the living room lights
# - What time is it?
# - Play jazz music and calculate 20 * 30
```

## 🎭 Unified Architecture

Totoro intelligently routes your commands to the right system:

```
Your Command: "Play music and what time is it?"
     ↓
🧠 Input Analysis
     ↓
🏠 Smart Home: play_music → JSON tasks
🤖 General AI: get_time → Tool execution  
     ↓
🔗 Unified Response: "Playing music! The time is 3:42 PM"
```

## 🔧 LLM Backend Options

| Backend | Privacy | Cost | Quality | Setup | Offline |
|---------|---------|------|---------|-------|---------|
| **Unified (Default)** | 🔒 100% | 🆓 Free | ⭐⭐⭐⭐ | Easy | ✅ Yes |
| OpenAI | ⚠️ Cloud | 💰 $0.002/1k | ⭐⭐⭐⭐⭐ | Easy | ❌ No |
| Local Only | 🔒 100% | 🆓 Free | ⭐⭐⭐ | Medium | ✅ Yes |

**Recommendation:** Start with the unified backend for the best balance of capabilities and privacy.

## Features

- 🎤 **Voice Recognition** - Wake word detection and continuous listening
- 🗣️ **Text-to-Speech** - Natural voice responses with 143+ voices
- 🤖 **Multiple LLM Backends** - Choose between OpenAI, local models (Ollama), or unified
- 🏠 **Home Assistant Integration** - Control lights, switches, and other smart devices
- 🎵 **Spotify Integration** - Play music on different speakers/devices
- 📍 **Room Presence Detection** - Context-aware commands based on your location
- 🧠 **Smart Command Processing** - Understand complex, chained commands
- ⚡ **Task Chaining** - Execute multiple actions from a single command
- 🔍 **Web Search** - Real-time information lookup
- 🧮 **Calculations** - Mathematical operations and computations
- 🌤️ **Weather** - Current weather information
- 💬 **Conversation Memory** - Maintains context across interactions

## Installation (Detailed)

### Prerequisites

- Python 3.8 or higher
- Home Assistant Green (or any Home Assistant instance)
- Spotify Premium account (for music control, optional)
- Microphone and speakers
- **One of:**
  - OpenAI API key, OR
  - Ollama installed locally, OR
  - Hugging Face transformers

### System Dependencies

**macOS:**
```bash
# Install PortAudio for PyAudio
brew install portaudio

# Install espeak for text-to-speech (optional)
brew install espeak
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip portaudio19-dev espeak espeak-data libespeak1 libespeak-dev
```

### Python Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd totoro
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Configuration

1. **Copy the example configuration:**
```bash
cp config.env.example .env
```

2. **Edit the `.env` file with your settings:**

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Home Assistant Configuration
HOME_ASSISTANT_URL=http://your-home-assistant-ip:8123
HOME_ASSISTANT_TOKEN=your_long_lived_access_token

# Spotify Configuration (optional)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# Voice Configuration
WAKE_WORD=totoro
VOICE_RATE=200
VOICE_VOLUME=0.9

# Assistant Configuration
ASSISTANT_NAME=Totoro
DEFAULT_ROOM=living_room
```

### Getting API Keys

#### OpenAI API Key
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

#### Home Assistant Long-Lived Access Token
1. In Home Assistant, go to your profile (click your name in the sidebar)
2. Scroll down to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Give it a name and copy the token
5. Add it to your `.env` file

#### Spotify API Credentials (Optional)
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the Client ID and Client Secret
4. Set the redirect URI to `http://localhost:8888/callback`
5. Add credentials to your `.env` file

## Usage

### Voice Mode (Default)
```bash
python main.py
```

The assistant will start listening for the wake word ("totoro" by default). Once it hears the wake word, it will process your command.

### Test Mode (Text Input)
```bash
python main.py --test
```

This mode allows you to type commands instead of using voice, useful for testing and development.

### Single Command Execution
```bash
python main.py --command "turn on the living room lights"
```

Execute a single command and exit.

### Set Room Context
```bash
python main.py --room kitchen --test
```

Start with a specific room context.

## Project Structure

```
totoro/
├── src/
│   ├── __init__.py
│   ├── assistant.py          # Main assistant class
│   ├── config.py             # Configuration management
│   ├── voice/                # Voice recognition and TTS
│   │   ├── speech_recognition.py
│   │   └── text_to_speech.py
│   ├── llm/                  # LLM command processing
│   │   └── command_processor.py
│   ├── integrations/         # External service integrations
│   │   ├── home_assistant.py
│   │   └── spotify_client.py
│   ├── presence/             # Room presence detection
│   │   └── detector.py
│   └── core/                 # Core task execution
│       └── task_executor.py
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
├── config.env.example       # Configuration template
└── README.md
```

## Home Assistant Setup

### Entity Naming Convention

For best results, name your Home Assistant entities with room prefixes:

```yaml
# Example entities
light.living_room_main
light.living_room_lamp
light.bedroom_ceiling
light.kitchen_under_cabinet
switch.living_room_fan
media_player.kitchen_speaker
```

### Creating Long-Lived Access Token

1. In Home Assistant, click on your profile
2. Scroll to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Name it "Totoro Assistant"
5. Copy the token to your `.env` file

## Spotify Setup

### Device Control

The assistant can control Spotify playback on different devices. Make sure your devices are:

1. **Connected to the same network**
2. **Logged into the same Spotify account**
3. **Active in Spotify Connect**

Common device names:
- "Kitchen Speaker"
- "Living Room TV"
- "Bedroom Echo"
- "Office Computer"

## Troubleshooting

### Voice Recognition Issues

1. **Check microphone permissions**
2. **Adjust ambient noise** - The assistant calibrates on startup
3. **Speak clearly** after the wake word
4. **Check internet connection** - Uses Google Speech Recognition

### Home Assistant Connection Issues

1. **Verify URL and token** in `.env` file
2. **Check network connectivity** to Home Assistant
3. **Ensure Home Assistant is running**
4. **Check firewall settings**

### Audio Issues

**macOS:**
```bash
# If you get PyAudio errors
brew install portaudio
pip uninstall pyaudio
pip install pyaudio
```

**Linux:**
```bash
# If you get audio device errors
sudo apt-get install pulseaudio pulseaudio-utils
```

### Common Error Messages

- **"Missing required configuration"** - Check your `.env` file
- **"Home Assistant connection failed"** - Verify URL and token
- **"Could not understand audio"** - Speak more clearly or check microphone
- **"Spotify authentication failed"** - Check Spotify credentials

## Development

### Adding New Actions

1. **Add action to `CommandProcessor`** in `src/llm/command_processor.py`
2. **Implement execution logic** in `src/core/task_executor.py`
3. **Test with text mode** first

### Adding New Integrations

1. **Create integration module** in `src/integrations/`
2. **Add to `TaskExecutor`** initialization
3. **Update configuration** in `src/config.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT API
- Home Assistant community
- Spotify Web API
- Python speech recognition libraries

---

**Note:** This assistant requires active internet connection for voice recognition and LLM processing. Local alternatives can be implemented for privacy-focused deployments. 