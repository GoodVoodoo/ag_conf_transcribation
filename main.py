import argparse
import os
from pathlib import Path
from audio_transcriber.audio_processor import AudioProcessor

def main():
    """Process audio/video file and generate transcription.
    
    Supports mp4, mp3, and wav files.
    """
    parser = argparse.ArgumentParser(description='Process audio/video file and generate transcription.')
    parser.add_argument('input_file', type=str, help='Path to the input audio/video file')
    parser.add_argument('--output-dir', default='output', help='Directory to save the transcription results')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input_file):
        parser.error(f"Input file does not exist: {args.input_file}")
    
    processor = AudioProcessor(args.input_file, args.output_dir)
    
    # Convert to WAV if needed
    if not args.input_file.lower().endswith('.wav'):
        wav_path = str(Path(args.output_dir) / "input.wav")
        processor._convert_to_wav(args.input_file, wav_path)
        args.input_file = wav_path
    
    # Split if necessary and transcribe
    audio_chunks = processor.split_audio(args.input_file)
    processor.transcribe_audio(audio_chunks)

if __name__ == "__main__":
    main() 