import json
from datetime import datetime, timezone, timedelta

utc_plus_4 = timezone(timedelta(hours = 4))

def load_data():
    data = None
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

def save_user_data(user_data: Dictionary):
    data = load_data()
    data[user_data["info"]["username"]] = user_data
    with open("data.json", "w") as file:
        json.dump(data, file, indent = 2)


def get_user_data(user: String):
    data = load_data()
    user_data = None
    try:
        user_data = data[user]
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
        },
        "Log": {}
    }
    return user

def write_to_log(user_data: Dictionary, log: String):
    current_time = datetime.now(utc_plus_4).strftime("%Y-%m-%d %H:%M:%S %z")
    user_data["Log"].setdefault(current_time, log)
    return user_data
