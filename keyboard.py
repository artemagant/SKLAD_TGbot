import telegram as tg
import telegram.ext as tgext
import math

import data as data

def get_under_construction_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Вернуться в главное меню", callback_data="return_main")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)


def get_main_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Склады", callback_data = "storage")],
        [tg.InlineKeyboardButton("Информация", callback_data="info")],
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_storage_menu():
    keyboard = [
        [
            tg.InlineKeyboardButton("Список", callback_data = "storage_list"),
            tg.InlineKeyboardButton("Добавить", callback_data = "add_storage")
        ],
        [tg.InlineKeyboardButton("Вернуться", callback_data = "return_main")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_info_menu():
    keyboard = [
        [
            tg.InlineKeyboardButton("Личная информация", callback_data = "info_user"),
            tg.InlineKeyboardButton("Информация бота", callback_data = "info_bot")
        ],
        [
            tg.InlineKeyboardButton("Вернуться", callback_data = "return_main")
        ]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_info_menu_admin():
    keyboard = [
        [tg.InlineKeyboardButton("Aдмин меню", callback_data = "admin_menu")],
        [
            tg.InlineKeyboardButton("Личная информация", callback_data = "info_user"),
            tg.InlineKeyboardButton("Информация бота", callback_data = "info_bot")
        ],
        [
            tg.InlineKeyboardButton("Вернуться", callback_data = "return_main")
        ]
    ]
    return tg.InlineKeyboardMarkup(keyboard)


#
# Storage
#

def get_add_storage_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Отменить", callback_data = "cancel_bot_creation")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_return_to_storage_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Вернуться", callback_data = "storage")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_successed_storage_creation_menu(storage_name, username):
    keyboard = [
        [tg.InlineKeyboardButton("Настроить склад", callback_data = f"configurestorage_{username["info"]["username"]}_{storage_name}")],
        [tg.InlineKeyboardButton("Вернуться", callback_data = "storage")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_storage_list_menu(user_data):
    storages = user_data.get("storages", {})
    storages_list = list(storages)
    storages_amount = len(storages)
    current_storage = 0
    keyboard = []

    for i in range(0, len(storages_list), 2):
        row = []
        storage_1 = storages_list[i]
        callback_1 = f"configurestorage_{user_data["info"]["username"]}_{storage_1}"
        row.append(tg.InlineKeyboardButton(storage_1, callback_data = callback_1))

        if i + 1 < len(storages_list):
            storage_2 = storages_list[i+1]
            callback_2 = f"configurestorage_{user_data["info"]["username"]}_{storage_2}"
            row.append(tg.InlineKeyboardButton(storage_2, callback_data = callback_2))
        keyboard.append(row)
    keyboard.append([tg.InlineKeyboardButton("Вернуться", callback_data = "storage")])
    return tg.InlineKeyboardMarkup(keyboard)

def get_storage_configure_menu(storage_name, user_data):
    username = user_data["info"]["username"]
    keyboard = [
        [tg.InlineKeyboardButton("Список предметов", callback_data = f"storageitems_{username}_{storage_name}")],
        [tg.InlineKeyboardButton("Информация", callback_data = f"storageinfo_{username}_{storage_name}"),
         tg.InlineKeyboardButton("Настройки", callback_data = f"storagesettings_{username}_{storage_name}")],
        [tg.InlineKeyboardButton("Вернуться", callback_data = f"configurestorage_{username}_{storage_name}")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)


#
# Admin
#

def get_admin_menu():
    keyboard = [
        [
            tg.InlineKeyboardButton("Дата юзера", callback_data = "admin_user_data"),
            #tg.InlineKeyboardButton("Дата", callback_data = "admin_data")
        ],
        [tg.InlineKeyboardButton("Вернуться", callback_data = "return_main")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_return_to_admin_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Вернуться", callback_data = "admin_menu")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)


def get_user_data_menu(username):
    keyboard = [
        [
            tg.InlineKeyboardButton("Удалить логи", callback_data = f"admindeletelogs_{username}")
        ],
        [
            tg.InlineKeyboardButton("Сбросить юзера", callback_data = f"adminresetuser_{username}"),
            tg.InlineKeyboardButton("Удалить юзера", callback_data = f"admindeleteuser_{username}")
        ],
        [tg.InlineKeyboardButton("Изменить admin. \nСделать админом или наоборот", callback_data = f"adminchangeadmin_{username}")],
        [tg.InlineKeyboardButton("Вернуться", callback_data = "admin_menu")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_create_default_user_data_menu(username):
    keyboard = [
        [
            tg.InlineKeyboardButton("Да", callback_data = f"yesforcreatedefaultuserdata_{username}"),
            tg.InlineKeyboardButton("Отмена", callback_data = "admin_menu")
        ]
    ]
    return tg.InlineKeyboardMarkup(keyboard)


