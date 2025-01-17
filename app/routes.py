from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import date






tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")



                            #### HELPER FUNCTIONS ####

def return_task_or_abort(task_id):
    try:
        verified_id = int(task_id)
    except ValueError:
        abort(make_response({"details":"Invalid ID: id must be an integer"}, 400))

    task = Task.query.get(verified_id)

    if not task:
        abort(make_response({"details":"Invalid ID: id does not exist"}, 404))

    return task



def return_goal_or_abort(goal_id):
    try:
        verified_id = int(goal_id)
    except ValueError:
        abort(make_response({"details":"Invalid ID: id must be an integer"}, 400))

    goal = Goal.query.get(verified_id)

    if not goal:
        abort(make_response({"details":"Invalid ID: id does not exist"}, 404))

    return goal


def boolean_completeness(completed_at):
    if not completed_at:
        return False
    return True


def format_return_task(target_task):
    return {"id": target_task.task_id,
            "goal_id": target_task.goal_id,
            "title": target_task.title,
            "description": target_task.description,
            "is_complete": boolean_completeness(target_task.completed_at)
            }
    
def format_return_goal(target_goal):
    return {"id": target_goal.goal_id,
            "title": target_goal.title
            }





                                #### TASK ROUTES ####

@tasks_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
            # completed_at=request_body["completed_at"],
        )

        db.session.add(new_task)
        db.session.commit()

        return {"task":format_return_task(new_task)}, 201
    except KeyError:
        return {"details":"Invalid data"}, 400
   





@tasks_bp.route("", methods=["GET"])
def list_all_tasks():
    
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()



    response = [format_return_task(task) for task in tasks]
    return jsonify(response), 200






@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = return_task_or_abort(task_id)

    return {"task":format_return_task(task)}, 200






@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task=return_task_or_abort(task_id)

    request_body=request.get_json()

    if "title" not in request_body or \
    "description" not in request_body:
        return jsonify("Must include task title and description"), 400

    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]

    db.session.commit()

    return {"task":format_return_task(task)}, 200




@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task=return_task_or_abort(task_id)
    reponse_message = f'Task {task.task_id} "{task.title}" successfully deleted'

    db.session.delete(task)
    db.session.commit()

    return {"details": reponse_message}, 200



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task=return_task_or_abort(task_id)

    task.completed_at = date.today()
   
    db.session.commit()

    return {"task":format_return_task(task)}, 200



@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task=return_task_or_abort(task_id)

    task.completed_at = None
   
    db.session.commit()

    return {"task":format_return_task(task)}, 200







                            #### GOAL ROUTES ####

@goals_bp.route("", methods = ["POST"])
def add_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title=request_body["title"],
        )

        db.session.add(new_goal)
        db.session.commit()

        return {"goal":format_return_goal(new_goal)}, 201
    except KeyError:
        return {"details":"Invalid data"}, 400
   





@goals_bp.route("", methods=["GET"])
def list_all_goals():    
    goals = Goal.query.all()

    response = [format_return_goal(goal) for goal in goals]
    return jsonify(response), 200






@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = return_goal_or_abort(goal_id)

    return {"goal":format_return_goal(goal)}, 200






@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal=return_goal_or_abort(goal_id)

    request_body=request.get_json()

    if "title" not in request_body:
        return jsonify("Must include goal title"), 400

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal":format_return_goal(goal)}, 200




@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal=return_goal_or_abort(goal_id)
    reponse_message = f'Goal {goal.goal_id} "{goal.title}" successfully deleted'

    db.session.delete(goal)
    db.session.commit()

    return {"details": reponse_message}, 200






                            #### LINKED ROUTES ####

# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def send_tasks_to_goal(goal_id):
#     goal=return_goal_or_abort(goal_id)

#     request_body=request.get_json()

#     if "task_ids" not in request_body:
#         return jsonify("Must include task ids"), 400

#     for task_id in request_body["task_ids"]:
#         task = return_goal_or_abort(task_id)
#         task.goal = goal_id

#     db.session.commit()

#     return jsonify({"id": goal_id, "task_ids": goal.tasks}), 200




@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def list_all_goal_tasks(goal_id):    
    goal = return_goal_or_abort(goal_id)

    response = [format_return_task(task) for task in goal.tasks]
    return jsonify({"id": int(goal_id), "title": goal.title, "tasks": response}), 200



