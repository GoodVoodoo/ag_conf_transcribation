import os
from pathlib import Path
from typing import List
import subprocess
import ffmpeg
from pydub import AudioSegment
from tqdm import tqdm

class AudioProcessor:
    def __init__(self, input_file: str, output_dir: str = "output"):
        self.input_file = input_file
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
    def extract_audio(self) -> str:
        """Extract audio from video file if input is mp4."""
        print(f"Processing file: {self.input_file}")
        
        if self.input_file.endswith('.mp4'):
            print("Extracting audio from video...")
            output_path = os.path.join(self.output_dir, "extracted_audio.wav")
            
            try:
                stream = ffmpeg.input(self.input_file)
                stream = ffmpeg.output(stream, output_path, acodec='pcm_s16le', ac=1, ar='16k')
                ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
                return output_path
            except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e
        return self.input_file

    def convert_to_wav(self, audio_path: str) -> str:
        """Convert audio to WAV format if needed."""
        if not audio_path.endswith('.wav'):
            print("Converting to WAV format...")
            audio = AudioSegment.from_file(audio_path)
            wav_path = os.path.join(self.output_dir, "converted_audio.wav")
            audio.export(wav_path, format="wav")
            return wav_path
        return audio_path

    def split_audio(self, audio_path: str, max_size_mb: int = 25) -> List[str]:
        """Split audio into chunks if larger than max_size_mb."""
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Convert to MB
        
        if file_size <= max_size_mb:
            return [audio_path]

        print(f"File size ({file_size:.2f}MB) exceeds {max_size_mb}MB. Splitting into chunks...")
        audio = AudioSegment.from_wav(audio_path)
        
        # Calculate duration for each chunk (approximate)
        total_duration = len(audio)
        chunk_duration = int((max_size_mb / file_size) * total_duration)
        
        chunks = []
        for i, start in enumerate(range(0, total_duration, chunk_duration)):
            end = min(start + chunk_duration, total_duration)
            chunk = audio[start:end]
            chunk_path = os.path.join(self.output_dir, f"chunk_{i+1}.wav")
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)
            
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
    
    # Step 1 & 2: Extract audio from video
    audio_path = processor.extract_audio()
    
    # Step 3: Convert to WAV
    wav_path = processor.convert_to_wav(audio_path)
    
    # Step 4: Split if necessary
    audio_chunks = processor.split_audio(wav_path)
    
    # Step 5 & 6: Transcribe and save results
    processor.transcribe_audio(audio_chunks)

if __name__ == "__main__":
    main() 