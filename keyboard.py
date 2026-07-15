import telegram as tg
import telegram.ext as tgext


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
        [tg.InlineKeyboardButton("Добавить склад", callback_data = "add_storage")],
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


def get_add_storage_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Отменить", callback_data = "cancel_bot_creation")]
    ]
    return tg.InlineKeyboardMarkup(keyboard)

def get_admin_menu():
    keyboard = [
        [
            tg.InlineKeyboardButton("Дата юзера", callback_data = "admin_user_data"),
            tg.InlineKeyboardButton("Дата", callback_data = "admin_data")
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
            tg.InlineKeyboardButton("Посмотреть логи", callback_data = f"adminseelogs_{username}"),
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


