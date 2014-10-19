from os import path
import json
import apps
import levels
import users

SINCE_ID_FILE = path.join(path.dirname(__file__), '..', '..', 'data/since/since_ids.json')

def save_since_id(user, _id):
    with open(SINCE_ID_FILE, 'r') as f:
        ids = json.load(f)

    ids[user] = str(_id)

    with open(SINCE_ID_FILE, 'w') as f:
        json.dump(ids, f)

def since_id(user):
    with open(SINCE_ID_FILE, 'r') as f:
        ids = json.load(f)

    return ids[user]

