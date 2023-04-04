from flask import Flask, redirect

from config import Config
from app.extensions import db, setFormatter, info_logger, error_logger
from app.models.office import Office
from app.models.user import User
from app.models.rate import Rate
from app.models.commission import Commission
from app.models.listing import Listing
from app.models.order import Order
from app.fakerData.createBuyers import createBuyers
from app.fakerData.createOffices import createOffices
from app.fakerData.createAgents import createAgents
from app.fakerData.createListings import createListings
from app.fakerData.createOrders import createOrders

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
        db.drop_all()
        db.create_all()
        info_logger.info('Tables created on DB')

    # Creating fake data
    numBuyers = 1000
    numOffices = int(numBuyers/200)
    numAgents = int(numBuyers/40)
    numListings = int(numBuyers/2)
    numOrders = int(numListings/2)

    createBuyers(numBuyers, flaskApp)
    createOffices(numOffices, flaskApp)
    createAgents(numAgents, numOffices, flaskApp)
    createListings(numListings, flaskApp)
    createOrders(numOrders, numListings, numAgents, numBuyers, flaskApp)

    # Registering blueprints
    @flaskApp.errorhandler(404)
    def notFound(e):
        return redirect('/auth/login')

    from app.home import bp as home_bp
    flaskApp.register_blueprint(home_bp, url_prefix='/home/')

    from app.auth import bp as auth_bp
    flaskApp.register_blueprint(auth_bp, url_prefix='/auth/')

    return flaskApp
