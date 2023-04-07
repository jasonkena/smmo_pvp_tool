from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__, url_prefix="/api")

import pvp_tool.resources.login as login

login_bp = Blueprint("login", login.__name__, url_prefix="/login")
login_api = Api(login_bp)
login_api.add_resource(login.LoginStatus, "/status")
login_api.add_resource(login.LoginRequest, "/<int:uid>")
login_api.add_resource(login.LoginVerify, "/verify")

import pvp_tool.resources.batch as batch

batch_bp = Blueprint("batch", batch.__name__, url_prefix="/batch")
batch_api = Api(batch_bp)
batch_api.add_resource(batch.BatchRequest, "/request")
batch_api.add_resource(batch.BatchSubmit, "/submit")

import pvp_tool.resources.job as job

job_bp = Blueprint("job", job.__name__, url_prefix="/job")
job_api = Api(job_bp)
job_api.add_resource(job.JobCreate, "/create")
job_api.add_resource(job.JobGet, "/<int:job_id>")

import pvp_tool.resources.query as query

query_bp = Blueprint("query", query.__name__, url_prefix="/query")
query_api = Api(query_bp)
query_api.add_resource(query.Query, "/submit")

import pvp_tool.resources.hit as hit

hit_bp = Blueprint("hit", hit.__name__, url_prefix="/hit")
hit_api = Api(hit_bp)
hit_api.add_resource(hit.Hit, "/get")

import pvp_tool.resources.leaderboard as leaderboard

leaderboard_bp = Blueprint(
    "leaderboard", leaderboard.__name__, url_prefix="/leaderboard"
)
leaderboard_api = Api(leaderboard_bp)
leaderboard_api.add_resource(leaderboard.Leaderboard, "/get")


api_bp.register_blueprint(login_bp)
api_bp.register_blueprint(batch_bp)
api_bp.register_blueprint(job_bp)
api_bp.register_blueprint(query_bp)
api_bp.register_blueprint(hit_bp)
api_bp.register_blueprint(leaderboard_bp)
