import jwt

from flask import render_template, request, make_response, redirect
from werkzeug.security import check_password_hash

from datetime import datetime, timedelta
from config import Config

from app.auth import bp
from app.models.user import User
from app.extensions import info_logger, error_logger
from config import Config


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

            info_logger.info(
                f"Client tried to log in with email: {userData['email']}")

            if (not existingUser):
                error_logger.error(
                    f"User not found with email: {userData['email']}")
                return make_response({"message": 'User not found'}, 404)
            # Compares the password with the hashed password stored in the database
            elif (check_password_hash(existingUser.password, userData['password'])):
                jwtToken = jwt.encode({
                    'uuid': existingUser.uuid,
                    'exp': datetime.utcnow() + timedelta(days=1)
                }, Config.SECRET_KEY)

                info_logger.info(
                    f"User successfully log in with email: {userData['email']}")

                response = make_response(
                    {"message": 'User logged in!'}, 200)
                response.set_cookie('user_uuid', jwtToken)

                return response

            error_logger.error(
                f"User tried to log in with email: {userData['email']}, but used the wrong password")
            return make_response({"message": 'Wrong password'}, 401)
        except Exception as error:
            error_logger.error(f"Error on log in")
            return make_response({"message": error}, 500)
    else:
        if ('message' in request.args):
            info_logger.info(f"Login view rendered with message")
            response_auth = request.args['message']
            return render_template('./auth/login.html', message=response_auth)
        else:
            info_logger.info(f"Login view rendered without message")
            return render_template('./auth/login.html')


@bp.errorhandler(404)
def notFound():
    return redirect('/auth/login')
