from pvp_tool.utils import db
from pvp_tool.models.association_table import association_table


class Task(db.Model):
    # composite primary key, in order to separate uids between guilds and players
    # target player/guild
    uid = db.Column(db.ForeignKey("playercache.uid"), primary_key=True, nullable=False)
    # player task vs guild task
    is_player_task = db.Column(db.Boolean, primary_key=True, nullable=False)

    # many to one
    assigned_user = db.relationship("User", back_populates="tasks", uselist=False)
    assigned_user_uid = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=True)
    assigned_timestamp = db.Column(db.DateTime(timezone=True), nullable=True)

    jobs = db.relationship("Job", back_populates="tasks", secondary=association_table)

    def __repr__(self):
        return f"<Task (uid={self.uid}, is_player_task={self.is_player_task})>"


class PendingTask(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.ForeignKey("playercache.uid"), nullable=False)
    is_player_task = db.Column(db.Boolean, nullable=False)

    due_timestamp = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f"<PendingTask (id={self.id}, uid={self.uid}, is_player_task={self.is_player_task})>"
