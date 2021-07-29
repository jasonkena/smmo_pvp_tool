from tqdm import tqdm
import json
import time
import requests

UID = 613732 # Enter your UID here
RATE_LIMIT = 40
API_KEY = "Copy your key from https://web.simple-mmo.com/p-api/home"
ACCESS_TOKEN = "welp"
BASE_URL = "http://127.0.0.1:5000"

def create_headers(token):
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


class PVPToolAPI:
    @staticmethod
    def login_status(token=None):
        headers = create_headers(token)
        r = requests.get(f"{BASE_URL}/api/login/status", headers=headers)
        r.raise_for_status()

        result = r.json()
        print(f"Logged in with id: {result['uid']}")
        return result

    @staticmethod
    def login_request(uid):
        r = requests.get(f"{BASE_URL}/api/login/{uid}")
        r.raise_for_status()

        result = r.json()
        print(f"Change motto to {result['motto']} to verify")
        print("https://web.simple-mmo.com/changemotto")
        return result

    @staticmethod
    def login_verify(verification_token):
        headers = create_headers(verification_token)
        r = requests.get(f"{BASE_URL}/api/login/verify", headers=headers)
        r.raise_for_status()

        result = r.json()
        print(f"Login success")
        return result

    @staticmethod
    def request_batch(access_token, num_tasks):
        headers = create_headers(access_token)
        r = requests.post(f"{BASE_URL}/api/batch/request", json = {"num_tasks": num_tasks}, headers=headers)
        r.raise_for_status()

        result = r.json()
        return result

    @staticmethod
    def submit_batch(access_token, data):
        headers = create_headers(access_token)
        r = requests.post(f"{BASE_URL}/api/batch/submit", headers=headers, json=data)
        r.raise_for_status()

        result = r.json()
        return result

    @staticmethod
    def create_job(access_token, guild_ids):
        headers = create_headers(access_token)
        r = requests.post(f"{BASE_URL}/api/job/create", headers=headers, json={"guild_ids": guild_ids})
        r.raise_for_status()

        result = r.json()
        print(f"Job {result['job_id']} with {result['num_tasks']} tasks has been created")
        return result

    @staticmethod
    def get_job(access_token, job_id):
        headers = create_headers(access_token)
        r = requests.get(f"{BASE_URL}/api/job/{job_id}", headers=headers)
        r.raise_for_status()

        result = r.json()
        print(f"Job {result['job_id']} has {result['num_tasks']} tasks; completed: {result['is_completed']}")
        return result

    @staticmethod
    def query(access_token, num_results, guild_ids=None, maximum_level=None, minimum_gold=None, player_blacklist=None, guild_blacklist=None, last_update=None, sort_by=None):
        data = {"num_results":num_results, "guild_ids":guild_ids, "maximum_level":maximum_level, "minimum_gold":minimum_gold, "player_blacklist":player_blacklist, "guild_blacklist":guild_blacklist, "last_update":last_update, "sort_by":sort_by}
        data = {k:v for (k,v) in data.items() if v is not None}

        headers = create_headers(access_token)
        r = requests.post(f"{BASE_URL}/api/query/submit", headers=headers, json=data)
        r.raise_for_status()

        result = r.json()
        return result


class PVPClient:
    def get_user(self, user_id):
        r = requests.post(
            f"https://api.simple-mmo.com/v1/player/info/{user_id}",
            data={"api_key": API_KEY},
        )
        r.raise_for_status()

        result = r.json()

        time.sleep(60 / RATE_LIMIT)
        return r.json()


    def get_guild(self, guild_id):
        # return list of users
        r = requests.post(
            f"https://api.simple-mmo.com/v1/guilds/members/{guild_id}",
            data={"api_key": API_KEY},
        )
        r.raise_for_status()

        result = r.json()

        time.sleep(60 / RATE_LIMIT)
        return r.json()

    def process_tasks(self, tasks):
        result = {"players": {}, "guilds":{}}
        for task in tqdm(tasks):
            if task["is_player_task"]:
                result["players"][task["uid"]] = self.get_user(task["uid"])
            else:
                result["guilds"][task["uid"]] = self.get_guild(task["uid"])
        return result


def main():
    client = PVPClient()
    a = PVPToolAPI.login_status(ACCESS_TOKEN)

if __name__ == "__main__":
    main()
