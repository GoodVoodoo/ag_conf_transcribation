import argparse
from .audio_processor import AudioProcessor

def main():
    parser = argparse.ArgumentParser(description='Audio transcription utility')
    parser.add_argument('--input', '-i', 
                       help='Input audio/video file path',
                       required=True)
    parser.add_argument('--output-dir', '-o',
                       help='Output directory',
                       default='output')
    args = parser.parse_args()
    
    # Initialize processor
    processor = AudioProcessor(args.input, args.output_dir)
    
    # Process the file
    print(f"Processing {args.input}...")
    
    # Extract audio
    audio_path = processor.extract_audio()
    
    # Convert to WAV if needed
    wav_path = processor.convert_to_wav(audio_path)
    
    # Split if necessary
    audio_chunks = processor.split_audio(wav_path)
    
    # Transcribe
    processor.transcribe_audio(audio_chunks)
    
    print("Processing complete!")

__all__ = ['AudioProcessor', 'main'] 