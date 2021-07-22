from pvp_tool.utils import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    # level of the user will be extracted by the server at query time, not on the user side
    tasks = db.relationship("Task", back_populates="assigned_user")
    # one to many
    jobs = db.relationship("Job", back_populates="creating_user")

    balance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Player (uid={self.uid}, balance={self.balance})>"
