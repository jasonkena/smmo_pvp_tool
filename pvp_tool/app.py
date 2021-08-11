from flask import Flask, render_template, current_app, request

from pvp_tool.utils import db, jwt, api, migrate
from pvp_tool.resources import api_bp
from pvp_tool.cli import app_cli


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("prod_config.ProductionConfig")

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api_bp)
    app.cli.add_command(app_cli)

    @app.route("/")
    def client():
        client_config = current_app.config["CLIENT_CONFIG"].copy()
        client_config["SERVER_URL"] = request.url_root
        return render_template("content.html", CLIENT_CONFIG=client_config)

    @app.route("/pvptool.user.js")
    def tool_userscript():
        return render_template("pvptool.user.js", SERVER_URL=request.url_root)

    @app.route("/pointslistener.user.js")
    def points_userscript():
        return render_template("pointslistener.user.js", SERVER_URL=request.url_root)

    return app
