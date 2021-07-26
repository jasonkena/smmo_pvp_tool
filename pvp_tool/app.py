from flask import Flask, render_template

from pvp_tool.utils import db, jwt, api
from pvp_tool.resources import api_bp
from pvp_tool.cli import app_cli


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api_bp)
    app.cli.add_command(app_cli)

    @app.route("/")
    def client():
        return render_template("content.html")

    return app
