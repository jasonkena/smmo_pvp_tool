from pvp_tool.utils import db
from pvp_tool.models import Ban, Player


def ban_player(user, player_id):
    assert db.session.get(Player, player_id) is not None
    # tuple because composite primary task
    key = {"player_id": player_id, "user_id": user.uid}
    ban = db.session.get(Ban, key)
    if not ban:
        ban = Ban(**key)
        db.session.add(ban)
    return ban
