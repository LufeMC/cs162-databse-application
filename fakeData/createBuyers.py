from faker import Faker
from werkzeug.security import generate_password_hash
from models.user import User
from extensions import session, info_logger, error_logger


def createBuyers(numBuyers):
    """
    Create a given number of fake buyers with random names, emails, passwords.
    The created buyers will be added to the session and committed to the database.

    Args:
        numBuyers (int): Number of agents to create.

    Returns:
        None
    """

    try:
        for i in range(numBuyers):
            fake = Faker()
            user = User(
                **{
                    "name": fake.name(),
                    "email": fake.email(),
                    "password": generate_password_hash(f"buyer_password_{i}"),
                }
            )

            session.add(user)

        session.commit()
        info_logger.info("Buyers data created")
    except Exception as error:
        error_logger.error(f'"{error}" -> Error on creating buyers data')
