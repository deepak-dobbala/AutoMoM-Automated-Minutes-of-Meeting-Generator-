from flask import Blueprint, request, jsonify
from pathlib import Path

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/health", methods=["GET"])
def health():
    return {"status": "AutoMoM running"}

@upload_bp.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    save_dir = Path("data/uploads")
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / file.filename
    file.save(save_path)
    return jsonify({"saved_to": str(save_path)})
