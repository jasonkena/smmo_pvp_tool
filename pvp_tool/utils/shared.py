from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
api = Api()
migrate = Migrate()
