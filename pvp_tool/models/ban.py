from pvp_tool.utils import db


class Ban(db.Model):
    player_id = db.Column(db.ForeignKey("playercache.uid"), primary_key=True, nullable=False)
    user_id = db.Column(db.ForeignKey("user.uid"), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<Ban (player_id={self.player_id}, user_id={self.user_id})>"
