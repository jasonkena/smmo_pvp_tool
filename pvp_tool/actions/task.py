from math import ceil
from flask import current_app
from datetime import datetime, timezone
from pvp_tool.utils import db
from pvp_tool.models import Task, PendingTask, Player, parse_player_json


def get_task(task_id, is_player_task):
    # tuple because composite primary task
    key = {"uid": task_id, "is_player_task": is_player_task}
    task = db.session.get(Task, key)
    if not task:
        task = Task(**key)
        db.session.add(task)
    return task


def create_pending_task(uid, is_player_task, timestamp):
    pending_task = PendingTask(
        uid=uid, is_player_task=is_player_task, due_timestamp=timestamp
    )
    db.session.add(pending_task)
    return pending_task


def refresh_player(player):
    # +1 because of UID 69882
    if player.hp / (player.max_hp + 1) < 0.5:
        # https://web.simple-mmo.com/diamondstore/membership
        increment = 0.1 if player.membership else 0.05
        num_increments = ceil((0.5 - player.hp / (player.max_hp + 1)) / increment)
        seconds = (
            ceil(datetime.now(tz=timezone.utc).timestamp() / 300 + num_increments) * 300
        )
        timestamp = datetime.now().fromtimestamp(seconds, tz=timezone.utc)
        create_pending_task(player.uid, True, timestamp)


def assign_task(task, user):
    # https://stackoverflow.com/questions/270879/efficiently-updating-database-using-sqlalchemy-orm
    # ^ is not used because limit cannot be used with update. Workaround is complex
    # https://stackoverflow.com/questions/25943616/update-limit-1-with-sqlalchemy-and-postgresql/25943713#25943713
    if user:
        task.assigned_user = user
        task.assigned_timestamp = datetime.now(timezone.utc)
    else:
        task.assigned_user = None
        task.assigned_timestamp = None


def process_task_result(task, user, json_dict):
    # NOTE: assertion may be triggered by clean_tasks
    if task.assigned_user != user:
        print(f"Warning: non-assigned user {user} is submitting task {task}")

    if task.is_player_task:
        old_player = db.session.get(Player, task.uid)
        dictionary = parse_player_json(json_dict)
        # in order to handle error edge cases
        dictionary["uid"] = task.uid
        dictionary["user"] = user

        new_time = datetime.now(timezone.utc)
        # Weight decay
        if old_player:
            dictionary["weight"] = old_player.weight * (
                (0.5)
                ** (
                    (new_time - old_player.timestamp) / current_app.config["DECAY_TIME"]
                )
            )
        else:
            dictionary["weight"] = 0.0

        dictionary["timestamp"] = new_time
        player = db.session.merge(Player(**dictionary))
        if current_app.config["REFRESH_PLAYER"]:
            refresh_player(player)

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
            < (datetime.now(timezone.utc) - current_app.config["CLEAN_TASKS_DELTA"]),
        )
        .all()
    )

    for task in old_tasks:
        assign_task(task, None)


def process_pending_tasks():
    query = db.session.query(PendingTask).filter(
        PendingTask.due_timestamp < datetime.now(timezone.utc)
    )
    for pending_task in query.all():
        get_task(pending_task.uid, pending_task.is_player_task)
    query.delete()
