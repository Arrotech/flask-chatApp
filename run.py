import os
from flask import redirect, url_for
from app import create_app

socketio, app = create_app(os.environ.get("FLASK_ENV"))


@app.route("/")
def index():
    return redirect(url_for('chat_v1.home'))


if __name__ == "__main__":
    socketio.run(app)
