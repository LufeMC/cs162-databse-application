from dotenv import load_dotenv
from os import environ as env
import os
import pymysql
import urllib

# Set the default database driver to MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration settings for the Flask app.

    Attributes:
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - SQLALCHEMY_TRACK_MODIFICATIONS: whether to track modifications to the database
    - SECRET_KEY: the secret key for the app (used for decoding)
    - LOG_FILE_NAME: Log file name
    """

    # Set the connection URI for the database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Enable tracking modifications to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Set the secret key for the app
    SECRET_KEY = env['SECRET_KEY']
    LOG_FILE_NAME = 'log.txt'
