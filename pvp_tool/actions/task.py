from flask import current_app
from datetime import datetime
from pvp_tool.utils import db
from pvp_tool.models import Task, Player, parse_player_json


def get_task(task_id, is_player_task):
    # tuple because composite primary task
    key = {"uid": task_id, "is_player_task": is_player_task}
    task = db.session.get(Task, key)
    if not task:
        task = Task(**key)
        db.session.add(task)
    return task


def assign_task(task, user):
    # https://stackoverflow.com/questions/270879/efficiently-updating-database-using-sqlalchemy-orm
    # ^ is not used because limit cannot be used with update. Workaround is complex
    # https://stackoverflow.com/questions/25943616/update-limit-1-with-sqlalchemy-and-postgresql/25943713#25943713
    if user:
        task.assigned_user = user
        task.assigned_timestamp = datetime.utcnow()
    else:
        task.assigned_user = None
        task.assigned_timestamp = None


def process_task_result(task, user, json_dict):
    # NOTE: assertion may be triggered by clean_tasks
    if task.assigned_user != user:
        print(f"Warning: non-assigned user {user} is submitting task {task}")

    if task.is_player_task:
        dictionary = parse_player_json(json_dict)
        # in order to handle error edge cases
        dictionary["uid"] = task.uid
        dictionary["user"] = user
        dictionary["timestamp"] = datetime.utcnow()

        player = Player(**dictionary)
        db.session.merge(player)
    else:
        if "error" not in json_dict:
            jobs = task.jobs
            player_ids = [player["user_id"] for player in json_dict]
            tasks = [get_task(player_id, True) for player_id in player_ids]
            for subtask in tasks:
                # APPEND, do not substitute jobs because may already exist
                subtask.jobs.extend(jobs)
            db.session.add_all(tasks)
    db.session.delete(task)


def clean_tasks():
    # NOTE: clean_tasks is currently called automatically in batch.py
    old_tasks = (
        db.session.query(Task)
        .filter(
            Task.assigned_timestamp != None,
            Task.assigned_timestamp
            < (datetime.utcnow() - current_app.config["CLEAN_TASKS_DELTA"]),
        )
        .all()
    )

    for task in old_tasks:
        assign_task(task, None)
