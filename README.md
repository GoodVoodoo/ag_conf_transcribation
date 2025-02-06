# AG ASR (Audiogram Speech Recognition)

A command-line utility for speech recognition that supports various audio formats and provides advanced features like punctuation and speaker labeling.

## Features

- Support for multiple audio formats (MP4, MP3, WAV)
- Automatic audio extraction from video files
- Audio file splitting for large files (>25MB)
- Speech recognition with punctuation
- Speaker labeling
- Gender and age detection
- Anti-spoofing protection

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ag-asr
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Create a configuration file:
```bash
asr create-config
```

## Usage

### Basic File Recognition
```bash
asr recognize file --audio-file input.wav --model general
```

### Recognition with Punctuation
```bash
asr recognize file --audio-file input.wav --model general --enable-punctuator
```

### Recognition with Speaker Labeling
```bash
asr recognize file --audio-file input.wav --model general --enable-speaker-labeling
```

### Get Available Models
```bash
asr models recognize
```

## Configuration

The application uses a configuration file (`config.ini`) for API credentials and settings. You can create it using:
```bash
asr create-config
```

Required configuration:
- `api_address`: gRPC API host and port
- `client_id`: Keycloak client ID
- `client_secret`: Keycloak client secret
- `iam_account`: IAM account name
- `iam_workspace`: IAM workspace name

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
isort .
```

4. Run type checking:
```bash
mypy .
```

## License

This project is proprietary and confidential. All rights reserved. 