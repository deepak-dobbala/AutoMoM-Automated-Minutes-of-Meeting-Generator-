from pathlib import Path
import subprocess
from config import ffmpeg_path

def preprocess_audio(input_path, output_path):
    command = [
        str(ffmpeg_path),
        "-hide_banner",     # Hides the version/build info you saw earlier
        "-loglevel", "error", # Only shows errors, no progress bars
        "-y",               # Overwrite output file if it exists
        "-i", input_path,
        "-ac", "1",         # Convert to Mono
        "-ar", "16000",     # 16kHz for Whisper
        "-vn",              # Disable video
        "-af", "loudnorm",  # Normalize volume for better AI accuracy
        output_path
    ]
    
    # Run the command
    subprocess.run(command, check=True)