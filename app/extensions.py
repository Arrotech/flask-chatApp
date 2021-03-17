from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
socketio = SocketIO()
