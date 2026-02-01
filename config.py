from pathlib import Path

# Path to ffmpeg executable (used by pipelines.preprocess)
ffmpeg_path = Path("tools/ffmpeg-8.0.1-essentials_build/bin/ffmpeg.exe")

# Centralized data directories
DATA_DIR = Path("data")
UPLOADS_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
GISTS_DIR = DATA_DIR / "gists"

# Ensure folders exist when imported
for p in (DATA_DIR, UPLOADS_DIR, PROCESSED_DIR, GISTS_DIR):
	p.mkdir(parents=True, exist_ok=True)