from flask import render_template, redirect, request, make_response, url_for
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
        if ('response_auth' in request.args):
            response_auth = request.args['response_auth']
            return render_template('./login.html', response_auth=json.loads(response_auth))
        else:
            return render_template('./login.html')
    else:
        userData = request.form.to_dict()

        existingUser = User.query\
            .filter_by(email=userData['email'])\
            .first()

        if (not existingUser):
            response_auth = {"message": 'User not found'}
            response = make_response(render_template(
                './login.html', response_auth=response_auth))
            response.status_code = 404
            return response
        elif (check_password_hash(existingUser.password, userData['password'])):
            jwtToken = jwt.encode({
                'uuid': existingUser.uuid,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, Config.SECRET_KEY)

            redirectTo = redirect('/home')
            redirectTo.headers['Authorization'] = jwtToken
            response = make_response(redirectTo)
            response.set_cookie('user_uuid', jwtToken)

            return response

        response_auth = {"message": 'Wrong password'}
        response = make_response(render_template(
            './login.html', response_auth=response_auth))
        response.status_code = 401
        return response


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

            response_auth = {"message": 'User created successfully! Login now'}
            response = make_response(render_template(
                './register.html', response_auth=response_auth))
            response.status_code = 201

            return response
        else:
            response_auth = {
                "message": 'This email is already registered! Login now'}
            response = make_response(render_template(
                './register.html', response_auth=response_auth))
            response.status_code = 202

            return response
    else:
        return render_template('./register.html')
