# Audio Processing and Transcription Utility

This utility processes audio/video files and transcribes them using the ASR service. It can:
1. Extract audio from MP4 files
2. Convert audio to WAV format
3. Split large audio files into chunks
4. Transcribe audio with punctuation
5. Save transcriptions to text files

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install the package and its dependencies:
```bash
pip install .
```

## Usage

Place your audio/video file in the project directory and run:

```bash
python audio_processor.py
```

By default, it will process the file "jnr-cduk-irv (2023-03-06 17_15 GMT+3).mp4".

The script will:
1. Create an 'output' directory
2. Extract audio if the input is a video file
3. Convert the audio to WAV format if needed
4. Split the audio into chunks if it's larger than 25MB
5. Transcribe each chunk with punctuation
6. Save the transcriptions in the output directory

## Output

The script creates an 'output' directory containing:
- Extracted audio (if input was video)
- Converted WAV file (if input wasn't WAV)
- Audio chunks (if splitting was necessary)
- Transcription text files for each chunk 