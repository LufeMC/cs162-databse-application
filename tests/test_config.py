import os

# Get the absolute path of the directory containing this file
TEST_DB = "test.db"
basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    """
    Configuration settings for the Flask app.

    Attributes:
    - TESTING: If the app is in testing mode
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - LOG_FILE_NAME: Log file name
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, TEST_DB)
    LOG_FILE_NAME = "log-test.txt"
