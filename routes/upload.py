from flask import Blueprint, request, jsonify
from pathlib import Path
from pipelines.preprocess import preprocess_audio

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

    save_dir = Path("data/uploads")
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / file.filename
    file.save(save_path)

    # Preprocess the audio file
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output filename with .wav extension
    base_name = save_path.stem
    processed_path = processed_dir / (base_name + "_processed.wav")
    
    try:
        preprocess_audio(str(save_path), str(processed_path))
        processed_saved_to = str(processed_path)
    except Exception as e:
        return jsonify({"error": f"preprocessing failed: {str(e)}"}), 500

    gist_saved_to = None
    if gist_text:
        gist_dir = Path("data/gists")
        gist_dir.mkdir(parents=True, exist_ok=True)
        gist_file = gist_dir / (file.filename + ".gist.txt")
        gist_file.write_text(gist_text, encoding="utf-8")
        gist_saved_to = str(gist_file)

    return jsonify({
        "saved_to": str(save_path),
        "processed_to": processed_saved_to,
        "gist_saved_to": gist_saved_to
    })
