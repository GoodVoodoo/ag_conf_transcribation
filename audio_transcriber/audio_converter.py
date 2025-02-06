import os
from pathlib import Path
import ffmpeg
from pydub import AudioSegment
import click

class AudioConverter:
    def __init__(self, input_file: str, output_dir: str = "output"):
        """Initialize the audio converter.
        
        Args:
            input_file: Path to the input file (mp4, mp3, or wav)
            output_dir: Directory to save the output files (default: "output")
        """
        self.input_file = input_file
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def extract_audio(self) -> str:
        """Extract audio from video file if input is mp4.
        
        Returns:
            Path to the extracted audio file
        """
        if not self.input_file.endswith('.mp4'):
            return self.input_file
            
        print(f"Extracting audio from video: {self.input_file}")
        output_path = os.path.join(self.output_dir, "extracted_audio.wav")
        
        try:
            stream = ffmpeg.input(self.input_file)
            stream = ffmpeg.output(stream, output_path, acodec='pcm_s16le', ac=1, ar='16k')
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"Audio extracted to: {output_path}")
            return output_path
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e

    def convert_to_wav(self, audio_path: str) -> str:
        """Convert audio to WAV format if needed.
        
        Args:
            audio_path: Path to the input audio file
            
        Returns:
            Path to the WAV file
        """
        if audio_path.endswith('.wav'):
            return audio_path
            
        print(f"Converting {audio_path} to WAV format...")
        audio = AudioSegment.from_file(audio_path)
        wav_path = os.path.join(self.output_dir, "converted_audio.wav")
        audio.export(wav_path, format="wav", parameters=["-ac", "1", "-ar", "16000"])
        print(f"Converted to WAV: {wav_path}")
        return wav_path

    def process(self) -> str:
        """Process the input file: extract audio if needed and convert to WAV.
        
        Returns:
            Path to the final WAV file
        """
        # First extract audio if it's a video file
        audio_path = self.extract_audio()
        
        # Then convert to WAV if it's not already
        wav_path = self.convert_to_wav(audio_path)
        
        return wav_path

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output-dir', default='output', help='Directory to save the output files')
def main(input_file: str, output_dir: str):
    """Convert video/audio files to WAV format.
    
    This utility can:
    1. Extract audio from MP4 files
    2. Convert MP3 files to WAV
    3. Process existing WAV files (will copy to output directory)
    
    All output WAV files will be mono channel with 16kHz sample rate.
    """
    converter = AudioConverter(input_file, output_dir)
    try:
        output_path = converter.process()
        print(f"\nSuccess! Final WAV file: {output_path}")
    except Exception as e:
        print(f"\nError during conversion: {str(e)}")
        raise click.Abort()

if __name__ == "__main__":
    main() 