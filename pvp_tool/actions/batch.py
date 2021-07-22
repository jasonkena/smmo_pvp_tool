from pvp_tool.utils import db
from pvp_tool.models import Task
from pvp_tool.actions.task import (
    assign_task,
    get_task,
    process_task_result,
    clean_tasks,
)


def request_batch(user, num_tasks):
    clean_tasks()

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
        tasks.extend(mining(num_tasks - len(tasks)))

    for task in tasks:
        assign_task(task, user)

    return tasks


def mining(num_targets):
    return []


def submit_batch(user, json_dict):
    """
    FORMAT:
    { "players": {id: {...}},
    "guilds": {
    "guild_id": {id: [users]}
    }
    }

    both are dicts, because returned dictionary can be {"error": "error"}

    """
    user.balance += len(json_dict["players"]) + len(json_dict["guilds"])
    for player_id, player in json_dict["players"].items():
        process_task_result(get_task(player_id, True), user, player)
    for guild_id, guild in json_dict["guilds"].items():
        process_task_result(get_task(guild_id, False), user, guild)
