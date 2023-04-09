from models.order import Order
from models.user import User
from models.office import Office
from models.listing import Listing
from models.rate import Rate
from models.commission import Commission
from extensions import session
from sqlalchemy import func, desc, or_
from query_input import run_app
import re


def format_usd(value):
    """
    Transform a matched float into a formatted USD string.

    Args:
        value (float): The float to be converted.

    Returns:
        str: The formatted USD string.
    """
    return "${:,.2f}".format(value)


def get_top_5_offices_month(
    first_day_of_current_month, last_second_of_current_month, session=session
):
    """
    Returns the top 5 offices based on the count of orders made in a given month.

    Args:
        first_day_of_current_month (datetime): The first day of the month to get orders from.
        last_second_of_current_month (datetime): The last second of the month to get orders from.

    Returns:
        list: A list of tuples where each tuple contains an Office object and the count of
        orders made in that office.
    """

    top_5_offices_month = (
        session.query(Office, func.count(Office.id))
        .join(User, Office.id == User.office_id)
        .join(Order, User.id == Order.agent_id)
        .filter(
            Order.date_created >= first_day_of_current_month,
            Order.date_created <= last_second_of_current_month,
        )
        .group_by(Office.id)
        .order_by(desc(func.count(Office.id)))
        .limit(5)
        .all()
    )
    return top_5_offices_month


def get_top_5_agents_month(
    first_day_of_current_month, last_second_of_current_month, session=session
):
    """
    Returns the top 5 agents based on the count of orders made in a given month.

    Args:
        first_day_of_current_month (datetime): The first day of the month to get orders from.
        last_second_of_current_month (datetime): The last second of the month to get orders from.

    Returns:
        list: A list of tuples where each tuple contains a User object and the count of
        orders made by that user.
    """
    top_5_agents_month = (
        session.query(User, func.count(User.id))
        .join(Order, User.id == Order.agent_id)
        .filter(
            Order.date_created >= first_day_of_current_month,
            Order.date_created <= last_second_of_current_month,
        )
        .group_by(User.id)
        .order_by(desc(func.count(User.id)))
        .limit(5)
        .all()
    )
    return top_5_agents_month


def get_averages(
    first_day_of_current_month, last_second_of_current_month, session=session
):
    """
    Returns the average price of sold listings and the average time between the
    date the listing was created and the date it was sold, in days, for a given month.

    Args:
        first_day_of_current_month (datetime): The first day of the month to get sold listings from.
        last_second_of_current_month (datetime): The last second of the month to get sold listings from.

    Returns:
        tuple: A tuple containing the average price of sold listings and the average time
        between the date the listing was created and the date it was sold, in days.
    """
    averages = (
        session.query(
            func.round(func.avg(Listing.price), 2),
            func.round(
                func.avg(
                    func.julianday(Listing.date_sold)
                    - func.julianday(Listing.date_created)
                )
            ),
            0,
        )
        .filter(
            Listing.date_created >= first_day_of_current_month,
            Listing.date_created <= last_second_of_current_month,
            Listing.sold == True,
        )
        .first()
    )
    return averages


def create_commissions(
    first_day_of_current_month, last_second_of_current_month, session=session
):
    """
    Creates commission objects for each agent based on the orders they made in a given month.

    Args:
        first_day_of_current_month (datetime): The first day of the month to get orders from.
        last_second_of_current_month (datetime): The last second of the month to get orders from.

    Returns:
        bool: True if commissions were created, False if they were not because they
        already exist for the given month.
    """
    existing_commissions = (
        session.query(Commission)
        .filter(Commission.month == last_second_of_current_month)
        .all()
    )
    if len(existing_commissions) == 0:
        # Get all orders for the given month, and their corresponding agents and listing prices.
        month_orders = (
            session.query(User.id, User.name, Listing.price)
            .join(Order, User.id == Order.agent_id)
            .join(Listing, Order.listing_id == Listing.id)
            .filter(
                Order.date_created >= first_day_of_current_month,
                Order.date_created <= last_second_of_current_month,
            )
            .order_by(User.id)
            .all()
        )
        print(len(month_orders))

        agents_added = set()
        agents = {}

        # Calculate commission for each order, and sum the commissions for each agent.
        for order in month_orders:
            order_agent_id = order[0]
            order_agent_name = order[1]
            order_price = order[2]
            rate = (
                session.query(Rate)
                .filter(
                    Rate.min_price <= order_price,
                    or_(Rate.max_price >= order_price, Rate.max_price == None),
                )
                .first()
            )
            total_commission = round(order_price * rate.rate, 2)
            commission = {
                "agent_id": order_agent_id,
                "total_commission": total_commission,
                "month": last_second_of_current_month,
            }

            if order_agent_id in agents_added:
                agents[f"{order_agent_name}"]["total_commission"] += total_commission
            else:
                agents_added.add(order_agent_id)
                agents[f"{order_agent_name}"] = commission

        # Create a Commission object for each agent with the total commission for the month.
        for agent in agents.keys():
            commission = Commission(**agents[agent])
            session.add(commission)

        session.commit()
        return (
            True,
            [
                [agent, format_usd(agents[agent]["total_commission"])]
                for agent in agents.keys()
            ],
        )

    return (False, [])


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    run_app(
        get_top_5_offices_month,
        get_top_5_agents_month,
        get_averages,
        create_commissions,
        format_usd,
    )
