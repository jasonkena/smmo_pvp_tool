from flask import current_app
from pvp_tool.utils import db


class PlayerCache(db.Model):
    __tablename__ = "playercache"
    uid = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    player = db.relationship("Player", uselist=False, viewonly=True)
    task = db.relationship(
        "Task",
        uselist=False,
        viewonly=True,
        primaryjoin="and_(PlayerCache.uid==Task.uid, Task.is_player_task)",
    )
    pending_task = db.relationship(
        "PendingTask",
        uselist=True,
        viewonly=True,
        primaryjoin="and_(PlayerCache.uid==PendingTask.uid, PendingTask.is_player_task)",
    )
    bans = db.relationship("Ban", uselist=True, viewonly=True)

    def __repr__(self):
        return f'<PlayerCache (uid={self.uid}, player="{self.player}", task="{self.task}", pending_task="{pending_task}")>'


def create_cache(max_value=None):
    # will update pre-existing cache
    min_value = db.session.query(PlayerCache).count() + 1
    if max_value is None:
        max_value = current_app.config["NUM_PLAYERS"]
    if min_value >= max_value:
        return

    # https://stackoverflow.com/a/21426929/10702372
    SQL_STRING = """WITH RECURSIVE uids AS (
    SELECT :min_value AS num
    UNION ALL
    SELECT num+1 FROM uids WHERE num+1<=:max_value
)
INSERT INTO playercache (uid) SELECT uids.num FROM uids"""
    SQL_STRING = db.text(SQL_STRING)
    result = db.session.execute(
        SQL_STRING, {"min_value": min_value, "max_value": max_value}
    )
