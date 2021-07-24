from flask import request, current_app, url_for
from pvp_tool.utils import db, server_get_user
from pvp_tool.actions import process_query, create_hit_token, get_current_user

from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, post_dump

from marshmallow.validate import Range, OneOf


class Query(Resource):
    decorators = [jwt_required(fresh=True)]

    def post(self):
        class InputSchema(Schema):
            num_results = fields.Int(
                required=True,
                strict=True,
                validate=Range(min=1, max=current_app.config["MAX_QUERY_RESULTS"]),
            )
            guild_ids = fields.List(
                fields.Int(strict=True, validate=Range(min=1)), load_default=[]
            )
            maximum_level = fields.Int(
                strict=True,
                validate=Range(min=1),
                load_default=lambda: server_get_user(get_jwt_identity())["level"],
            )
            minimum_gold = fields.Int(strict=True, validate=Range(min=1), load_default=0)
            player_blacklist = fields.List(
                fields.Int(strict=True, validate=Range(min=1)), load_default=[]
            )
            guild_blacklist = fields.List(
                fields.Int(strict=True, validate=Range(min=1)), load_default=[]
            )
            last_update = fields.Int(strict=True, validate=Range(min=1), load_default=None)
            sort_by = fields.Str(
                validate=OneOf(["gold", "level", "last_update"]), load_default="gold"
            )

        class OutputSchema(Schema):
            uid = fields.Int(required=True, strict=True, validate=Range(min=1))
            name = fields.Str(required=True)
            level = fields.Int(required=True, strict=True, validate=Range(min=1))
            gold = fields.Int(required=True, strict=True, validate=Range(min=0))
            guild_name = fields.Str(required=True, allow_none=True, dump_default="")
            timestamp = fields.DateTime(required=True)

            @post_dump
            def generate_hit_url(self, data, many, **kwargs):
                uid = data.pop("uid")
                hit_token = create_hit_token(user, uid)

                data["url"] = url_for("hit.hit", jwt=hit_token, _external=True)
                return data

        user = get_current_user()

        try:
            data = InputSchema().load(request.get_json(force=True))
        except ValidationError as e:
            return e.messages, 422

        if current_app.config["ENFORCE_BALANCE"] and (
            user.balance < data["num_results"]
        ):
            abort(
                402,
                description=f"Insufficient balance for query with {data['num_results']} results",
            )

        data["user"] = user

        players = process_query(**data)
        result = OutputSchema(many=True).dump(players)

        db.session.commit()
        return result
