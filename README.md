# Audio Transcriber

A Python utility for audio extraction and transcription with speaker labeling and punctuation.

## Prerequisites for macOS

1. **Python**: Requires Python 3.8 or newer
   ```bash
   brew install python@3.9
   ```

2. **FFmpeg**: Required for audio processing
   ```bash
   brew install ffmpeg
   ```

3. **Git**: For cloning the repository
   ```bash
   brew install git
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd audio-transcriber
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the package and its dependencies:
   ```bash
   pip install .
   ```

## Configuration

1. Create a `config.ini` file in the project root (if not already present) with your API credentials:
   ```ini
   api_address = "grpc.audiogram-demo.mts.ai:443"
   use_ssl = true
   timeout = 60
   client_id = "your-client-id"
   client_secret = "your-client-secret"
   iam_account = "demo"
   iam_workspace = "default"
   sso_url = "https://sso.dev.mts.ai"
   realm = "audiogram-demo"
   verify_sso = true
   ```

## Configuration Management

The application uses a `config.ini` file for its settings. To protect sensitive data:

1. Copy the template configuration:
   ```bash
   cp config.ini.template config.ini
   ```

2. Edit `config.ini` and fill in your values for:
   - client_id
   - client_secret
   - iam_account
   - iam_workspace

3. Environment Variables (Optional):
   - `MAX_CHUNK_SIZE_MB`: Maximum size in MB for audio chunks (default: 20)
   ```bash
   # Example: Set 30MB as maximum chunk size
   export MAX_CHUNK_SIZE_MB=30  # On Unix/macOS
   # or
   $env:MAX_CHUNK_SIZE_MB=30    # On Windows PowerShell
   ```

**Security Notes:**
- Never commit `config.ini` to git (it's already in `.gitignore`)
- Use a secure password manager for storing and sharing credentials
- The pre-commit hooks will help prevent accidentally committing sensitive data

4. Pre-commit Setup (For Developers):
   ```bash
   pip install pre-commit
   pre-commit install
   ```
   This will install hooks that prevent committing:
   - Files containing secrets
   - Private keys
   - Large files
   - Files with case conflicts

## Usage

The application supports processing audio and video files (mp4, mp3, wav) and generates transcriptions with speaker labeling and punctuation.

### Basic Usage

```bash
python -m audio_transcriber --input path/to/your/audio/file.mp3 --output-dir output
```

### Command Line Arguments

- `--input` or `-i`: Path to the input audio/video file (required)
- `--output-dir` or `-o`: Directory to save the transcription results (default: 'output')

### Supported Input Formats

- MP4 video files
- MP3 audio files
- WAV audio files

### Output

The application will:
1. Convert the input file to WAV format if needed
2. Split the audio into chunks if necessary
3. Transcribe the audio with speaker labeling and punctuation
4. Save the results in the specified output directory

### Environment Variables

You can configure the maximum chunk size for audio processing:

```bash
# On Windows PowerShell
$env:MAX_CHUNK_SIZE_MB=30

# On Unix/macOS
export MAX_CHUNK_SIZE_MB=30
```

Default value is 20MB if not specified.