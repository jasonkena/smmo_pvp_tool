from datetime import datetime
from pvp_tool.utils import db
from pvp_tool.models import Job, Task
from pvp_tool.actions.task import get_task


def create_job(user, guild_ids):
    job = Job(creating_user=user, created_timestamp=datetime.utcnow())
    tasks = []
    for guild_id in guild_ids:
        tasks.append(get_task(guild_id, False))
    # NOTE: if this crashes, don't forget to change the job completion in tasks.py
    job.tasks = tasks
    db.session.add(job)
    return job


def get_job(job_id):
    # will return None if job does not exist
    return db.session.get(Job, job_id)


def job_completed(job):
    tasks = db.session.query(Task).filter(Task.jobs.contains(job)).all()
    num_tasks = len(tasks)
    return num_tasks == 0, num_tasks
