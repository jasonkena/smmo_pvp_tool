from flask import current_app
from pvp_tool.utils import db, flatten
from pvp_tool.models import Task, create_cache
from pvp_tool.actions.task import (
    assign_task,
    get_task,
    process_task_result,
    clean_tasks,
    process_pending_tasks,
)
from pvp_tool.actions.mining import mining


def request_batch(user, num_tasks):
    clean_tasks()
    process_pending_tasks()

    tasks = []
    if len(tasks) < num_tasks:
        tasks.extend(
            db.session.query(Task)
            .filter(Task.assigned_user == user)
            .limit(num_tasks - len(tasks))
            .all()
        )

    if len(tasks) < num_tasks:
        tasks.extend(
            db.session.query(Task)
            .filter(Task.assigned_user == None)
            .limit(num_tasks - len(tasks))
            .all()
        )

    if len(tasks) < num_tasks:
        tasks.extend(
            mining(max(current_app.config["MINING_BUFFER"], num_tasks - len(tasks)))
        )

    tasks = tasks[:num_tasks]
    for task in tasks:
        assign_task(task, user)

    return tasks


def submit_batch(user, json_dict):
    max_id = get_max_id(json_dict)
    create_cache(max_id)

    user.balance += len(json_dict["players"]) + len(json_dict["guilds"])
    for player_id, player in json_dict["players"].items():
        process_task_result(get_task(player_id, True), user, player)
    for guild_id, guild in json_dict["guilds"].items():
        process_task_result(get_task(guild_id, False), user, guild)


def get_max_id(json_dict):
    players = [k for k, v in json_dict["players"].items() if "error" not in v]
    guilds = [v for k, v in json_dict["guilds"].items() if "error" not in v]
    guild_players = flatten([[user["user_id"] for user in guild] for guild in guilds])

    total = players + guild_players
    if total:
        return max(players + guild_players)
    return None
