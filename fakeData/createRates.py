from models.rate import Rate
from extensions import session, info_logger, error_logger


def createRates(session=session):
    """
    Function that creates rates data in the database based on a dictionary
    of price ranges and their corresponding rates.

    Args:
        None

    Returns:
        None
    """

    try:
        # Define a dictionary of price ranges and their corresponding rates
        rates = {
            "0.1": [0, 99999],
            "0.075": [100000, 199999],
            "0.06": [200000, 499999],
            "0.05": [500000, 999999],
            "0.04": [1000000, None],
        }

        # Loop through the rates dictionary and create Rate objects for each price range
        for key in rates.keys():
            max_min_prices = rates[key]
            rate = Rate(
                **{
                    "rate": float(key),
                    "min_price": max_min_prices[0],
                    "max_price": max_min_prices[1],
                }
            )

            session.add(rate)

        session.commit()
        info_logger.info("Rates data created")
    except Exception as error:
        error_logger.error(f'"{error}" -> Error on creating rates data')
