"""Opearting system module."""
import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """App configuration variables."""

    DEBUG = False
    TESTING = False

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # app secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(Config):
    """Production configurations."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Allow debug to restart after changes."""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing the application."""

    DEBUG = True
    TESTING = True

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL')
    LIVESERVER_PORT = 8943


class StagingConfig(Config):
    """Configurations for Staging."""

    DEVELOPMENT = True
    DEBUG = True


class ReleaseConfig(Config):
    """Releasing app configurations."""


app_config = dict(
    testing=TestingConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
    staging=StagingConfig,
    release=ReleaseConfig
)
