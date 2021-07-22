from pvp_tool.utils import db, jwt
from pvp_tool.models import User
from flask_jwt_extended import get_jwt_identity


def get_user(uid):
    assert uid > -1
    # will create the user if it does not already exist
    user = db.session.get(User, uid)
    if not user:
        user = User(uid=uid, balance=0)
        db.session.add(user)
    return user


def get_user_balance(user):
    return user.balance


def get_current_user():
    return get_user(get_jwt_identity())
