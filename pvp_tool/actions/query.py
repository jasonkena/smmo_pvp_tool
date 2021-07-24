from flask import current_app
from datetime import datetime, timezone, timedelta
from pvp_tool.utils import db
from pvp_tool.models import Player


def process_query(
    user,
    num_results,
    guild_ids,
    maximum_level,
    minimum_gold,
    player_blacklist,
    guild_blacklist,
    last_update,
    sort_by,
):
    # NOTE TODO ownership

    player_blacklist.append(user.uid)

    query = db.session.query(Player).filter(
        Player.invalid == False,
        (Player.hp + 0.0) / Player.max_hp > 0.5,
        Player.safeMode == False,
    )
    if guild_ids:
        query = query.filter(Player.guild_id.in_(guild_ids))

    query = query.filter(Player.level <= maximum_level)
    if maximum_level >= 100:
        query = query.filter(Player.level >= 100)

    query = query.filter(Player.gold >= minimum_gold)
    query = query.filter(~Player.uid.in_(player_blacklist))
    query = query.filter(~Player.guild_id.in_(guild_blacklist))
    if last_update:
        query = query.filter(
            Player.timestamp
            > (datetime.now(timezone.utc) - timedelta(minutes=last_update))
        )

    if sort_by == "gold":
        query = query.order_by(Player.gold.desc())
    elif sort_by == "level":
        query = query.order_by(Player.level.desc())
    elif sort_by == "last_update":
        query = query.order_by(Player.timestamp.desc())

    results = query.limit(num_results).all()
    user.balance -= len(results)

    return results
