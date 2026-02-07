from flask import Blueprint, request, jsonify
from pathlib import Path
from pipelines.preprocess import preprocess_audio
from config import DATA_DIR, UPLOADS_DIR, PROCESSED_DIR, GISTS_DIR
from pipelines.stt import transcribe, load_whisper

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/health", methods=["GET"])
def health():
    return {"status": "AutoMoM running"}


@upload_bp.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "no file provided"}), 400

    file = request.files["file"]
    gist_text = request.form.get("gist", "")

    save_dir = UPLOADS_DIR
    save_path = save_dir / file.filename
    file.save(save_path)

    # Preprocess the audio file
    processed_dir = PROCESSED_DIR
    # Create output filename with .wav extension
    base_name = save_path.stem
    processed_path = processed_dir / (base_name + "_processed.wav")
    
    try:
        preprocess_audio(str(save_path), str(processed_path))
        processed_saved_to = str(processed_path)
    except Exception as e:
        return jsonify({"error": f"preprocessing failed: {str(e)}"}), 500
    print(f"Preprocessed audio saved to: {processed_saved_to}")
    # Run speech-to-text on the preprocessed audio using the loaded Whisper model
    try:
        # ensure model is loaded (load_whisper is idempotent)
        load_whisper()
        segments = transcribe(str(processed_path))
        # join segment texts into a single transcript
        transcript = "\n".join([s.get("text", "") for s in segments])
        # Save transcript to data/transcript/<base_name>.txt
        transcripts_dir = DATA_DIR / "transcript"
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        transcript_file = transcripts_dir / (base_name + ".txt")
        transcript_file.write_text(transcript, encoding="utf-8")
        transcript_saved_to = str(transcript_file)
    except Exception as e:
        print(f"Transcription failed: {str(e)}")
        return jsonify({"error": f"transcription failed: {str(e)}"}), 500
    print(f"Transcript saved to: {transcript_saved_to}")
    gist_saved_to = None
    if gist_text:
        gist_dir = GISTS_DIR
        gist_file = gist_dir / (file.filename + ".gist.txt")
        gist_file.write_text(gist_text, encoding="utf-8")
        gist_saved_to = str(gist_file)

    return jsonify({
        "saved_to": str(save_path),
        "processed_to": processed_saved_to,
        "gist_saved_to": gist_saved_to
    })
