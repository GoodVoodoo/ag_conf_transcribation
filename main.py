import click
from pathlib import Path
from audio_transcriber.audio_processor import AudioProcessor

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output-dir', default='output', help='Directory to save the transcription results')
def main(input_file: str, output_dir: str):
    """Process audio/video file and generate transcription.
    
    Supports mp4, mp3, and wav files.
    """
    processor = AudioProcessor(input_file, output_dir)
    
    # Convert to WAV if needed
    if not input_file.lower().endswith('.wav'):
        wav_path = str(Path(output_dir) / "input.wav")
        processor._convert_to_wav(input_file, wav_path)
        input_file = wav_path
    
    # Split if necessary and transcribe
    audio_chunks = processor.split_audio(input_file)
    processor.transcribe_audio(audio_chunks)

if __name__ == "__main__":
    main() 