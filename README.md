# CS162 Database Application 12:30 - Luis Fernando

## Project Structure

`/.github/workflows` contains CI/CD code.

`/app.py` main application that creates models and fake data.

`/fakeData` contains the code that creates the fake data in the database

`/models` contains the DB models using SQLAlchemy.

`/extensions.py` contains build-in extensions that are initialized in `app.py`.

`/tests` contains the unit tests files.

`/config.py` contains the environment variables used in this code

## Virtual Environment and run the app
Create the virtualenv:

    $ virtualenv -p python3 venv

Sometimes, the above doesn't work. You can try then:

    $ python3 -m venv venv

Then, activate the activate the virtualenv. For Mac

    $ source venv/bin/activate

For **Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

To create the models with the fake data on the database:

	$ python3 app.py

To query the data based on a certain month of an year:

	$ python3 query.py

To run the unit tests:

	$ python3 -m unittest discover tests

When you are done. Close the virtual env.

    $ deactivate