from pathlib import Path
import subprocess
from config import ffmpeg_path

def preprocess_audio(input_path, output_path):
    command = [
        str(ffmpeg_path),
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        "-vn",
        "-af", "loudnorm",
        output_path
    ]
    subprocess.run(command, check=True, quiet=True)
