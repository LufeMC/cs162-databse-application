import extensions
import tests.test_extensions as test_extensions
from models.office import Office
from models.user import User
from models.rate import Rate
from models.commission import Commission
from models.listing import Listing
from models.order import Order


def createModels(ConfigClass):
    engine = test_extensions.engine if ConfigClass.TESTING else extensions.engine
    Base = extensions.Base
    info_logger = extensions.info_logger

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    info_logger.info("Tables created on DB")
