from datetime import timedelta


class Config(object):
    ADMIN_UIDS = [613732]
    # https://web.simple-mmo.com/town-hall/stats
    # NOTE: ALWAYS ROUND DOWN
    NUM_PLAYERS = 615000

    # Generate one with os.urandom(24).hex()
    SECRET_KEY = "secret-key"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + "smmo:smmo@localhost" + "/data"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # used to query levels and authentication
    SMMO_SERVER_API_KEY = "api-key"

    # if True, performing a query reduces balance
    ENFORCE_BALANCE = True
    QUERY_BALANCE_COST = 2
    # duration required for task assignment to be considered obsolete
    CLEAN_TASKS_DELTA = timedelta(minutes=5)

    LOGIN_REQUEST_MOTTO_LENGTH = 6
    LOGIN_REQUEST_DELTA = timedelta(minutes=5)
    # Hit URL expiry
    HIT_DELTA = timedelta(minutes=5)
    HIT_URL = "https://web.simple-mmo.com/user/attack/"
    # Time after hit when pending task should be scheduled
    HIT_REFRESH_DELTA = timedelta(minutes=2)

    # login expiry (set to False for no delta)
    LOGIN_DELTA = False
    BYPASS_MOTTO_CHECK = False

    MAX_BATCH_SIZE = 60
    # number of guilds
    MAX_JOB_GUILDS = 20
    MAX_QUERY_RESULTS = 50

    # % of mining tasks allocated to unregistered uids
    NEW_MINING_RATIO = 0.8
    RANDOMIZE_NEW_MINING = True
    RANDOMIZE_OLD_MINING = True
    # cache future mining results
    MINING_BUFFER = 100

    # required time to halve additional weight
    DECAY_TIME = timedelta(weeks=1)
    BASE_WEIGHT = 1.0

    # create a new task for a player when processed (when health < 0.5)
    REFRESH_PLAYER = True

    NUM_LEADERBOARD = 20

    CLIENT_CONFIG = {
        "BATCH_SIZE": 10,
        "SMMO_DELAY": (60 / 40) * 1000,
        "API_DELAY": 1000,
        "AJAX_TIMEOUT": 30000,
        # for access_token and form settings
        "COOKIE_EXPIRY": 365,
    }
