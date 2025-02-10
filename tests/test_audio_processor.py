import os
import pytest
from pathlib import Path
from audio_transcriber.audio_processor import AudioProcessor

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory for tests."""
    return str(tmp_path / "output")

@pytest.fixture
def audio_processor(temp_output_dir):
    """Create an AudioProcessor instance with a test file."""
    test_file = "test_input.wav"
    return AudioProcessor(test_file, output_dir=temp_output_dir)

def test_init_creates_directories(audio_processor, temp_output_dir):
    """Test that initialization creates necessary directories."""
    assert os.path.exists(temp_output_dir)
    assert os.path.exists(audio_processor.transcription_dir)

def test_convert_to_wav(audio_processor, mocker):
    """Test WAV conversion with mocked subprocess."""
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.returncode = 0
    
    input_path = "test.mp4"
    output_path = "test.wav"
    
    audio_processor._convert_to_wav(input_path, output_path)
    
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args[0] == 'ffmpeg'
    assert args[2] == input_path
    assert args[-1] == output_path

def test_convert_to_wav_error(audio_processor, mocker):
    """Test WAV conversion error handling."""
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "FFmpeg error"
    
    with pytest.raises(Exception) as exc_info:
        audio_processor._convert_to_wav("test.mp4", "test.wav")
    
    assert "FFmpeg error" in str(exc_info.value)

def test_split_audio_small_file(audio_processor, mocker):
    """Test that small files are not split."""
    mocker.patch('os.path.getsize', return_value=5 * 1024 * 1024)  # 5MB
    input_file = "small_file.wav"
    
    result = audio_processor.split_audio(input_file)
    
    assert result == [input_file]

def test_merge_transcriptions(audio_processor, temp_output_dir):
    """Test merging transcription files."""
    # Create test transcription files
    for i in range(1, 4):
        file_path = os.path.join(audio_processor.transcription_dir, f"transcription_{i}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Speaker 1: Test content {i}\n")
    
    audio_processor.merge_transcriptions()
    
    # Check that merged file exists and contains content
    merged_files = [f for f in os.listdir(temp_output_dir) 
                   if f.startswith("merged_transcription_")]
    assert len(merged_files) == 1
    
    merged_path = os.path.join(temp_output_dir, merged_files[0])
    with open(merged_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Speaker 1: Test content 1" in content
        assert "Speaker 1: Test content 2" in content
        assert "Speaker 1: Test content 3" in content 