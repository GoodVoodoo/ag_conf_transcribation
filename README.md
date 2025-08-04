# Audio Transcriber

A powerful Python utility for audio/video transcription with AI-powered summarization, speaker analysis, and punctuation. Supports Russian language processing through MTS.ai gRPC API with OpenAI GPT-4o integration for intelligent summaries.

## 🚀 Features

✅ **Multi-format Support** - MP4, MP3, WAV files  
✅ **Automatic Conversion** - FFmpeg-powered audio processing  
✅ **Smart Chunking** - Handles large files automatically  
✅ **Russian Language** - Optimized for Russian speech recognition  
✅ **AI Summarization** - GPT-4o powered conversation summaries  
✅ **Punctuation & Timing** - Accurate timestamps and punctuation  
✅ **Voice Activity Detection** - Advanced VAD algorithms  
✅ **Production Ready** - Robust error handling and timeouts  

## Prerequisites

### macOS/Linux
1. **Python 3.8+**: 
   ```bash
   # macOS
   brew install python@3.9
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install python3 python3-venv python3-pip
   ```

2. **FFmpeg**: Required for audio processing
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt install ffmpeg
   ```

3. **Git**: For cloning the repository
   ```bash
   # macOS
   brew install git
   
   # Ubuntu/Debian
   sudo apt install git
   ```

## Quick Installation

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd ag_conf_transcribation
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install with all dependencies:**
   ```bash
   pip install -e .
   ```

## Configuration

1. **Copy configuration template:**
   ```bash
   cp config.ini.template config.ini
   ```

2. **Edit `config.ini` with your credentials:**
   ```ini
   # gRPC API settings
   api_address = "grpc.audiogram-demo.mts.ai:443"
   use_ssl = true
   timeout = 120  # Increased for reliability
   
   # Authentication (get from your provider)
   client_id = "your-client-id"
   client_secret = "your-client-secret"
   iam_account = "demo"
   iam_workspace = "default"
   sso_url = "https://sso.dev.mts.ai"
   realm = "audiogram-demo"
   verify_sso = true
   
   # OpenAI for summarization (optional)
   openai_api_key = "${OPENAI_API_KEY}"  # or direct key
   openai_model = "gpt-4o"
   openai_temperature = "0.3"
   ```

3. **Set environment variables (optional):**
   ```bash
   # OpenAI API key for summarization
   export OPENAI_API_KEY="your-openai-key"
   
   # Audio processing settings
   export MAX_CHUNK_SIZE_MB=30  # Default: 20MB
   ```

## 🎯 Quick Start

### Test API Connection
```bash
source venv/bin/activate
python -m clients.main models recognize --config config.ini
```

### Basic Transcription
```bash
source venv/bin/activate
python main.py your_audio.wav --output-dir output
```

### With AI Summary
```bash
source venv/bin/activate
python main.py your_audio.wav --output-dir output --add-summarization
```

## 📖 Detailed Usage

### Main Application

**Command:**
```bash
python main.py <input_file> [options]
```

**Options:**
- `input_file`: Audio/video file (MP4, MP3, WAV)
- `--output-dir`: Output directory (default: 'output')
- `--add-summarization`: Generate GPT-4o summary
- `--config`: Config file path (default: 'config.ini')

**Example:**
```bash
python main.py meeting.mp4 --output-dir transcripts --add-summarization
```

### Direct Client Usage

**File Recognition:**
```bash
python -m clients.main recognize file \
  --audio-file audio.wav \
  --config config.ini \
  --model e2e-v3 \
  --enable-punctuator \
  --timeout 120
