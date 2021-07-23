from flask import request, current_app
from pvp_tool.utils import db
from pvp_tool.actions import create_job, get_job, job_completed, get_current_user

from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, ValidationError

from marshmallow.validate import Range, Length


class JobCreate(Resource):
    decorators = [jwt_required(fresh=True)]

    def post(self):
        class InputSchema(Schema):
            guild_ids = fields.List(
                fields.Int(strict=True, validate=Range(min=1)),
                required=True,
                validate=Length(min=1, max=current_app.config["MAX_JOB_GUILDS"]),
            )

        user = get_current_user()

        try:
            data = InputSchema().load(request.get_json(force=True))
        except ValidationError as e:
            return e.messages, 422

        job = create_job(user, data["guild_ids"])
        db.session.commit()

        return {"job_id": job.id, "num_tasks": len(job.tasks)}


class JobGet(Resource):
    decorators = [jwt_required(fresh=True)]

    def get(self, job_id):
        user = get_current_user()
        # early commit since the rest does not change database state
        db.session.commit()

        job = get_job(job_id)
        if job is not None:
            if (user == job.creating_user) or (
                user in current_app.config["ADMIN_UIDS"]
            ):
                is_completed, num_tasks = job_completed(job)
                return {
                    "job_id": job_id,
                    "num_tasks": num_tasks,
                    "is_completed": is_completed,
                }

        abort(
            401,
            description=f"User does not have access to Job {job_id} or Job {job_id} does not exist",
        )
