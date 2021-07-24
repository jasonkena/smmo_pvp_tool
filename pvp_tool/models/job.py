from pvp_tool.utils import db
from pvp_tool.models.association_table import association_table


class Job(db.Model):
    # level of the user will be extracted by the server at query time, not on the user side
    id = db.Column(db.Integer, primary_key=True)

    # many to one
    creating_user = db.relationship("User", back_populates="jobs", uselist=False)
    creating_user_uid = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=False)
    created_timestamp = db.Column(db.DateTime(timezone=True), nullable=False)

    tasks = db.relationship("Task", back_populates="jobs", secondary=association_table)

    def __repr__(self):
        return f"<Job (id={self.id}, balance={self.balance})>"
