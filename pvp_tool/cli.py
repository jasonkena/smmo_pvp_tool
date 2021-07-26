from flask.cli import AppGroup
from pvp_tool.utils import db
from pvp_tool.models import create_cache as models_create_cache

app_cli = AppGroup("cli")


@app_cli.command()
def init_db():
    """Initialize database"""
    db.create_all()
    models_create_cache()
    db.session.commit()


@app_cli.command()
def create_cache():
    """Create PlayerCache"""
    models_create_cache()
    db.session.commit()


@app_cli.command()
def drop_all():
    """Drop all tables"""
    db.drop_all()
