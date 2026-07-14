import telegram as tg
import telegram.ext as tgext


def get_under_construction_menu():
    keyboard = [
        [tg.InlineKeyboardButton("Вернуться в главное меню", callback_data="return")]
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
        [tg.InlineKeyboardButton("Добавить склад", callback_data="add_storage")],
        [tg.InlineKeyboardButton("Вернуться", callback_data="return")]

    ]
    return tg.InlineKeyboardMarkup(keyboard)
