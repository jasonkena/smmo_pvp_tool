from math import ceil
from time import time
import sqlalchemy as sa
from flask import current_app
from pvp_tool.utils import db
from pvp_tool.models import Task, Player, PlayerCache, create_cache
from pvp_tool.actions.task import get_task


def mining(num_targets):
    num_new = ceil(current_app.config["NEW_MINING_RATIO"] * num_targets)
    new_targets = new_mining(num_new)
    old_targets = old_mining(num_targets - len(new_targets))
    return new_targets + old_targets


def new_mining(num_targets):
    # choose untouched uids
    uids = db.session.query(PlayerCache.uid).filter(
        PlayerCache.player == None,
        PlayerCache.task == None,
        PlayerCache.pending_task == None,
    )
    if current_app.config["RANDOMIZE_NEW_MINING"]:
        uids = uids.order_by(db.func.random())
    uids = uids.limit(num_targets).all()

    return [get_task(uid[0], True) for uid in uids]


def old_mining(num_targets):
    # https://stackoverflow.com/questions/1398113/how-to-select-one-row-randomly-taking-into-account-a-weight
    value = (
        (1 - db.func.random()) if current_app.config["RANDOMIZE_OLD_MINING"] else 0.5
    )
    # join because https://stackoverflow.com/questions/16589208/attributeerror-while-querying-neither-instrumentedattribute-object-nor-compa
    uids = (
        db.session.query(PlayerCache.uid)
        .filter(
            PlayerCache.player != None,
            PlayerCache.task == None,
            PlayerCache.pending_task == None,
        )
        .join(Player)
        .filter(Player.invalid == False)
        .order_by(
            # add factor based on time difference
            -db.func.log(value)
            / (
                Player.weight
                + current_app.config["BASE_WEIGHT"]
                + (time() - sa.extract("epoch", Player.timestamp))
                / current_app.config["AGE_FACTOR"].total_seconds()
            )
        )
        .limit(num_targets)
        .all()
    )
    return [get_task(uid[0], True) for uid in uids]
