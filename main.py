import argparse
import os
from pathlib import Path
from audio_transcriber.audio_processor import AudioProcessor
from audio_transcriber.summarization import TranscriptionSummarizer

def main():
    """Process audio/video file and generate transcription.
    
    Supports mp4, mp3, and wav files.
    """
    parser = argparse.ArgumentParser(description='Process audio/video file and generate transcription.')
    parser.add_argument('input_file', type=str, help='Path to the input audio/video file')
    parser.add_argument('--output-dir', default='output', help='Directory to save the transcription results')
    parser.add_argument('--add-summarization', action='store_true', help='Generate a summary of the transcription using GPT-4o')
    parser.add_argument('--config', default='config.ini', help='Path to the configuration file')
    
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
    
    # If summarization is requested
    if args.add_summarization:
        try:
            # Find the merged transcription file
            transcription_files = [f for f in os.listdir(args.output_dir) if f.startswith("merged_transcription_")]
            if not transcription_files:
                print("No merged transcription found. Cannot generate summary.")
                return
                
            # Sort by modification time to get the most recent one
            latest_file = sorted(
                transcription_files,
                key=lambda x: os.path.getmtime(os.path.join(args.output_dir, x)),
                reverse=True
            )[0]
            
            transcription_path = os.path.join(args.output_dir, latest_file)
            
            # Generate summary
            print("Generating summary using OpenAI...")
            summarizer = TranscriptionSummarizer(transcription_path, args.output_dir, args.config)
            summarizer.summarize()
            
        except Exception as e:
            print(f"Error during summarization: {str(e)}")

if __name__ == "__main__":
    main() 