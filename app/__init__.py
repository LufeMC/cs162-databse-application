from flask import Flask

from config import Config
from app.extensions import db
from app.models.task import Task
from app.models.user import User


def create_app(config_class=Config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(flaskApp)
    with flaskApp.app_context():
        db.create_all()

    # Register blueprints here
    from app.home import bp as home_bp
    flaskApp.register_blueprint(home_bp, url_prefix='/home/')

    from app.auth import bp as auth_bp
    flaskApp.register_blueprint(auth_bp, url_prefix='/auth/')

    return flaskApp
