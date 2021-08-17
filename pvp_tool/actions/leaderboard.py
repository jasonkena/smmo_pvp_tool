from flask import current_app
from pvp_tool.utils import db
from pvp_tool.models import User


def get_leaderboard():
    return (
        db.session.query(User)
        .order_by(User.balance.desc())
        .limit(current_app.config["NUM_LEADERBOARD"])
        .all()
    )
