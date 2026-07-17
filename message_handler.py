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
        if (text in storage_data["storage"]):
            await update.message.reply_text(
                f"Предмет {text} уже существует",
                reply_markup = keyboard.get_storage_itemes_menu(user_data, storage_name)
            )
        else:
            user_data = data.create_item(user_data, storage_name, text)
            await update.message.reply_text(
                f"Успех! Предмет '{text}' создан",
                reply_markup = keyboard.get_success_item_creation_menu(user_data, storage_name, text)
            )

    if (state.startswith("storagenamechanging_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storages = user_data["storages"]
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        if (storage_name != text and not text in storages):
            data.change_storage_name(user_data, storage_name, text)
            await update.message.reply_text(
                f"Успех! Склад '{storage_name}' теперь '{text}'",
                reply_markup = keyboard.get_storage_info_menu(text, user_data)
            )
        else:
            await update.message.reply_text(
                f"Склад '{text}' уже существует",
                reply_markup = keyboard.get_storage_info_menu(storage_name, user_data)
            )
    
    if (state.startswith("storagedescriptionchanging_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storages = user_data["storages"]
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        description = storage_data["info"]["description"]
        if (description != text):
            data.change_storage_description(user_data, storage_name, text)
            await update.message.reply_text(
                f"Успех! Описание склада '{storage_name}' теперь '{text}'",
                reply_markup = keyboard.get_storage_info_menu(storage_name, user_data)
            )
        else:
            await update.message.reply_text(
                f"Описание '{text}'\n совпадает с прошлым описанием",
                reply_markup = keyboard.get_storage_info_menu(storage_name, user_data)
            )
    
    if (state.startswith("changeitemname_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        item_name = state.split("_")[3]
        item_data = data.get_item_data(user_data, storage_name, item_name)
        if (item_name != text and not text in storage_data["storage"]):
            data.change_item_name(user_data, storage_name, item_name, text)
            await update.message.reply_text(
                f"Настройки предмета '{text}'\nУспех! Имя предмета '{item_name}' теперь '{text}'",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, text)
            )
        else:
            await update.message.reply_text(
                f"Настройки предмета '{item_name}'\nИмя '{text}' совпадает с прошлым именем предмета или такой предмет уже существует",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
            )
    if (state.startswith("changeitemdescription_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        item_name = state.split("_")[3]
        item_data = data.get_item_data(user_data, storage_name, item_name)
        if (item_data["description"] != text):
            data.change_item_description(user_data, storage_name, item_name, text)
            await update.message.reply_text(
                f"Настройки предмета '{text}'\nУспех! Описание предмета '{item_name}' теперь '{text}'",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
            )
        else:
            await update.message.reply_text(
                f"Настройки предмета '{item_name}'\nОписание '{text}' совпадает с прошлым описанием предмета",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
            )
    
    if (state.startswith("changeitemplace_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        item_name = state.split("_")[3]
        item_data = data.get_item_data(user_data, storage_name, item_name)
        if (item_data["place"] != text):
            data.change_item_place(user_data, storage_name, item_name, text)
            await update.message.reply_text(
                f"Настройки предмета '{text}'\nУспех! Место предмета '{item_name}' теперь '{text}'",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
            )
        else:
            await update.message.reply_text(
                f"Настройки предмета '{item_name}'\nМесто '{text}' совпадает с прошлым местом предмета",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
                )

    if (state.startswith("changeitemamount_")):
        username = state.split("_")[1]
        user_data = data.get_user_data(username)
        storage_name = state.split("_")[2]
        storage_data = data.get_storage_data(user_data, storage_name)
        item_name = state.split("_")[3]
        item_data = data.get_item_data(user_data, storage_name, item_name)
        if (item_data["amount"] != int(text)):
            data.change_item_amount(user_data, storage_name, item_name, text)
            await update.message.reply_text(
                f"Настройки предмета '{text}'\nУспех! Количество предмета '{item_name}' теперь {text}",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
            )
        else:
            await update.message.reply_text(
                f"Настройки предмета '{item_name}'\nКоличество '{text}' совпадает с прошлым количеством предмета",
                reply_markup = keyboard.get_item_settings_menu(user_data, storage_name, item_name)
                )

    data.set_state(update.effective_user.username, "None")
