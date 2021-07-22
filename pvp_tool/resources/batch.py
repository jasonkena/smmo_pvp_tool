from flask import request, current_app
from pvp_tool.utils import db
from pvp_tool.actions import request_batch, submit_batch, get_current_user
from marshmallow_oneofschema import OneOfSchema

from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range


class BatchRequest(Resource):
    decorators = [jwt_required(fresh=True)]

    def post(self):
        class InputSchema(Schema):
            num_tasks = fields.Int(
                required=True,
                strict=True,
                validate=Range(min=1, max=current_app.config["MAX_BATCH_SIZE"]),
            )

        class OutputSchema(Schema):
            uid = fields.Int(required=True)
            is_player_task = fields.Bool(required=True)

        user = get_current_user()

        try:
            data = InputSchema().load(request.get_json())
        except ValidationError as e:
            print(e.messages)
            return e.messages, 422

        batch = request_batch(user, data["num_tasks"])
        result = OutputSchema(many=True).dump(batch)

        db.session.commit()
        return result


class BatchSubmit(Resource):
    decorators = [jwt_required(fresh=True)]

    def post(self):
        class ErrorSchema(Schema):
            error = fields.Str(required=True)

        class PlayerGuildSchema(Schema):
            id = fields.Int(required=True, strict=True, validate=Range(min=1))
            name = fields.Str(required=True)

        # since some keys are Python keywords
        PlayerSchema = Schema.from_dict(
            {
                "id": fields.Int(required=True, strict=True, validate=Range(min=1)),
                "name": fields.Str(required=True),
                "level": fields.Int(required=True, strict=True, validate=Range(min=1)),
                "motto": fields.Str(required=True),
                "profile_number": fields.Str(required=True),
                "exp": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "gold": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "steps": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "npc_kills": fields.Int(
                    required=True, strict=True, validate=Range(min=0)
                ),
                "user_kills": fields.Int(
                    required=True, strict=True, validate=Range(min=0)
                ),
                "quests_complete": fields.Int(
                    required=True, strict=True, validate=Range(min=0)
                ),
                "dex": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "def": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "str": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "bonus_dex": fields.Int(
                    required=True, strict=True, validate=Range(min=0)
                ),
                "bonus_def": fields.Int(
                    required=True, strict=True, validate=Range(min=0)
                ),
                "bonus_str": fields.Int(
                    required=True, strict=True, validate=Range(min=0)
                ),
                "hp": fields.Int(required=True, strict=True, validate=Range(min=0)),
                "max_hp": fields.Int(required=True, strict=True, validate=Range(min=1)),
                "safeMode": fields.Bool(required=True),
                "safeModeTime": fields.DateTime(required=True, allow_none=True),
                "background": fields.Int(required=True, strict=True),
                "membership": fields.Bool(required=True),
                "guild": fields.Nested(PlayerGuildSchema, required=False),
            }
        )

        class GuildPlayerSchema(Schema):
            user_id = fields.Int(required=True, strict=True, validate=Range(min=1))
            position = fields.Str(required=True)
            name = fields.Str(required=True)
            level = fields.Int(required=True, strict=True, validate=Range(min=1))
            safe_mode = fields.Int(
                required=True, strict=True, validate=Range(min=0, max=1)
            )
            current_hp = fields.Int(required=True, strict=True, validate=Range(min=0))
            max_hp = fields.Int(required=True, strict=True, validate=Range(min=1))

        class PlayersSchema(OneOfSchema):
            type_schemas = {"error": ErrorSchema, "player": PlayerSchema}

            def get_data_type(self, data):
                return "error" if "error" in data else "player"

        class GuildsSchema(OneOfSchema):
            type_schemas = {"error": ErrorSchema, "guild": GuildPlayerSchema}

            def get_data_type(self, data):
                return "error" if "error" in data else "guild"

            def load(self, data, *, many=None, **kwargs):
                # in order to emulate nested GuildPlayerSchema
                # only edge case is a list of ErrorSchema
                is_list = isinstance(data, list)
                data = data if is_list else [data]
                result = super().load(data, many=True, **kwargs)
                result = result if is_list else result[0]
                return result

        class InputSchema(Schema):
            players = fields.Dict(
                keys=fields.Int(validate=Range(min=0)),
                values=fields.Nested(PlayersSchema),
                required=True,
            )
            guilds = fields.Dict(
                keys=fields.Int(validate=Range(min=0)),
                values=fields.Nested(GuildsSchema),
                required=True,
            )

        user = get_current_user()

        try:
            data = InputSchema().load(request.get_json())
        except ValidationError as e:
            return e.messages, 422

        submit_batch(user, data)

        db.session.commit()
        return {"message": "Batch successfully processed"}
