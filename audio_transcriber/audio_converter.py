import os
from pathlib import Path
import subprocess
import click
import shlex

class AudioConverter:
    def __init__(self, input_file: str, output_dir: str = "output"):
        """Initialize the audio converter.
        
        Args:
            input_file: Path to the input file (mp4, mp3, or wav)
            output_dir: Directory to save the output files (default: "output")
        """
        self.input_file = str(Path(input_file).resolve())  # Get absolute path
        self.output_dir = str(Path(output_dir).resolve())  # Get absolute path
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def _convert_with_ffmpeg(self, input_path: str, output_path: str) -> None:
        """Convert audio using ffmpeg with specified parameters."""
        try:
            # Use absolute paths to avoid issues with spaces
            input_path = str(Path(input_path).resolve())
            output_path = str(Path(output_path).resolve())
            
            # Create the ffmpeg command
            ffmpeg_cmd = f'ffmpeg -i "{input_path}" -acodec pcm_s16le -ac 1 -ar 16000 -y "{output_path}"'
            print(f"Running command: {ffmpeg_cmd}")
            
            # Run the command through shell to handle paths with spaces properly
            result = subprocess.run(
                ffmpeg_cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                print("Error output:", result.stderr)
                raise Exception(f"ffmpeg failed with return code {result.returncode}")
                
            print(f"Converted to: {output_path}")
        except Exception as e:
            print(f"Error during conversion: {str(e)}")
            raise

    def process(self) -> str:
        """Process the input file: extract audio and convert to WAV.
        
        Returns:
            Path to the final WAV file
        """
        output_path = os.path.join(self.output_dir, "output.wav")
        
        print(f"Processing file: {self.input_file}")
        self._convert_with_ffmpeg(self.input_file, output_path)
        
        return output_path

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output-dir', default='output', help='Directory to save the output files')
def main(input_file: str, output_dir: str):
    """Convert video/audio files to WAV format.
    
    This utility can:
    1. Extract audio from MP4 files
    2. Convert MP3 files to WAV
    3. Process existing WAV files (will copy to output directory)
    
    All output WAV files will be:
    - Mono channel
    - 16kHz sample rate
    - 16-bit PCM encoding
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