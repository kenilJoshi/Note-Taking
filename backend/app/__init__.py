from flask import Flask 

from .events import socketio
from .routes import main
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    CORS(app, origins=["*"])
    app.register_blueprint(main)

    socketio.init_app(app, cors_allowed_origins="*")

    return app