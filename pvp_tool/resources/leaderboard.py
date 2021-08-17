from pvp_tool.utils import db
from pvp_tool.actions import get_leaderboard

from flask_restful import Resource
from marshmallow import Schema, fields


class Leaderboard(Resource):
    def get(self):
        class OutputSchema(Schema):
            uid = fields.Int(required=True)
            balance = fields.Int(required=True)

        return OutputSchema(many=True).dump(get_leaderboard())
