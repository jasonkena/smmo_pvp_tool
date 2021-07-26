from datetime import timedelta


class Config(object):
    ADMIN_UIDS = [613732]
    # https://web.simple-mmo.com/town-hall/stats
    # NOTE: ALWAYS ROUND DOWN
    NUM_PLAYERS = 615000

    SECRET_KEY = (
        b"***REMOVED***"
    )
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + "smmo:smmo@localhost" + "/data"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # used to query levels and authentication
    SMMO_SERVER_API_KEY = "***REMOVED***"

    # if True, performing a query reduces balance
    ENFORCE_BALANCE = False
    QUERY_BALANCE_COST = 2
    # duration required for task assignment to be considered obsolete
    CLEAN_TASKS_DELTA = timedelta(minutes=5)

    LOGIN_REQUEST_MOTTO_LENGTH = 6
    LOGIN_REQUEST_DELTA = timedelta(minutes=5)
    HIT_DELTA = timedelta(minutes=5)
    HIT_URL = "https://web.simple-mmo.com/user/attack/"
    # login expiry (set to False for no delta)
    LOGIN_DELTA = False
    BYPASS_MOTTO_CHECK = False

    MAX_BATCH_SIZE = 60
    # number of guilds
    MAX_JOB_GUILDS = 20
    MAX_QUERY_RESULTS = 50

    CLIENT_CONFIG = {
        "BATCH_SIZE": 5,
        "SMMO_DELAY": (60 / 40) * 1000,
        "API_DELAY": 1000,
        "AJAX_TIMEOUT": 10000,
    }


class ProductionConfig(Config):
    SQLALCHEMY_ECHO = False
    BYPASS_MOTTO_CHECK = False
    ENFORCE_BALANCE = True
