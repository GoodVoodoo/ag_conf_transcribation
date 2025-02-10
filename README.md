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

**Security Notes:**
- Never commit `config.ini` to git (it's already in `.gitignore`)
- Use a secure password manager for storing and sharing credentials
- The pre-commit hooks will help prevent accidentally committing sensitive data

3. Pre-commit Setup (For Developers):
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

You can process any audio/video file by providing its path as a parameter:

1. Using the Python module:
   ```bash
   python -m audio_transcriber.audio_processor --input-file "path/to/your/file.mp4"
   ```

   Or with the installed script:
   ```bash
   audio-transcriber --input-file "path/to/your/file.mp4"
   ```

2. Supported input formats:
   - Video files (mp4, avi, mkv, etc.)
   - Audio files (mp3, wav, m4a, etc.)

The script will:
- Convert the input file to WAV format if necessary
- Split large files into smaller chunks
- Transcribe each chunk with speaker labeling
- Merge all transcriptions into a single output file

## Output

Transcriptions will be saved in the `output` directory:
- Individual chunk transcriptions in a timestamped folder
- Final merged transcription as `merged_transcription_TIMESTAMP.txt`

## Troubleshooting

1. If you encounter FFmpeg errors:
   ```bash
   brew update && brew upgrade ffmpeg
   ```

2. If you get SSL/certificate errors:
   - Check your internet connection
   - Verify your API credentials in `config.ini`
   - Ensure you have the latest Python SSL certificates:
   ```bash
   /Applications/Python\ 3.9/Install\ Certificates.command
   ```

## Development

For development work:
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   .\venv\Scripts\Activate.ps1  # On Windows
   ```

2. Install the package with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

   This will install:
   - black (code formatter)
   - isort (import sorter)
   - ruff (linter)
   - mypy (type checker)

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Testing

1. Install the package with test dependencies:
   ```bash
   pip install -e ".[test]"
   ```

   This will install:
   - pytest (testing framework)
   - pytest-mock (mocking support)
   - pytest-cov (coverage reporting)

2. Run the tests:
   ```bash
   # Run all tests
   python -m pytest tests/

   # Run with verbose output
   python -m pytest tests/ -v

   # Run with coverage report
   python -m pytest tests/ --cov=audio_transcriber
   ```

3. Manual Testing

   Quick test with sample audio:
   ```bash
   # Download a sample audio file
   curl -O https://www2.cs.uic.edu/~i101/SoundFiles/gettysburg.wav
   
   # Run the transcriber
   python -m audio_transcriber.audio_processor --input-file gettysburg.wav
   ```

   Test with your own files:
   ```bash
   # For video file
   python -m audio_transcriber.audio_processor --input-file "path/to/your/video.mp4"
   
   # For audio file
   python -m audio_transcriber.audio_processor --input-file "path/to/your/audio.mp3"
   ```

4. Test Results
   - Unit test results will show pass/fail status for each test
   - Coverage report will show percentage of code covered by tests
   - For manual testing, check the `output` directory for transcription results

## License

[Add your license information here] 