```

**Available Models:**
```bash
python -m clients.main models recognize --config config.ini
```

## 🎤 Supported Formats & Features

### Input Formats
- **Video:** MP4 (auto-extracts audio)
- **Audio:** MP3, WAV (16kHz recommended)

### Language Support
- **Primary:** Russian 🇷🇺
- **Models:** e2e-v3 (recommended), e2e-v1

### Processing Features
- ✅ **Auto-conversion** to optimal format
- ✅ **Smart chunking** for large files (configurable)
- ✅ **Voice Activity Detection** (VAD)
- ✅ **Punctuation** and timing
- ✅ **Robust timeouts** (120s default)

### AI Features
- ✅ **GPT-4o summaries** (key points, decisions)
- ✅ **Context preservation** for Russian content
- ✅ **Action item extraction**

## 📁 Output Structure

```
output/
├── merged_transcription_YYYYMMDD_HHMMSS.txt  # Final result
├── summary_YYYYMMDD_HHMMSS.txt               # AI summary (if enabled)
└── transcription_YYYYMMDD_HHMMSS/            # Individual chunks
    ├── transcription_1.txt
    ├── transcription_2.txt
    └── ...
```

**Example Output:**
```
Part 1
Speaker None. (00.00s-01.93s): "Марвин, засеки пять минут."
```

## ⚙️ Environment Variables

```bash
# Audio processing
export MAX_CHUNK_SIZE_MB=30        # Default: 20MB

# OpenAI integration  
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o"       # Default: gpt-4o
export OPENAI_TEMPERATURE="0.3"    # Default: 0.3
```

## 🔧 Dependencies

All dependencies are automatically installed with `pip install -e .`:

### Core Dependencies
```python
click>=8.0.0              # CLI framework
grpcio>=1.50.0            # gRPC client
grpcio-tools>=1.50.0      # gRPC development tools
protobuf>=4.21.0          # Protocol Buffers
dynaconf[ini]>=3.1.0      # Configuration management
python-keycloak>=3.0.0    # Authentication
urllib3>=1.26.0           # HTTP client
tabulate>=0.8.0           # Table formatting
tqdm>=4.65.0              # Progress bars
ffmpeg-python>=0.2.0      # Audio processing
openai>=1.0.0             # GPT integration
```

## 🐛 Troubleshooting

### Common Issues

**1. gRPC Timeout Errors:**
```bash
# Increase timeout in config.ini
timeout = 120  # seconds
```

**2. Speaker Labeling Issues:**
```bash
# Use basic punctuation mode if speaker labeling fails
python -m clients.main recognize file --enable-punctuator --timeout 120
```

**3. Missing FFmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian  
sudo apt install ffmpeg
```

**4. INI Configuration Errors:**
```bash
# Ensure dynaconf[ini] is installed
pip install "dynaconf[ini]"
```

**5. Large File Processing:**
```bash
# Adjust chunk size
export MAX_CHUNK_SIZE_MB=50
```

### Model Selection

**Available Models:**
- `e2e-v3` - **Recommended** (latest, best accuracy)
- `e2e-v1` - Legacy version

**Usage:**
```bash
python -m clients.main recognize file --model e2e-v3 --audio-file audio.wav
```

## 🔐 Security Notes

- ✅ `config.ini` is in `.gitignore` (never committed)
- ✅ Use environment variables for sensitive data
- ✅ Demo credentials provided for testing
- ✅ Production: Use your own API credentials

## 📊 Performance

### Tested Performance
- **Small files** (<1MB): ~5-10 seconds
- **Medium files** (10-50MB): ~30-120 seconds  
- **Large files** (>50MB): Auto-chunked processing
- **Languages**: Optimized for Russian 🇷🇺

### Sample Results
```
Input: "Марвин, засеки пять минут." (1.93s audio)
Output: Speaker None. (00.00s-01.93s): "Марвин, засеки пять минут."
Summary: "Brief conversation where speaker instructs Marvin to set a five-minute timer..."
```

## 🛠️ Development

### Project Structure
```
ag_conf_transcribation/
├── main.py                    # Main application entry
├── audio_transcriber/         # Core processing modules
├── clients/                   # gRPC client implementation
├── config.ini.template        # Configuration template
├── pyproject.toml            # Dependencies and build config
└── venv/                     # Virtual environment
```

### Contributing
1. Create virtual environment
2. Install in development mode: `pip install -e .`
3. Run tests: `python -m pytest tests/`
4. Follow existing code patterns