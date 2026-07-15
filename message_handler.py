import telegram as tg
import telegram.ext as tgext
import json

import data as data
import keyboard as keyboard

async def handle_text(update: Update, context):
    user_data = data.get_user_data(update.effective_user.username)

    if not user_data:
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    state = data.get_state(update.effective_user.username)
    text = update.message.text
    mes = data.get_user_data(text) 
    if (state == "admin_username_await"):
        if (data.get_user_data(text)):
            mes["Log"] = str(len(mes["Log"])) + " line/s of log"
            data.write_to_log(user_data, f"Accessed data of {text}")
            await update.message.reply_text(
                json.dumps(mes),
                reply_markup = keyboard.get_user_data_menu(text)
            )
        else:
            await update.message.reply_text(
                f"Юзер @{text} еще не активировал бота\nХочешь создать для юзера дефолтную дату?",
                reply_markup = keyboard.get_create_default_user_data_menu(text)
            )
    data.set_state(update.effective_user.username, "None")
