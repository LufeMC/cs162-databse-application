from models.order import Order
from models.listing import Listing
from extensions import session, info_logger, error_logger
import random
import datetime


def createOrders(numOrders, numListings, numAgents, numBuyers):
    """
    Creates the specified number of orders using randomly selected listings, agents, and buyers.

    Args:
        numOrders: An integer representing the number of orders to create.
        numListings: An integer representing the number of listings to choose from.
        numAgents: An integer representing the number of agents to choose from.
        numBuyers: An integer representing the number of buyers to choose from.

    Returns:
        None
    """
    try:
        idsChosen = set()
        for _ in range(int(numOrders)):
            # Choose a random listing id that hasn't already been chosen
            listing_id = random.choice([i + 1 for i in range(numListings)])

            while listing_id in idsChosen:
                listing_id = random.choice([i + 1 for i in range(numListings)])

            idsChosen.add(listing_id)

            # Get the listing object and update its sold status and date sold
            listing = session.query(Listing).filter_by(id=listing_id).first()
            date_sold = listing.date_created + datetime.timedelta(
                days=random.randint(1, 50)
            )
            if date_sold > datetime.datetime.now():
                date_sold = datetime.datetime.now()

            listing.date_sold = date_sold
            listing.sold = True

            # Create and add the new order to the database
            order = Order(
                **{
                    "listing_id": listing_id,
                    "agent_id": random.choice(
                        [i + 1 for i in range(numBuyers, numBuyers + numAgents)]
                    ),
                    "buyer_id": random.choice([i + 1 for i in range(numBuyers)]),
                    "date_created": date_sold,
                }
            )

            session.add(order)

        # Commit changes to the database and log success message
        session.commit()
        info_logger.info("Orders data created")
    except Exception as error:
        error_logger.error(f'"{error}" -> Error on creating orders data')
