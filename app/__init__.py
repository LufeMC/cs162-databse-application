from flask import Flask

from config import Config
from app.extensions import db
from app.models.task import Task
from app.models.user import User


def create_app(config_class=Config):
    """
    This function creates a Flask application instance and returns it.

    Parameters:
        config_class (Config): A configuration class to configure the Flask app
        instance. Defaults to `Config`, which comes from the configuration file
        that reads the environment variables.

    Returns:
        Flask: The Flask application instance.

    """
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config_class)

    # Initializing db extension and creating the tables
    db.init_app(flaskApp)
    with flaskApp.app_context():
        db.create_all()

    # Registering blueprints
    from app.home import bp as home_bp
    flaskApp.register_blueprint(home_bp, url_prefix='/home/')

    from app.auth import bp as auth_bp
    flaskApp.register_blueprint(auth_bp, url_prefix='/auth/')

    return flaskApp
