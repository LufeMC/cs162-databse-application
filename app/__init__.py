from flask import Flask, redirect

from config import Config
from app.extensions import db, setFormatter, info_logger, error_logger
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

    # Initializing extensions
    fileFormatter = setFormatter(config_class.LOG_FILE_NAME)
    info_logger.addHandler(fileFormatter)
    error_logger.addHandler(fileFormatter)
    info_logger.info('File log for Kanban Board opened')

    db.init_app(flaskApp)
    info_logger.info('DB Initiated')
    with flaskApp.app_context():
        db.create_all()
        info_logger.info('Tables created on DB')

    # Registering blueprints
    @flaskApp.errorhandler(404)
    def notFound(e):
        return redirect('/auth/login')

    from app.home import bp as home_bp
    flaskApp.register_blueprint(home_bp, url_prefix='/home/')

    from app.auth import bp as auth_bp
    flaskApp.register_blueprint(auth_bp, url_prefix='/auth/')

    return flaskApp
