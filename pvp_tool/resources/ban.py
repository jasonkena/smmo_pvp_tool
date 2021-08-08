from pvp_tool.utils import db
from pvp_tool.actions import ban_player, get_current_user

from flask_restful import Resource
from flask_jwt_extended import jwt_required


class BanPlayer(Resource):
    decorators = [jwt_required(fresh=True)]

    def post(self, player_id):
        user = get_current_user()
        ban_player(user, player_id)

        db.session.commit()
        return {"message": "Player successfully banned"}
