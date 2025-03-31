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
python main.py path/to/your/audio/file.mp4 --output-dir output
```

### Command Line Arguments

- `input_file`: Path to the input audio/video file (positional argument, required)
- `--output-dir`: Directory to save the transcription results (default: 'output')
- `--add-summarization`: Generate a summary of the transcription using GPT-4o
- `--config`: Path to the configuration file (default: 'config.ini')

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

## Summarization Feature

The application now supports generating summaries of transcribed conversations using OpenAI's GPT-4o model.

### Usage

To enable summarization, use the `--add-summarization` flag:

```bash
python main.py path/to/your/audio/file.mp4 --output-dir output --add-summarization
```

### Configuration

For the summarization feature to work, you need to set your OpenAI API key in one of two ways:

1. **Environment Variable**:
   ```bash
   # On Windows PowerShell
   $env:OPENAI_API_KEY="your-openai-api-key"

   # On Unix/macOS
   export OPENAI_API_KEY="your-openai-api-key"
   ```

2. **Config File**:
   Add the following section to your `config.ini` file:
   ```ini
   # OpenAI GPT settings
   openai_api_key = "${OPENAI_API_KEY}"  # Will read from environment variable
   openai_model = "gpt-4o"               # Model to use (default: gpt-4o)
   openai_temperature = "0.3"            # Temperature setting (default: 0.3)
   ```

You can also customize the model and temperature settings through these methods. The application prioritizes environment variables over config file settings.

### Output

The summarization feature will:
1. Process the full transcription using OpenAI's GPT-4o model
2. Generate a concise summary highlighting key points from the conversation
3. Save the summary to a file named `summary_YYYYMMDD_HHMMSS.txt` in the specified output directory

### Summary Content

The summary focuses on extracting:
- Main discussion topics and context
- Important decisions or conclusions
- Key insights from each speaker
- Action items mentioned during the conversation

The summary is optimized for Russian language conversations and preserves important context and nuances.