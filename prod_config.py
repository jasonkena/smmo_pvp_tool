from config import Config


class ProductionConfig(Config):
    SECRET_KEY = "production-secret-key"
    SMMO_SERVER_API_KEY = "production-api-key"
