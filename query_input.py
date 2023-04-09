from datetime import datetime, timedelta
import calendar
import re


# Define a function to run the application
def run_app(
    get_top_5_offices_month,
    get_top_5_agents_month,
    get_averages,
    create_commissions,
    format_usd,
):
    """
    This function runs an application that generates a monthly report for a real
    estate agency. It prompts the user to input the year and month they want to
    generate the report for, and then uses various functions to generate and print
    out the report.

    Args:
        get_top_5_offices_month (function): A function that takes two datetime objects
            as arguments (the first and last second of the month) and returns a list of
            tuples, where each tuple contains an office object and its total sales for
            the month.
        get_top_5_agents_month (function): A function that takes two datetime objects as
            arguments (the first and last second of the month) and returns a list of tuples,
            where each tuple contains an agent object, their email, and their total sales for
            the month.
        get_averages (function): A function that takes two datetime objects as arguments
            (the first and last second of the month) and returns a tuple containing the average
            selling price and the average number of days a property spends on the market.
        create_commissions (function): A function that takes two datetime objects as arguments
            (the first and last second of the month) and generates commissions for the agency's
            agents based on their sales for the month.
        format_usd (function): A function that takes a float as an argument and returns a string
            representing that float formatted as USD.

    Returns:
        None
    """

    # Define an ASCII art string to display at the beginning of the application
    ascii_art = """
    ██████████████████████████████████████████████████████████████████████████████████████████
    █░█░█▄─▀█▀─▄█▄─▄█▄─▀█▄─▄█▄─▄▄─█▄─▄▄▀█▄─█─▄██▀▄─████▄─▄▄▀█▄─▄▄─█▄─▄▄─█─▄▄─█▄─▄▄▀█─▄─▄─█░█░█
    █▄█▄██─█▄█─███─███─█▄▀─███─▄█▀██─▄─▄██▄▀▄███─▀─█████─▄─▄██─▄█▀██─▄▄▄█─██─██─▄─▄███─███▄█▄█
    ▀▀▀▀▀▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▀▀▄▀▀▀▄▄▀▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▀▀▀▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀▀▀▀▀
    """

    print(ascii_art)

    # Prompt the user for the year and validate the input
    report_year = input("What year do you want the report to for? (Example: 2023)\n")

    while not bool(re.match(r"^[1-9]\d{3}$", report_year)):
        report_year = input("Please input a valid year\n")

    # Prompt the user for the month and validate the input
    report_month = input("What month do you want the report to for? (01 to 12)\n")

    while not bool(re.match(r"^(0[1-9]|1[0-2])$", report_month)):
        report_month = input("Please input a valid month\n")

    # Create a string with the year and month, set the day to 01 and convert to a datetime object
    report_date = f"{report_year}-{report_month}-01"
    date_datetime = datetime.strptime(report_date, "%Y-%m-%d").replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Creates the firsy and last moments of the month
    first_day_of_current_month = datetime(date_datetime.year, date_datetime.month, 1)
    last_day_of_current_month = first_day_of_current_month.replace(
        day=calendar.monthrange(
            first_day_of_current_month.year, first_day_of_current_month.month
        )[1]
    )
    last_second_of_current_month = (
        last_day_of_current_month + timedelta(days=1) - timedelta(seconds=1)
    )

    # Call the function to get the top 5 offices in the current month and print them
    top_5_offices_month = get_top_5_offices_month(
        first_day_of_current_month, last_second_of_current_month
    )
    print(
        f"These are the top 5 offices in this month:\n"
        + "\n".join(
            [
                f"{office[0].name} | Total sales: {office[1]}"
                for office in top_5_offices_month
            ]
        )
    )

    print("\n----------------------------------------------------------------\n")

    # Call the function to get the top 5 agents in the current month and print them
    top_5_agents_month = get_top_5_agents_month(
        first_day_of_current_month, last_second_of_current_month
    )
    print(
        f"These are the top 5 agents in this month:\n"
        + "\n".join(
            [
                f"{agent[0].name} | Email: {agent[0].email} | Total sales: {agent[1]}"
                for agent in top_5_agents_month
            ]
        )
    )

    print("\n----------------------------------------------------------------\n")

    # Call the function to get the average number of days in the market and the average price in the marker in the current month and print it
    averages = get_averages(first_day_of_current_month, last_second_of_current_month)

    print(f"Average number of days in the market in this month: {int(averages[1])}")

    print("\n----------------------------------------------------------------\n")

    print(f"Average selling price in this month: {format_usd(averages[0])}")

    print("\n----------------------------------------------------------------\n")

    # Call the function to create commissions for the current month and print a message based on whether new commissions were added
    new_commissions = create_commissions(
        first_day_of_current_month, last_second_of_current_month
    )
    if new_commissions[0]:
        print(
            "Commissions added to the database! There are the commissions for the month:\n"
            + "\n".join(
                [
                    f"{commission[0]}: {commission[1]}"
                    for commission in new_commissions[1]
                ]
            )
        )
    else:
        print("This month's commissions were already added to the database")
