from app import Base, engine, info_logger
from models.office import Office
from models.user import User
from models.rate import Rate
from models.commission import Commission
from models.listing import Listing
from models.order import Order


def createModels():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    info_logger.info("Tables created on DB")
