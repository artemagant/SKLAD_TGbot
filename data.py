import json
from datetime import datetime, timezone, timedelta

utc_plus_4 = timezone(timedelta(hours = 4))

def load_data():
    data = None
    with open("data.json", "r", encoding = "utf-8") as file:
        data = json.load(file)
    return data

def save_data(data):
    with open("data.json", "w", encoding = "utf-8") as file:
        json.dump(data, file, ensure_ascii = False, indent = 4)

def save_user_data(user_data):
    data = load_data()
    if (isinstance(user_data, str)):
        data[user_data] = None
    else:
        data[user_data["info"]["username"]] = user_data
    with open("data.json", "w", encoding = "utf-8") as file:
        json.dump(data, file, ensure_ascii = False, indent = 4)


def get_user_data(username):
    data = load_data()
    user_data = None
    try:
        user_data = data[username]
    except KeyError:
        return None
    return user_data

def get_default_user(username):
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
            "name": storage_name,
            "description": None,
            "date_creating": datetime.now(utc_plus_4).strftime("%Y-%m-%d %H:%M:%S"),
            "level": 0
        }
    }

def get_default_item(item_name):
    return {
        "name": item_name,
        "description": None,
        "place": None,
        "amount": 0,
        "date_creating": datetime.now(utc_plus_4).strftime("%Y-%m-%d %H:%M:%S")
    }

def create_storage(user_data, storage_name):
    storages = user_data.get("storages", {})
    if (storages.get(storage_name, None)):
        return 1
    storages[storage_name] = get_default_storage(storage_name)
    user_data["storages"] = storages
    save_user_data(user_data)
    return 0

def reset_storage(user_data, storage_name):
    storage_data = get_storage_data(user_data, storage_name)
    storage_data = get_default_storage(storage_name)
    user_data["storages"][storage_name] = storage_data
    save_user_data(user_data)

def delete_storage(user_data, storage_name):
    storage_data = get_storage_data(user_data, storage_name)
    del user_data["storages"][storage_name]
    save_user_data(user_data)
    return user_data

def create_item(user_data, storage_name, item_name):
    storage_itemes = user_data["storages"][storage_name]["storage"]
    storage_itemes[item_name] = get_default_item(item_name)
    user_data["storages"][storage_name]["storage"] = storage_itemes
    save_user_data(user_data)
    return user_data

def get_storage_data(user_data, storage_name):
    return user_data["storages"][storage_name]

def get_item_data(user_data, storage_name, item_name):
    return user_data["storages"][storage_name]["storage"][item_name]

def change_storage_name(user_data, storage_name, new_storage_name):
    storage_data = get_storage_data(user_data, storage_name)
    user_data["storages"][new_storage_name] = user_data["storages"].pop(storage_name)
    save_user_data(user_data)
    return user_data

def change_item_name(user_data, storage_name, item_name, new_item_name):
    user_data["storages"][storage_name]["storage"][new_item_name] = user_data["storages"][storage_name]["storage"].pop(item_name)
    save_user_data(user_data)

def change_storage_description(user_data, storage_name, new_storage_description):
    user_data["storages"][storage_name]["info"]["description"] = new_storage_description
    save_user_data(user_data)
    return user_data

def change_item_description(user_data, storage_name, item_name, new_item_description):
    user_data["storages"][storage_name]["storage"][item_name]["description"] = new_item_description
    save_user_data(user_data)

def change_item_place(user_data, storage_name, item_name, new_item_place):
    user_data["storages"][storage_name]["storage"][item_name]["place"] = new_item_place
    save_user_data(user_data)

def change_item_amount(user_data, storage_name, item_name, new_item_amount):
    user_data["storages"][storage_name]["storage"][item_name]["amount"] = int(new_item_amount)
    save_user_data(user_data)

def delete_item(user_data, storage_name, item_name):
    del user_data["storages"][storage_name]["storage"][item_name]
    save_user_data(user_data)

#
# Admin
#

def delete_user_data(username):
    data = load_data()
    del data[username]
    save_data(data)

def delete_logs_user(username):
    data = load_data()
    data[username]["Log"] = {}
    save_user_data(data[username])

def change_admin(username):
    data = load_data()
    data[username]["info"]["admin"] = not data[username]["info"]["admin"]
    save_user_data(data[username])


def write_to_log(user_data, log):
    current_time = datetime.now(utc_plus_4).strftime("%Y-%m-%d %H:%M:%S")
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

