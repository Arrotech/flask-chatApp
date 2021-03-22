import os
import eventlet  # noqa
from os import path
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify
from app.extensions import db, bootstrap, login_manager, socketio
from instance.config import app_config


def bad_request(e):
    """Capture bad request error."""
    return make_response(jsonify({
        "status": "400",
        "message": "bad request"
    }), 400)


def page_not_found(e):
    """Capture not found error."""
    return make_response(jsonify({
        "status": "404",
        "message": "resource not found"
    }), 404)


def method_not_allowed(e):
    """Capture method not allowed error."""
    return make_response(jsonify({
        "status": "405",
        "message": "method not allowed"
    }), 405)


def unprocessabe_entity(e):
    """Capture unprocessable entity."""
    return make_response(jsonify({
        "status": "422",
        "message": "unprocessable entity"
    }), 500)


def internal_server_error(e):
    """Capture internal server error."""
    return make_response(jsonify({
        "status": "500",
        "message": "internal server error"
    }), 500)


def create_app(config_name='production'):

    app = Flask(__name__, instance_relative_config=True,
                template_folder='../../../templates',
                static_folder='../../../static')

    if config_name is not None:
        app.config.from_object(app_config[config_name])
    else:
        app.config.from_object(app_config[os.environ.get("FLASK_ENV")])

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'chat_v1.login'
    socketio.init_app(app)

    from app.api.v1 import chat_v1

    app.register_blueprint(chat_v1, url_prefix='/api/v1/')
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(422, unprocessabe_entity)
    app.register_error_handler(500, internal_server_error)

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))

    return socketio, app
