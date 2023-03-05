from dotenv import load_dotenv
from os import environ as env
import os
import pymysql
import urllib
pymysql.install_as_MySQLdb()

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    db_user = env['DATABASE_USERNAME']
    db_pass = urllib.parse.quote(
        env['DATABASE_PASSWORD'] if env['DATABASE_PASSWORD'] else '')
    db_host = env['DATABASE_HOST']
    db_port = env['DATABASE_PORT']
    db_name = env['DATABASE_NAME']

    SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = env['SECRET_KEY']
