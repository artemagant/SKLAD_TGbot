import telegram as tg
import telegram.ext as tgext
import json

import data as data
import keyboard as keyboard

async def handle_text(update: tg.Update, context):
    user_data = data.get_user_data(update.effective_user.username)

    if not user_data:
        await update.message.reply_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    state = data.get_state(update.effective_user.username)
    text = update.message.text

    if (state == "admin_username_await"):
        mes = data.get_user_data(text)
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

    if (state == "storage_name"):
        if (data.create_storage(user_data, text)):
            data.write_to_log(user_data, f"Storage creation denied - '{text}' already exists")
            await update.message.reply_text(
                f"Склад '{text}' уже существует",
                reply_markup = keyboard.get_return_to_storage_menu()
            )
        else:
            data.write_to_log(user_data, f"Create storage '{text}'")
            await update.message.reply_text(
                f"Успех! Склад '{text}' создан",
                reply_markup = keyboard.get_successed_storage_creation_menu(text, user_data)
            )
    if (state.startswith("itemcreating_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        user_data = data.create_item(user_data, storage_name, text)
    data.set_state(update.effective_user.username, "None")
