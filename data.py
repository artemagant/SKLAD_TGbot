import json
from datetime import datetime, timezone, timedelta

utc_plus_4 = timezone(timedelta(hours = 4))

def load_data():
    data = None
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

def save_user_data(user_data):
    data = load_data()
    if (isinstance(user_data, str)):
        data[user_data] = None
    else:
        data[user_data["info"]["username"]] = user_data
    with open("data.json", "w") as file:
        json.dump(data, file, indent = 2)


def get_user_data(username: String):
    data = load_data()
    user_data = None
    try:
        user_data = data[username]
    except KeyError:
        return None
    return user_data

def get_default_user(username: String):
    user = {
        "storages": {
        },
        "info": {
            "username": username,
            "admin": False,
            "state": None,
        },
        "Log": {}
    }
    return user


#
# Storage
#

def get_default_storage(storage_name):
    return {
        "storage":{},
        "info": {
            "name": storage_name
        }
    }

def create_storage(user_data, storage_name):
    storages = user_data.get("storages", {})
    if (storages.get(storage_name, None)):
        return 1
    storages[storage_name] = get_default_storage(storage_name)
    user_data["storages"] = storages
    save_user_data(user_data)
    return 0


#
# Admin
#

def delete_user_data(username):
    data = load_data()
    data[username] = username
    save_user_data(data[username])

def delete_logs_user(username):
    data = load_data()
    data[username]["Log"] = {}
    save_user_data(data[username])

def change_admin(username):
    data = load_data()
    data[username]["info"]["admin"] = not data[username]["info"]["admin"]
    save_user_data(data[username])


def write_to_log(user_data: Dictionary, log: String):
    current_time = datetime.now(utc_plus_4).strftime("%Y-%m-%d %H:%M:%S %z")
    user_data["Log"].setdefault(current_time, log)
    save_user_data(user_data)
    return user_data

def get_state(username):
    user_data = get_user_data(username)
    return user_data["info"]["state"] 

def set_state(username, state):
    user_data = get_user_data(username)
    user_data["info"]["state"] = state
    save_user_data(user_data)

