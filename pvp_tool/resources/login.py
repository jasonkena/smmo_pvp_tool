import string
import secrets

from flask import current_app
from flask_restful import Resource, abort
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required,
    create_access_token,
)
from pvp_tool.utils import server_get_user
from pvp_tool.actions import get_user


class LoginStatus(Resource):
    decorators = [jwt_required(optional=True, fresh=False)]

    def get(self):
        # db.session.commit() is not necessary
        # can be None, -1, or positive
        identity = get_jwt_identity()
        if (identity is not None) and (identity > -1):
            return {"uid": identity, "balance": get_user(identity).balance}
        return {"uid": None, "balance": 0}


class LoginRequest(Resource):
    def get(self, uid):
        current_motto = server_get_user(uid)["motto"]
        target_motto = get_random_string(
            current_app.config["LOGIN_REQUEST_MOTTO_LENGTH"]
        )
        assert current_motto != target_motto

        data = {"uid": uid, "motto": target_motto}
        verification_token = create_access_token(
            -1,
            fresh=False,
            expires_delta=current_app.config["LOGIN_REQUEST_DELTA"],
            additional_claims={"verify_data": data},
        )
        return {
            "uid": uid,
            "motto": target_motto,
            "verification_token": verification_token,
        }


class LoginVerify(Resource):
    decorators = [jwt_required(fresh=False)]

    def get(self):
        # NOTE: this will raise KeyError if fresh=True
        claims = get_jwt()["verify_data"]
        current_motto = server_get_user(claims["uid"])["motto"]

        if (claims["motto"] == current_motto) or current_app.config[
            "BYPASS_MOTTO_CHECK"
        ]:
            access_token = create_access_token(
                claims["uid"],
                fresh=True,
                expires_delta=current_app.config["LOGIN_DELTA"],
            )
            return {"access_token": access_token}
        abort(401, description=f"Player {claims['uid']}'s motto != {claims['motto']}")


def get_random_string(length):
    alphabet = string.ascii_uppercase + string.digits
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    return password
