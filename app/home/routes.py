from flask import render_template, redirect, request, make_response
from uuid import uuid4
from app.home import bp
from app.extensions import db, info_logger, error_logger
from app.models.task import Task
from app.models.user import User
from app.jwt import token_required
from config import Config


@bp.route('/')
@token_required
def render(user, tasks):
    """
    Renders the home page with the given user's tasks.

    Args:
        user (User): The authenticated user.
        tasks (list): The user's tasks (toDo, doing and done).

    Returns:
        The rendered home page HTML template with the user's tasks.
    """
    if ('message' in request.args):
        info_logger.info(f"Home view rendered with message")
        response_auth = request.args['message']
        return render_template('./home/home.html', tasks=tasks, message=response_auth)
    else:
        info_logger.info(f"Home view rendered without message")
        return render_template('./home/home.html', tasks=tasks)


@bp.route('/add', methods=['POST'])
@token_required
def add(user, tasks):
    """
    Adds a new task to the authenticated user's task list.

    Args:
        user (User): The authenticated user.
        tasks (list): The user's tasks.

    Returns:
        A response indicating whether the task was successfully added.
    """
    try:
        newTask = request.get_json()
        newTask['uuid'] = str(uuid4())
        newTask['user_id'] = user.id
        newTask = Task(**newTask)
        db.session.add(newTask)
        db.session.commit()
        info_logger.info(
            f"New task added for user with uuid: {user.uuid}")

        response = make_response({"message": 'Task added'}, 201)
        return response
    except Exception as error:
        error_logger.error(
            f"An error occured while adding a new task for user with uuid: {user.uuid}")
        response = make_response({"message": error}, 500)
        return response


@bp.route('/move/<string:type>', methods=['PATCH'])
@token_required
def move(user, tasks, type):
    """
    Moves a task to the next or previous status.

    Args:
        user (User): The authenticated user.
        tasks (list): The user's tasks.
        type (str): The type of move to make (either "next" or "previous").

    Returns:
        A response indicating whether the task was successfully moved.
    """
    try:
        uuid = request.get_json()['uuid']
        task = Task.query\
            .filter_by(uuid=uuid)\
            .first()

        if (type == 'next'):
            task.status += 1
        else:
            task.status -= 1

        db.session.commit()

        info_logger.info(
            f"Task with uuid {task.uuid} moved ({type}) for user with uuid: {user.uuid}")

        response = make_response({"message": 'Task moved'}, 204)
        return response

    except Exception as error:
        error_logger.error(f"An error occured while adding moving task with uuid\
                  {task.uuid} ({type}) for user with uuid: {user.uuid}")
        response = make_response({"message": error}, 500)
        return response


@bp.route('/remove/<string:uuid>', methods=['DELETE'])
@token_required
def delete(user, tasks, uuid):
    """
    Marks a task as deleted.

    Args:
        user (User): The authenticated user.
        tasks (list): The user's tasks.
        uuid (str): The UUID of the task to delete.

    Returns:
        A response indicating whether the task was successfully deleted.
    """
    try:
        task = Task.query\
            .filter_by(uuid=uuid)\
            .first()

        task.deleted = True

        db.session.commit()

        info_logger.info(
            f"Task {task.uuid} deleted for user with uuid: {user.uuid}")

        response = make_response({"message": 'Task moved'}, 204)
        return response

    except Exception as error:
        error_logger.error(f"An error occured while adding deleting task with uuid\
                  {task.uuid} for user with uuid: {user.uuid}")
        response = make_response({"message": error}, 500)
        return response


@bp.errorhandler(404)
def notFound():
    return redirect('/home')
