from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from config import Config

# Initializing db on SQLAlchemy
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
engine.connect()

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


def setFormatter(fileName):
    """Creates a file handler with a formatter for logging

    Args:
    fileName (str): name of the log file to write

    Returns:
    logging.FileHandler: a file handler with a formatter for logging
    """
    # Setting up logging handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler = logging.FileHandler(fileName)
    file_handler.setFormatter(formatter)

    return file_handler


# Setting up logger
info_logger = logging.getLogger(f"kanban_board_info")
info_logger.setLevel(logging.INFO)

# Setting up logger
error_logger = logging.getLogger(f"kanban_board_error")
error_logger.setLevel(logging.ERROR)
