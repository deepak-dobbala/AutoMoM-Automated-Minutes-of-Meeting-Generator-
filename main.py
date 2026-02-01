from flask import Flask, render_template
from routes.upload import upload_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(upload_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
