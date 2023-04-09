from faker import Faker
from werkzeug.security import generate_password_hash
from models.user import User
from extensions import session, info_logger, error_logger
import random


def createAgents(numAgents, numOffices):
    """
    Create a given number of fake agents with random names, emails, passwords, and office IDs.
    The created agents will be added to the session and committed to the database.

    Args:
        numAgents (int): Number of agents to create.
        numOffices (int): Number of offices to randomly assign to the created agents.

    Returns:
        None
    """

    try:
        for i in range(numAgents):
            fake = Faker()
            user = User(
                **{
                    "name": fake.name(),
                    "email": fake.email(),
                    "password": generate_password_hash(f"buyer_password_{i}"),
                    "type": "agent",
                    "office_id": random.choice([i + 1 for i in range(numOffices)]),
                }
            )

            session.add(user)

        session.commit()
        info_logger.info("Agents data created")
    except Exception as error:
        error_logger.error(f'"{error}" -> Error on creating agents data')
