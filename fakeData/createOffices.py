from faker import Faker
from models.office import Office
from extensions import session, info_logger, error_logger


def createOffices(numOffices):
    """
    Create a given number of fake offices with random names.
    The created offices will be added to the session and committed to the database.

    Args:
        numOffices (int): Number of offices to create.

    Returns:
        None
    """
    try:
        for _ in range(numOffices):
            fake = Faker()
            office = Office(
                **{
                    "name": fake.company(),
                }
            )

            session.add(office)

        session.commit()
        info_logger.info("Offices data created")
    except Exception as error:
        error_logger.error(f'"{error}" -> Error on creating offices data')
