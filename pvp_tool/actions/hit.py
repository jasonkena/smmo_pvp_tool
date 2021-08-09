from flask import current_app
from pvp_tool.utils import db, flatten
from pvp_tool.models import Player, Hit
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta, timezone
from pvp_tool.actions.task import get_task, create_pending_task


def hit(user, target_id):
    # create a pending task target player, update player weight, create a Hit object
    create_pending_task(
        target_id,
        True,
        datetime.now(timezone.utc) + current_app.config["HIT_REFRESH_DELTA"],
    )

    player = db.session.get(Player, target_id)
    assert player is not None

    player.weight += 1.0
    db.session.add(Hit(player=player, user=user, timestamp=datetime.now(timezone.utc)))


def generate_player_blacklist(user):
    # https://dba.stackexchange.com/questions/54187/select-rows-where-column-contains-same-data-in-more-than-one-record
    base_query = (
        db.session.query(Hit.player_uid)
        .group_by(Hit.player_uid)
        .filter(Hit.user == user)
    )

    # 3x limit within last 12 hours
    three_query = base_query.filter(
        Hit.timestamp > (datetime.now(timezone.utc) - timedelta(hours=12))
    ).having(db.func.count("*") >= 3)
    four_query = base_query.filter(
        Hit.timestamp > (datetime.now(timezone.utc) - timedelta(hours=24))
    ).having(db.func.count("*") >= 4)

    return list(set(flatten(three_query.all() + four_query.all())))


def create_hit_token(user, target_id):
    data = {"uid": user.uid, "target": target_id}
    access_token = create_access_token(
        -1,
        fresh=False,
        expires_delta=current_app.config["HIT_DELTA"],
        additional_claims={"hit_data": data},
    )
    return access_token


def clean_hits():
    db.session.query(Hit).filter(
        Hit.timestamp < (datetime.now(timezone.utc) - timedelta(days=1))
    ).delete()
