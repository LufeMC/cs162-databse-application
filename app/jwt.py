from flask import request, jsonify
from config import Config
from app.models.user import User
from app.models.task import Task
import jwt
from functools import wraps


def getCookie(name):
    value = f"; {request.headers['Cookie']}"
    parts = value.split(f"; {name}=")
    if len(parts) == 2:
        return parts.pop().split(';')[0]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if getCookie('user_uuid'):
            token = getCookie('user_uuid')
        # return 401 if token is not passed
        else:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user = User.query\
                .filter_by(uuid=data['uuid'])\
                .first()

            tasks = {
                'toDo': Task.query.filter_by(user_id=user.id, status='toDo', deleted=False),
                'doing': Task.query.filter_by(user_id=user.id, status='doing', deleted=False),
                'done': Task.query.filter_by(user_id=user.id, status='done', deleted=False)
            }
        except Exception as e:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return f(user, tasks, *args, **kwargs)

    return decorated
