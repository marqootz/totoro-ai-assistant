# 🏠 Local LLM Setup Guide for Totoro

This guide will help you set up Totoro to use local LLMs instead of OpenAI, giving you complete privacy and control over your smart home assistant.

## 🎯 Why Use Local LLMs?

### ✅ Pros
- **Complete Privacy**: Your voice commands never leave your home
- **No API Costs**: No monthly fees or per-request charges
- **Offline Operation**: Works without internet connection
- **Full Control**: Customize and fine-tune the model for your needs
- **No Rate Limits**: Process as many commands as you want
- **Data Sovereignty**: Your conversations stay on your hardware

### ⚠️ Cons
- **Hardware Requirements**: Needs decent CPU/GPU for good performance
- **Setup Complexity**: More initial configuration required
- **Model Quality**: May not be as sophisticated as GPT-4
- **Maintenance**: You're responsible for updates and troubleshooting

## 🚀 Option 1: Ollama (Recommended)

Ollama is the easiest way to run local LLMs. It handles model management and provides a simple API.

### Installation

#### macOS
```bash
# Install Ollama
brew install ollama

# Or download from https://ollama.ai
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows
Download from [ollama.ai](https://ollama.ai) and run the installer.

### Setup

1. **Start Ollama service**:
```bash
ollama serve
```

2. **Download a model** (choose one):
```bash
# Lightweight, fast (3.8GB)
ollama pull llama3.2

# Better quality, slower (7.4GB)
ollama pull llama3.1:8b

# High quality, needs good hardware (26GB)
ollama pull llama3.1:70b

# Specialized for coding/instructions (4.1GB)
ollama pull codellama
```

3. **Test the model**:
```bash
ollama run llama3.2
# Type: "Hello, how are you?" and press Enter
# Type: "/bye" to exit
```

4. **Configure Totoro**:
```env
# In your .env file
LLM_BACKEND=local
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.2
```

### Model Recommendations

| Model | Size | RAM Needed | Speed | Quality | Best For |
|-------|------|------------|-------|---------|----------|
| `llama3.2` | 3.8GB | 8GB | Fast | Good | General use, older hardware |
| `llama3.1:8b` | 7.4GB | 12GB | Medium | Better | Balanced performance |
| `mistral` | 4.1GB | 8GB | Fast | Good | Efficient, multilingual |
| `codellama` | 4.1GB | 8GB | Fast | Good | Code understanding |

## 🤖 Option 2: Hugging Face Transformers

Run models directly with Python transformers library.

### Installation
```bash
pip install transformers torch torchvision torchaudio
```

### Configuration
```env
# In your .env file
LLM_BACKEND=huggingface
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium
```

### Model Options

| Model | Size | Description |
|-------|------|-------------|
| `microsoft/DialoGPT-medium` | 345MB | Conversational AI |
| `microsoft/DialoGPT-large` | 774MB | Better conversations |
| `facebook/blenderbot-400M-distill` | 400MB | Facebook's chatbot |
| `google/flan-t5-base` | 248MB | Instruction following |

## 🔧 Option 3: Custom API Endpoint

If you're running your own LLM server (like text-generation-webui, FastChat, etc.):

### Configuration
```env
LLM_BACKEND=local
LOCAL_LLM_URL=http://your-server:port
LOCAL_LLM_MODEL=your-model-name
```

## ⚡ Performance Optimization

### Hardware Requirements

**Minimum**:
- 8GB RAM
- 4-core CPU
- 50GB free disk space

**Recommended**:
- 16GB+ RAM
- 8-core CPU or GPU
- 100GB+ free disk space

### GPU Acceleration

#### NVIDIA GPU (CUDA)
```bash
# Install CUDA support for Ollama
# Ollama automatically uses GPU if available

# For Hugging Face models
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Apple Silicon (M1/M2/M3)
```bash
# Ollama automatically uses Metal acceleration
# For Hugging Face models, install MPS support
pip install torch torchvision torchaudio
```

### Model Quantization

Use quantized models for better performance:
```bash
# 4-bit quantized models (smaller, faster)
ollama pull llama3.2:q4_0
ollama pull llama3.2:q4_k_m

# 8-bit quantized models (balanced)
ollama pull llama3.2:q8_0
```

## 🎛️ Fine-tuning for Smart Home

### Custom System Prompts

The local LLM processor includes optimized prompts for smart home control. You can customize them by editing `src/llm/local_llm_processor.py`.

### Training Data

To improve performance, you can fine-tune models with your specific commands:

1. **Collect your commands**:
```json
[
  {"input": "turn on living room lights", "output": "turning on living room lights"},
  {"input": "play jazz music", "output": "playing jazz music"},
  {"input": "set bedroom temperature to 72", "output": "setting bedroom to 72 degrees"}
]
```

2. **Use tools like**:
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl)
- [LLaMA Factory](https://github.com/hiyouga/LLaMA-Factory)
- [Unsloth](https://github.com/unslothai/unsloth)

## 🔍 Troubleshooting

### Common Issues

1. **"Could not connect to local LLM"**
   - Check if Ollama is running: `ollama list`
   - Verify the URL: `curl http://localhost:11434/api/tags`

2. **Slow responses**
   - Use a smaller model: `ollama pull llama3.2:q4_0`
   - Check system resources: `htop` or Activity Monitor

3. **Poor command understanding**
   - Try a larger model: `ollama pull llama3.1:8b`
   - Adjust the system prompt in the code

4. **Out of memory errors**
   - Use quantized models
   - Close other applications
   - Reduce model size

### Performance Monitoring

```bash
# Check Ollama status
ollama ps

# Monitor system resources
htop

# Check GPU usage (NVIDIA)
nvidia-smi

# Check GPU usage (Apple Silicon)
sudo powermetrics --samplers gpu_power -n 1
```

## 🔄 Switching Between Backends

You can easily switch between different LLM backends:

```bash
# Use OpenAI
echo "LLM_BACKEND=openai" >> .env

# Use local Ollama
echo "LLM_BACKEND=local" >> .env

# Use Hugging Face
echo "LLM_BACKEND=huggingface" >> .env
```

Then restart Totoro:
```bash
python main.py --test
```

## 📊 Comparison Matrix

| Feature | OpenAI | Local (Ollama) | Hugging Face |
|---------|--------|----------------|--------------|
| Privacy | ❌ | ✅ | ✅ |
| Cost | 💰 | Free | Free |
| Setup | Easy | Medium | Hard |
| Quality | Excellent | Good | Fair |
| Speed | Fast | Medium | Slow |
| Offline | ❌ | ✅ | ✅ |
| Customization | Limited | High | Highest |

## 🎯 Recommended Setup

**For beginners**: Start with Ollama + `llama3.2`
**For privacy-focused**: Ollama + `llama3.1:8b`
**For developers**: Hugging Face + custom fine-tuning
**For best quality**: OpenAI (if privacy isn't a concern)

---

**🎉 Ready to go private? Your smart home assistant can now run completely offline!** 