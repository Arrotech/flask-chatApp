import os
from app import create_app

socketio, app = create_app(os.environ.get("FLASK_ENV"))

if __name__ == "__main__":
    socketio.run(app)
