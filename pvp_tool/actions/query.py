from datetime import datetime, timezone, timedelta
from flask import current_app
from pvp_tool.utils import db
from pvp_tool.models import Player, PlayerCache
from pvp_tool.actions import generate_player_blacklist, clean_hits


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
    clean_hits()
    player_blacklist.extend(generate_player_blacklist(user))
    player_blacklist.append(user.uid)

    # +1 in denominator because of UID 69882
    query = (
        db.session.query(Player)
        .join(PlayerCache)
        .filter(
            PlayerCache.bans == None,
            # if a player has a pending refresh, do not show it as a result
            PlayerCache.task == None,
            PlayerCache.pending_task == None,
            Player.invalid == False,
            (Player.hp + 0.0) / (Player.max_hp + 1) >= 0.5,
            Player.safeMode == False,
        )
    )
    if guild_ids:
        query = query.filter(Player.guild_id.in_(guild_ids))

    query = query.filter(Player.level <= maximum_level)
    if maximum_level >= 200:
        query = query.filter(Player.level >= 200)
    elif maximum_level >= 100:
        query = query.filter(Player.level >= 100)

    query = query.filter(Player.gold >= minimum_gold)
    query = query.filter(~Player.uid.in_(player_blacklist))
    query = query.filter(
        (Player.guild_id == None) | (~Player.guild_id.in_(guild_blacklist))
    )
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
    user.balance -= len(results) * current_app.config["QUERY_BALANCE_COST"]

    return results
