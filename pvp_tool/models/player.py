from datetime import datetime, timezone
from pvp_tool.utils import db


class Player(db.Model):
    uid = db.Column(
        db.ForeignKey("playercache.uid"), primary_key=True, nullable=False, index=True
    )
    invalid = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    # edge case because of Mike: UID 1
    motto = db.Column(
        db.String(200), nullable=False
    )  # as specified on https://web.simple-mmo.com/diamondstore/membership
    profile_number = db.Column(db.String(4), nullable=False)
    exp = db.Column(db.BigInteger, nullable=False)
    gold = db.Column(db.BigInteger, nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    npc_kills = db.Column(db.Integer, nullable=False)
    user_kills = db.Column(db.Integer, nullable=False)
    quests_complete = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    bonus_dex = db.Column(db.Integer, nullable=False)
    bonus_def = db.Column(db.Integer, nullable=False)
    bonus_str = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    safeMode = db.Column(db.Boolean, nullable=False)
    safeModeTime = db.Column(db.DateTime(timezone=True), nullable=True)
    background = db.Column(db.Integer, nullable=False)
    membership = db.Column(db.Boolean, nullable=False)
    guild_id = db.Column(db.Integer, nullable=True)
    guild_name = db.Column(db.String(), nullable=True)

    # New fields added in November 10 update
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False)
    reputation = db.Column(db.Integer, nullable=False)
    tasks_completed = db.Column(db.Integer, nullable=False)
    bounties_completed = db.Column(db.Integer, nullable=False)
    chests_opened = db.Column(db.Integer, nullable=False)
    dailies_unlocked = db.Column(db.Integer, nullable=False)
    avatar = db.Column(db.String(), nullable=False)
    market_trades = db.Column(db.Integer, nullable=False)
    last_activity = db.Column(db.DateTime(timezone=True), nullable=False)
    boss_kills = db.Column(db.Integer, nullable=False)

    # New fields added in December 13 update
    location_id = db.Column(db.Integer, nullable=False)
    location_name = db.Column(db.String(), nullable=False)

    # New fields added in February 7 update
    quests_performed = db.Column(db.Integer, nullable=False)

    banned = db.Column(db.Boolean, nullable=False)

    # cache = db.relationship("PlayerCache", uselist=False, viewonly=True)
    # player who scanned
    # many to one
    user = db.relationship("User", uselist=False)
    user_uid = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Player (uid={self.uid}, name="{self.name}", level={self.level}, guild="{self.guild_name}")>'


"""
Guild member example
{'id': 613732, 'name': 'RevoGen', 'level': 430, 'motto': "Stepping like there's no tomorrow.", 'profile_number': '9089', 'exp': 4616629, 'gold': 1966, 'steps'
: 5291, 'npc_kills': 1146, 'user_kills': 0, 'quests_complete': 588, 'dex': 475, 'def': 53, 'str': 267, 'bonus_dex': 0, 'bonus_def': 1059, 'bonus_str': 1075, '
hp': 2225, 'max_hp': 2225, 'safeMode': 1, 'safeModeTime': '2021-07-16 16:25:49', 'background': 102, 'membership': 0, 'guild': {'id': 474, 'name': 'The Forest'
}}

Guildless example
{'id': 616747, 'name': 'LostPleaseFound', 'level': 4, 'motto': 'There is no motto for this player.', 'profile_number': '7810', 'exp': 319, 'gold': 3208, 'step
s': 90, 'npc_kills': 8, 'user_kills': 0, 'quests_complete': 0, 'dex': 10, 'def': 5, 'str': 6, 'bonus_dex': 0, 'bonus_def': 4, 'bonus_str': 60, 'hp': 89, 'max_
hp': 95, 'safeMode': 0, 'safeModeTime': None, 'background': 102, 'membership': 0}

Guild example
[{'user_id': 270524, 'position': 'Leader', 'name': 'Tilphia', 'level': 50099, 'safe_mode': 0, 'current_hp': 25282, 'max_hp': 250540}, {'user_id': 336301, 'position': 'Member', 'name': 'JackKai', 'level': 126456, 'safe_mode': 0, 'current_hp': 658920, 'max_hp': 632355}, {'user_id': 347372, 'position': 'Member', 'name': 'iTrippaz', 'level': 4994, 'safe_mode': 0, 'current_hp': 7542, 'max_hp': 25145}]
"""

# missing guild & uid
NULL_MAPPING = {
    "invalid": True,
    "name": "",
    "level": -1,
    "motto": "",
    "profile_number": "",
    "exp": -1,
    "gold": -1,
    "steps": -1,
    "npc_kills": -1,
    "user_kills": -1,
    "quests_complete": -1,
    "dexterity": -1,
    "defense": -1,
    "strength": -1,
    "bonus_dex": -1,
    "bonus_def": -1,
    "bonus_str": -1,
    "hp": -1,
    "max_hp": -1,
    "safeMode": False,
    "safeModeTime": None,
    "background": -1,
    "membership": False,
    "creation_date": datetime.min.replace(tzinfo=timezone.utc),
    "reputation": 0,
    "tasks_completed": -1,
    "bounties_completed": -1,
    "chests_opened": -1,
    "dailies_unlocked": -1,
    "avatar": "",
    "market_trades": -1,
    "last_activity": datetime.min.replace(tzinfo=timezone.utc),
    "boss_kills": -1,
    "location_id": -1,
    "location_name": "",
    "quests_performed": -1,
    "banned": False,
}


KEY_MAPPING = {"id": "uid", "dex": "dexterity", "def": "defense", "str": "strength"}


def update_keys(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        new_key = KEY_MAPPING[key] if key in KEY_MAPPING else key
        new_dict[new_key] = value
    return new_dict


def parse_player_json(dictionary):
    # takes JSON input of user and converts it to kwargs for Player constructor
    # NOTE: user and timestamp to be handled later
    # NOTE: uid here is not used, will be overwritten in process_task_result to handle error case where uid is undefined

    if "error" in dictionary:
        return NULL_MAPPING

    updated_dict = update_keys(dictionary)
    updated_dict["invalid"] = False
    if updated_dict["profile_number"] is None:
        updated_dict["profile_number"] = ""

    if "guild" in updated_dict:
        updated_dict["guild_name"] = updated_dict["guild"]["name"]
        updated_dict["guild_id"] = updated_dict["guild"]["id"]
        updated_dict.pop("guild")

    updated_dict["last_activity"] = datetime.utcfromtimestamp(
        updated_dict["last_activity"]
    )

    updated_dict["location_id"] = updated_dict["current_location"]["id"]
    updated_dict["location_name"] = updated_dict["current_location"]["name"]
    updated_dict.pop("current_location")

    return updated_dict
