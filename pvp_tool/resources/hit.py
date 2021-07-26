from flask import current_app, redirect
from flask_restful import Resource
from flask_jwt_extended import get_jwt, jwt_required
from pvp_tool.utils import db
from pvp_tool.actions import get_user, hit


class Hit(Resource):
    decorators = [jwt_required(fresh=False, locations="query_string")]

    def get(self):
        # will raise an error if undefined
        claims = get_jwt()["hit_data"]
        user = get_user(claims["uid"])
        target = claims["target"]
        hit(user, target)

        db.session.commit()
        return redirect(current_app.config["HIT_URL"] + str(target))
