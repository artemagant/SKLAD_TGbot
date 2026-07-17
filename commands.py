import telegram as tg
import telegram.ext as tgext

import keyboard as keyboard
import data as data

def commands_action(update: tg.Update):
    data.set_state(update.effective_user.username, "None")

async def start(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
        user_data = data.get_default_user(update.effective_user.username)
        user_data = data.write_to_log(user_data, f"New user")
        data.save_user_data(user_data)
        await context.bot.send_message(
            chat_id=update.message.chat_id, 
            text=f"Добро пожаловать в этого бота!\nПеред стартом, вы должны знать, что вся ваша информация хранится в обычном файле data.json и может быть видна всем на https://github.com/artemagant/SKLAD_TGbot\n Удачи!",
        )

    user_data = data.write_to_log(user_data, f"Main menu opened")
    data.save_user_data(user_data)
    await update.message.reply_text(
        "Главное меню",
        reply_markup = keyboard.get_main_menu() 
    )

    commands_action(update)

    return 0


async def storage(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)

    if not user_data:
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    data.write_to_log(user_data, f"Storage menu opened")
    await update.message.reply_text(
        "Меню складов",
        reply_markup = keyboard.get_storage_menu()
    )

    commands_action(update)

    return 0


async def info(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    data.write_to_log(user_data, f"Info menu opened")

    info_keyboard = None
    if user_data["info"]["admin"]:
        info_keyboard = keyboard.get_info_menu_admin()
    else:
        info_keyboard = keyboard.get_info_menu()
    data.write_to_log(user_data, f"Info menu opened")
    await update.message.reply_text(
        "Меню информации",
        reply_markup = info_keyboard
    )

    commands_action(update)

    return 0


async def admin(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
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
            reply_markup = keyboard.get_admin_menu()
        )
    else:
        data.write_to_log(user_data, f"Admin access denied")
        user_data = data.get_user_data(update.effective_user.username)
        await update.message.reply_text(
            "У тебя нет админ доступа.\nСвяжитесь с @artemagant для его получения",
            reply_markup = keyboard.get_under_construction_menu()
        )
    commands_action(update)


    return 0
