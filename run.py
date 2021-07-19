import os
from flask import redirect, url_for
from app import create_app
from app.extensions import db

socketio, app = create_app(os.environ.get("FLASK_ENV", "development"))


@app.route("/")
def index():
    return redirect(url_for('chat_v1.home'))


@app.cli.command()
def create_tables_v1():
    """Version 1: Create tables if they do not exists."""
    print("Creating tables...")
    db.create_all()
    print("Version 1 new tables created... OK")


if __name__ == "__main__":
    app.run()
