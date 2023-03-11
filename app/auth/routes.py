import jwt

from flask import render_template, request, make_response
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
from config import Config

from app.auth import bp
from app.models.user import User
from app.extensions import db


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    """
    A route for logging in a user.

    GET requests will display the login page, while POST requests
    will attempt to log in the user.

    Returns:
        A rendered template containing the login page (for GET requests),
        or a response object indicating success or failure (for POST requests).
    """
    if (request.method == 'POST'):
        try:
            userData = request.get_json()

            existingUser = User.query\
                .filter_by(email=userData['email'])\
                .first()

            if (not existingUser):
                return make_response({"message": 'User not found'}, 404)
            # Compares the password with the hashed password stored in the database
            elif (check_password_hash(existingUser.password, userData['password'])):
                jwtToken = jwt.encode({
                    'uuid': existingUser.uuid,
                    'exp': datetime.utcnow() + timedelta(days=1)
                }, Config.SECRET_KEY)

                response = make_response({"message": 'User logged in!'}, 200)
                response.set_cookie('user_uuid', jwtToken)

                return response

            return make_response({"message": 'Wrong password'}, 401)
        except Exception as error:
            return make_response({"message": error}, 500)
    else:
        if ('message' in request.args):
            response_auth = request.args['message']
            return render_template('./auth/login.html', message=response_auth)
        else:
            return render_template('./auth/login.html', )


@bp.route('/register/', methods=['POST', 'GET'])
def register():
    """
    A route for registering a new user.

    GET requests will display the registration page, while POST
    requests will attempt to create a new user.

    Returns:
        A rendered template containing the registration page (for GET
        requests), or a response object indicating success or failure
        (for POST requests).
    """
    if (request.method == 'POST'):
        try:
            newUserData = request.get_json()
            newUserData['uuid'] = uuid4()

            existingUser = User.query\
                .filter_by(email=newUserData['email'])\
                .first()

            if (not existingUser):
                # Hashes the password for saving in the database
                newUserData['password'] = generate_password_hash(
                    newUserData['password'])
                user = User(**newUserData)
                db.session.add(user)
                db.session.commit()

                return make_response({"message": 'User created successfully! Login now'}, 201)
            else:
                return make_response({"message": 'This email is already registered! Login now'}, 202)
        except Exception as error:
            return make_response({"message": error}, 500)
    else:
        return render_template('./auth/register.html')


@bp.route('/logout/')
def logout():
    """
    A route for logging out a user.

    Returns:
        A response object indicating success.
    """
    response = make_response({"message": 'User logged out!'}, 200)
    response.set_cookie('user_uuid', expires=0)

    return response
