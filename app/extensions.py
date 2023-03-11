from flask_sqlalchemy import SQLAlchemy

# Initializing db on SQLAlchemy
db = SQLAlchemy(session_options={
    'expire_on_commit': False
})
