from pvp_tool.utils import db

association_table = db.Table(
    "association",
    db.metadata,
    db.Column("job_id", db.Integer, db.ForeignKey("job.id")),
    db.Column("task_uid", db.Integer),
    db.Column("task_type", db.Boolean),
    db.ForeignKeyConstraint(
        ("task_uid", "task_type"), ("task.uid", "task.is_player_task")
    ),
)
