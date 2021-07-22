from flask import Flask

from pvp_tool.utils import db, jwt, api
from pvp_tool.resources import api_bp


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api_bp)

    @app.cli.command("init-db")
    def init_db():
        """Initialize database"""
        db.create_all()

    @app.route("/")
    def hello_world():
        return "hi"

    return app
