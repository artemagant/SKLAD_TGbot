import telegram as tg
import telegram.ext as tgext

import keyboard as keyboard
import data as data


async def start(update: Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
        user_data = data.get_default_user(update.effective_user.username)
        user_data = data.write_to_log(user_data, f"New user")
        data.save_user_data(user_data)

    user_data = data.write_to_log(user_data, f"Main menu opened")
    data.save_user_data(user_data)
    await update.message.reply_text(
        "Главное меню",
        reply_markup = keyboard.get_main_menu() 
    )
    return 0


async def storage(update: Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)

    if not user_data:
        data.write_to_log(user_data, f"Not started user")
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    data.write_to_log(user_data, f"Storage menu opened")
    await update.message.reply_text(
        "Меню складов",
        reply_markup = keyboard.get_storage_menu()
    )
    return 0


async def info(update: Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
        data.write_to_log(user_data, f"Not started user")
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    data.write_to_log(f"Info menu opened")
    await update.message.reply_text(
        "Меню информации",
        reply_markup = keyboard.get_info_menu()
    )
    return 0


async def admin(update: Update, context: tgext.ContextTypes.DEFAULT_TYPE): 
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
        data.write_to_log(user_data, f"Not started user")
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    data.write_to_log(user_data, f"Admin menu was called")
    user_data = data.get_user_data(update.effective_user.username)
     
    if user_data["info"]["admin"]:
        data.write_to_log(user_data, f"Admin menu opened")
        user_data = data.get_user_data(update.effective_user.username)
        await update.message.reply_text(
            "Да, на самом деле, ты админ",
            reply_markup = keyboard.get_info_menu()
        )
    else:
        data.write_to_log(user_data, f"Admin access denied")
        user_data = data.get_user_data(update.effective_user.username)
        await update.message.reply_text(
            "У тебя нет админ доступа",
            reply_markup = keyboard.get_under_construction_menu()
        )

    return 0

