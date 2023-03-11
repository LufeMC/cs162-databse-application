from flask import render_template, request, make_response, url_for
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import json
import jwt
from datetime import datetime, timedelta
from config import Config

from app.auth import bp
from app.models.user import User
from app.extensions import db


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    if (request.method == 'GET'):
        if ('message' in request.args):
            response_auth = request.args['message']
            return render_template('./login.html', message=message)
        else:
            return render_template('./login.html', )
    else:
        userData = request.form.to_dict()

        existingUser = User.query\
            .filter_by(email=userData['email'])\
            .first()

        if (not existingUser):
            return make_response({"message": 'User not found'}, 404)
        elif (check_password_hash(existingUser.password, userData['password'])):
            jwtToken = jwt.encode({
                'uuid': existingUser.uuid,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, Config.SECRET_KEY)

            response = make_response({"message": 'User logged in!'}, 200)
            response.set_cookie('user_uuid', jwtToken)

            return response
        
        return make_response({"message": 'Wrong password'}, 401)


@bp.route('/register/', methods=['POST', 'GET'])
def register():
    if (request.method == 'POST'):
        newUserData = request.form.to_dict()
        newUserData['uuid'] = uuid4()

        existingUser = User.query\
            .filter_by(email=newUserData['email'])\
            .first()

        if (not existingUser):
            newUserData['password'] = generate_password_hash(
                newUserData['password'])
            user = User(**newUserData)
            db.session.add(user)
            db.session.commit()
            
            return make_response({"message": 'User created successfully! Login now'}, 201)
        else:
            return make_response({"message": 'This email is already registered! Login now'}, 202)
    else:
        return render_template('./register.html')
