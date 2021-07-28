from pvp_tool.utils import db


class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_uid = db.Column(db.ForeignKey("player.uid"), nullable=False)
    user_uid = db.Column(db.ForeignKey("user.uid"), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)

    player = db.relationship("Player", uselist=False)
    user = db.relationship("User", uselist=False, back_populates="hits")

    def __repr__(self):
        return f'<Hit (player={self.player}, user="{self.user}", timestamp="{self.timestamp}")>'
