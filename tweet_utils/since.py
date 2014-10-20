from os import path
import config
import json

SINCE_ID_FILE = None


def _set_path():
    global SINCE_ID_FILE
    if SINCE_ID_FILE is None:
        config.load_config()

        pth = config.config['since_id_file'].format(data_path=config.config['data_path'])

        SINCE_ID_FILE = path.join(path.expanduser(pth))


def save_since_id(user, _id):
    _set_path()

    with open(SINCE_ID_FILE, 'r') as f:
        ids = json.load(f)

    ids[user] = str(_id)

    with open(SINCE_ID_FILE, 'w') as f:
        json.dump(ids, f)


def since_id(user):
    _set_path()
    with open(SINCE_ID_FILE, 'r') as f:
        ids = json.load(f)

    return ids[user]
