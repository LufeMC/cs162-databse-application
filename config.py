import os
import pymysql
import urllib
pymysql.install_as_MySQLdb()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    db_user = os.environ.get('DATABASE_USERNAME')
    db_pass = urllib.parse.quote(os.environ.get('DATABASE_PASSWORD'))
    db_host = os.environ.get('DATABASE_HOST')
    db_port = os.environ.get('DATABASE_PORT')
    db_name = os.environ.get('DATABASE_NAME')

    SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
