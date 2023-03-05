from flask import render_template, redirect, request, make_response
from uuid import uuid4
from app.home import bp
from app.extensions import db
from app.models.task import Task
from app.models.user import User
from app.jwt import token_required


@bp.route('/')
@token_required
def render(user, tasks):
    return render_template('./index.html', tasks=tasks)


@bp.route('/add', methods=['POST'])
@token_required
def add(user, tasks):
    if (request.method == 'POST'):
        newTask = request.form.to_dict()
        newTask['uuid'] = uuid4()
        newTask['deleted'] = False
        newTask['user_id'] = user.id
        newTask['status'] = 'toDo'
        newTask = Task(**newTask)
        db.session.add(newTask)
        db.session.commit()

        response = make_response(render_template(
            './index.html', tasks=tasks))
        response.status_code = 201
        return response


@bp.route('/next', methods=['POST'])
@token_required
def next(user, tasks):
    task = Task.query\
        .filter_by(uuid=request.form['uuid'])\
        .first()

    if (task.status == 'toDo'):
        task.status = 'doing'
    else:
        task.status = 'done'

    db.session.commit()

    response = make_response(render_template(
        './index.html', tasks=tasks))
    response.status_code = 204
    return response


@bp.route('/previous', methods=['POST'])
@token_required
def previous(user, tasks):
    task = Task.query\
        .filter_by(uuid=request.form['uuid'])\
        .first()

    if (task.status == 'done'):
        task.status = 'doing'
    else:
        task.status = 'toDo'

    db.session.commit()

    response = make_response(render_template(
        './index.html', tasks=tasks))
    response.status_code = 204
    return response


@bp.route('/delete', methods=['POST'])
@token_required
def delete(user, tasks):
    task = Task.query\
        .filter_by(uuid=request.form['uuid'])\
        .first()

    task.deleted = True
    db.session.commit()

    response = make_response(render_template(
        './index.html', tasks=tasks))
    response.status_code = 204
    return response
