from config import Config
from extensions import setFormatter, info_logger, error_logger
import logging
from models.createModels import createModels
from fakeData.createFakeData import createFakeData


def create_database(ConfigClass=Config):
    # Initializing extensions
    fileFormatter = setFormatter(ConfigClass.LOG_FILE_NAME)
    info_logger.addHandler(fileFormatter)
    error_logger.addHandler(fileFormatter)
    info_logger.addHandler(logging.StreamHandler())
    error_logger.addHandler(logging.StreamHandler())
    info_logger.info("File log for Kanban Board opened")

    info_logger.info("DB Initiated")

    createModels(ConfigClass)

    if ConfigClass.TESTING == False:
        # Creating fake data
        info_logger.info("Creating fake data")
        numBuyers = 1000
        numOffices = int(numBuyers / 50)
        numAgents = int(numBuyers / 25)
        numListings = int(numBuyers / 2)
        numOrders = int(numListings / 2)

        createFakeData(numBuyers, numOffices, numAgents, numListings, numOrders)


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    create_database()
