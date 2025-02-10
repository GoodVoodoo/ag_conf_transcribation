import os
from pathlib import Path
from typing import List
import subprocess
from tqdm import tqdm
from datetime import datetime
import argparse

class AudioProcessor:
    def __init__(self, input_file: str, output_dir: str = "output"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.transcription_dir = os.path.join(output_dir, f"transcription_{self.timestamp}")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.transcription_dir).mkdir(parents=True, exist_ok=True)
        
    def _convert_to_wav(self, input_path: str, output_path: str) -> None:
        """Convert video/audio to WAV format."""
        try:
            cmd = [
                'ffmpeg', '-i', input_path,
                '-acodec', 'pcm_s16le',  # 16-bit PCM
                '-ac', '1',              # mono
                '-ar', '16000',          # 16kHz sample rate
                '-y',                    # overwrite output
                output_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Converted to: {output_path}")
            else:
                print(f"Error during conversion: {result.stderr}")
                raise Exception(result.stderr)
        except Exception as e:
            print(f'Error during conversion: {str(e)}')
            raise e

    def split_audio(self, audio_path: str, max_size_mb: int = 10) -> List[str]:
        """Split audio into chunks if larger than max_size_mb."""
            
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Convert to MB
        
        if file_size <= max_size_mb:
            return [audio_path]

        print(f"File size ({file_size:.2f}MB) exceeds {max_size_mb}MB. Splitting into chunks...")
        
        # Get audio duration using ffprobe
        cmd = ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error getting duration: {result.stderr}")
        duration = float(result.stdout.strip())
        
        # Calculate number of chunks needed
        num_chunks = int((file_size / max_size_mb) + 0.5)  # Round up
        chunk_duration = duration / num_chunks
        
        chunks = []
        for i in range(num_chunks):
            start_time = i * chunk_duration
            end_time = min((i + 1) * chunk_duration, duration)
            
            chunk_path = os.path.join(self.output_dir, f"chunk_{i+1}.wav")
            
            try:
                cmd = [
                    'ffmpeg',
                    '-i', audio_path,
                    '-ss', str(start_time),
                    '-t', str(end_time - start_time),
                    '-acodec', 'pcm_s16le',
                    '-ac', '1',
                    '-ar', '16000',
                    '-y',
                    chunk_path
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    chunks.append(chunk_path)
                else:
                    print(f"Error splitting chunk {i+1}: {result.stderr}")
                    raise Exception(result.stderr)
            except Exception as e:
                print(f"Error splitting chunk {i+1}: {str(e)}")
                raise
        
        print(f"Split into {len(chunks)} chunks")
        return chunks

    def transcribe_audio(self, audio_paths: List[str]) -> None:
        """Transcribe audio files using clients.main."""
        print("Transcribing audio...")
        
        for i, audio_path in enumerate(audio_paths, 1):
            output_file = os.path.join(self.transcription_dir, f"transcription_{i}.txt")
            print(f"Processing chunk {i}/{len(audio_paths)}")
            
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            
            cmd = ["python", "-m", "clients.main", "recognize", "file",
                  "--audio-file", audio_path, "--config", "config.ini",
                  "--enable-punctuator", "--enable-speaker-labeling"]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=env)
                if result.returncode == 0:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result.stdout)
                    print(f"Transcription saved to {output_file}")
                else:
                    print(f"Error during transcription: {result.stderr}")
                    print(f"Command output: {result.stdout}")
            except Exception as e:
                print(f"Error during transcription: {str(e)}")
                print(f"Error type: {type(e)}")
        
        # After all transcriptions are done, merge them
        self.merge_transcriptions()

    def merge_transcriptions(self) -> None:
        """Merge all transcription files into one with proper formatting."""
        print("Merging transcriptions...")
        
        # Get all transcription files sorted by number
        transcription_files = sorted(
            [f for f in os.listdir(self.transcription_dir) if f.startswith("transcription_")],
            key=lambda x: int(x.split("_")[1].split(".")[0])
        )
        
        # Create merged file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merged_file = os.path.join(self.output_dir, f"merged_transcription_{timestamp}.txt")
        
        with open(merged_file, 'w', encoding='utf-8') as outfile:
            for i, fname in enumerate(transcription_files, 1):
                file_path = os.path.join(self.transcription_dir, fname)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    
                    # Extract only the relevant parts (speaker lines)
                    cleaned_lines = []
                    for line in content.split('\n'):
                        # Skip technical lines and empty lines
                        if "Speaker labeling enabled:" in line:
                            continue
                        if "Speaker" in line and ":" in line:
                            cleaned_lines.append(line.strip())
                    
                    if cleaned_lines:
                        outfile.write(f"Part {i}\n")
                        outfile.write('\n'.join(cleaned_lines))
                        outfile.write('\n\n')
        
        print(f"Merged transcription saved to: {merged_file}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process and transcribe audio/video files')
    parser.add_argument('--input-file', type=str, required=True,
                       help='Path to the input audio/video file')
    args = parser.parse_args()

    processor = AudioProcessor(args.input_file)
    
    # Convert to WAV if needed
    if not args.input_file.endswith('.wav'):
        output_path = os.path.join(processor.output_dir, "input.wav")
        processor._convert_to_wav(args.input_file, output_path)
        input_file = output_path
    else:
        input_file = args.input_file
    
    # Split if necessary
    audio_chunks = processor.split_audio(input_file)
    
    # Transcribe and save results
    processor.transcribe_audio(audio_chunks)

if __name__ == "__main__":
    main() 