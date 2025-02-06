import click
from audio_transcriber.audio_processor import AudioProcessor

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output-dir', default='output', help='Directory to save the transcription results')
def main(input_file: str, output_dir: str):
    """Process WAV file and generate transcription."""
    if not input_file.endswith('.wav'):
        raise click.BadParameter('Input file must be a WAV file')
    
    processor = AudioProcessor(input_file, output_dir)
    
    # Split if necessary and transcribe
    audio_chunks = processor.split_audio(input_file)
    processor.transcribe_audio(audio_chunks)

if __name__ == "__main__":
    main() 