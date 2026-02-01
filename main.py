from flask import Flask
from routes.upload import upload_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(upload_bp)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
