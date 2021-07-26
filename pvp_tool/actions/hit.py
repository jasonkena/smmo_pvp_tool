from flask import current_app
from pvp_tool.utils import db
from flask_jwt_extended import create_access_token


def hit(user, target_id):
    pass


def create_hit_token(user, target_id):
    data = {"uid": user.uid, "target": target_id}
    access_token = create_access_token(
        -1,
        fresh=False,
        expires_delta=current_app.config["HIT_DELTA"],
        additional_claims={"hit_data": data},
    )
    return access_token
