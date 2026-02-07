import os
import whisper
from config import ffmpeg_path

_model = None

def _ensure_ffmpeg_on_path():
    # Add the ffmpeg binary directory to PATH so whisper can invoke it on Windows
    ffmpeg_dir = str(ffmpeg_path.parent)
    current_path = os.environ.get("PATH", "")
    if ffmpeg_dir and ffmpeg_dir not in current_path:
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + current_path


def load_whisper(model_name="base"):
    global _model
    if _model is None:
        _ensure_ffmpeg_on_path()
        _model = whisper.load_model(model_name)
    return _model


def transcribe(audio_path: str):
    # Verify file exists to provide clearer errors
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"audio file not found: {audio_path}")

    model = load_whisper()
    # returns dict with "segments": list of {start,end,text}
    result = model.transcribe(audio_path, word_timestamps=False)
    # normalize to our segment format
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })
    return segments
