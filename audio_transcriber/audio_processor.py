import os
from pathlib import Path
from typing import List
import subprocess
import ffmpeg
from tqdm import tqdm

class AudioProcessor:
    def __init__(self, input_file: str, output_dir: str = "output"):
        self.input_file = input_file
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
    def _convert_with_ffmpeg(self, input_path: str, output_path: str) -> None:
        """Convert audio using ffmpeg with specified parameters."""
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(
                stream, 
                output_path,
                acodec='pcm_s16le',  # 16-bit PCM
                ac=1,                # mono
                ar='16k',            # 16kHz sample rate
                loglevel='info'      # show progress
            )
            ffmpeg.run(stream)
            print(f"Converted to: {output_path}")
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e

    def split_audio(self, audio_path: str, max_size_mb: int = 25) -> List[str]:
        """Split audio into chunks if larger than max_size_mb."""
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Convert to MB
        
        if file_size <= max_size_mb:
            return [audio_path]

        print(f"File size ({file_size:.2f}MB) exceeds {max_size_mb}MB. Splitting into chunks...")
        
        # Get audio duration using ffprobe
        probe = ffmpeg.probe(audio_path)
        duration = float(probe['streams'][0]['duration'])
        
        # Calculate number of chunks needed
        num_chunks = int((file_size / max_size_mb) + 0.5)  # Round up
        chunk_duration = duration / num_chunks
        
        chunks = []
        for i in range(num_chunks):
            start_time = i * chunk_duration
            chunk_path = os.path.join(self.output_dir, f"chunk_{i+1}.wav")
            
            try:
                stream = ffmpeg.input(audio_path, ss=start_time, t=chunk_duration)
                stream = ffmpeg.output(
                    stream,
                    chunk_path,
                    acodec='pcm_s16le',
                    ac=1,
                    ar='16k'
                )
                ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
                chunks.append(chunk_path)
            except ffmpeg.Error as e:
                print(f"Error splitting chunk {i+1}: {str(e)}")
                raise
        
        print(f"Split into {len(chunks)} chunks")
        return chunks

    def transcribe_audio(self, audio_paths: List[str]) -> None:
        """Transcribe audio files using clients.main."""
        print("Transcribing audio...")
        
        for i, audio_path in enumerate(audio_paths, 1):
            output_file = os.path.join(self.output_dir, f"transcription_{i}.txt")
            print(f"Processing chunk {i}/{len(audio_paths)}")
            
            cmd = ["python", "-m", "clients.main", "recognize", 
                  "--enable-punctuator", audio_path]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result.stdout)
                    print(f"Transcription saved to {output_file}")
                else:
                    print(f"Error during transcription: {result.stderr}")
            except Exception as e:
                print(f"Error during transcription: {str(e)}")

def main():
    # Example usage
    input_file = "jnr-cduk-irv (2023-03-06 17_15 GMT+3).mp4"
    processor = AudioProcessor(input_file)
    
    # Convert to WAV if needed
    if not input_file.endswith('.wav'):
        output_path = os.path.join(processor.output_dir, "input.wav")
        processor._convert_with_ffmpeg(input_file, output_path)
        input_file = output_path
    
    # Split if necessary
    audio_chunks = processor.split_audio(input_file)
    
    # Transcribe and save results
    processor.transcribe_audio(audio_chunks)

if __name__ == "__main__":
    main() 