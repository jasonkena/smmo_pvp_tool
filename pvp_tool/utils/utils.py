import requests
from flask import current_app


def server_get_user(uid):
    r = requests.post(
        f"https://api.simple-mmo.com/v1/player/info/{uid}",
        data={"api_key": current_app.config["SMMO_SERVER_API_KEY"]},
    )
    r.raise_for_status()

    result = r.json()
    if "error" in result:
        # Unprocessable Entity
        abort(422, description=f"Player {uid} does not exist")
    return result
