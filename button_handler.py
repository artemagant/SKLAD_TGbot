import telegram as tg
import telegram.ext as tgext

import keyboard as keyboard
import data as data

async def handle(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    user_data = data.get_user_data(update.effective_user.username)
    if not user_data:
        await update.callback_query.edit_message_text(
            "Активируйте бота перед началом (/start)"
        )
        return 1

    data.set_state(update.effective_user.username, "None")
    user_data = data.get_user_data(update.effective_user.username)
    #print(data.get_user_data(update.effective_user.username))

    query = update.callback_query
    await query.answer()

    if query.data == "storage":
        data.write_to_log(user_data, f"Storage menu opened")
        await query.edit_message_text(
            "Меню ваших складов",
            reply_markup = keyboard.get_storage_menu()
        )
    elif query.data == "info":
        info_keyboard = None
        if True:
            info_keyboard = keyboard.get_info_menu_admin()
        else:
            info_keyboard = keyboard.get_info_menu()
        data.write_to_log(user_data, f"Info menu opened")
        await query.edit_message_text(
            "Меню информации",
            reply_markup = info_keyboard
        )
    elif query.data == "return_main":
        data.write_to_log(user_data, f"Main menu opened")
        await query.edit_message_text(
            "Главное меню",
            reply_markup = keyboard.get_main_menu()
        )

    #
    # Storage
    #
    elif query.data == "add_storage":
        data.write_to_log(user_data, f"Add storage menu opened")
        data.set_state(user_data["info"]["username"], "storage_name")
        await query.edit_message_text(
            "Введите имя склада",
            reply_markup = keyboard.get_add_storage_menu()
        )
    elif query.data == "cancel_bot_creation":
        data.write_to_log(user_data, f"Storage menu opened")
        await query.edit_message_text(
            "Меню ваших складов",
            reply_markup = keyboard.get_storage_menu()
        )
    elif query.data == "storage_list":
        data.write_to_log(user_data, f"Storage list opened")
        keyboard_markup = keyboard.get_storage_list_menu(user_data)
        if (not keyboard_markup):
            await query.edit_message_text(
                "У вас нет складов",
                reply_markup = keyboard.get_return_to_storage_menu()
            )
            return
        await query.edit_message_text(
            "Список ваших складов",
            reply_markup = keyboard.get_storage_list_menu(user_data)
        )

    elif query.data.startswith("configurestorage_"):
        username = query.data.split("_")[1]
        storage_name = query.data.split("_")[2]
        data.write_to_log(user_data, f"Configure storage '{storage_name}' of @{username}")
        storage_owner_data = data.get_user_data(username)
        storage_owner_data =data.write_to_log(storage_owner_data,f"@{user_data["info"]["username"]} configure your storage '{storage_name}'")
        await query.edit_message_text(
            f"Меню вашего склада '{storage_name}'",
            reply_markup = keyboard.get_storage_configure_menu(storage_name, user_data))
        
    elif query.data.startswith("storagesettings_"):
        username = query.data.split("_")[1]
        storage_name = query.data.split("_")[2]
        data.write_to_log(user_data, f"Storage '{storage_name}' settings of @{username} opened")
        storage_owner_data = data.get_user_data(username)
        storage_owner_data =data.write_to_log(storage_owner_data,f"@{user_data["info"]["username"]} setting your storage '{storage_name}'")
        await query.edit_message_text(
            f"Настройки вашего склада '{storage_name}'",
            reply_markup = keyboard.get_storage_settings_menu(storage_name, user_data))

    elif query.data.startswith("storageinfo_"):
        username = query.data.split("_")[1]
        storage_name = query.data.split("_")[2]
        data.write_to_log(user_data, f"Storage '{storage_name}' info of @{username} opened")
        storage_owner_data = data.get_user_data(username)
        storage_owner_data =data.write_to_log(storage_owner_data,f"@{user_data["info"]["username"]} saw info of your storage '{storage_name}'")
        storage_data = data.get_storage_data(data.get_user_data(username), storage_name)
        storage_info = storage_data.get("info", {"name": "a", "description": None, "data_creating": None, "level": 0})
        info_text = f"Описание: {storage_info["description"]}\nДата создания: {storage_info["date_creating"]}\nУровень: {storage_info["level"]}"
        await query.edit_message_text(
            f"Информация вашего склада '{storage_name}':\n{info_text}",
            reply_markup = keyboard.get_storage_info_menu(storage_name, user_data))

    elif query.data.startswith("storageitems_"):
        username = query.data.split("_")[1]
        storage_name = query.data.split("_")[2]
        data.write_to_log(user_data, f"Storage '{storage_name}' itemes of @{username} opened")
        storage_owner_data = data.get_user_data(username)
        storage_owner_data =data.write_to_log(storage_owner_data,f"@{user_data["info"]["username"]} opened items menu of your storage '{storage_name}'")
        await query.edit_message_text(
            f"Список предметов вашего склада '{storage_name}'",
            reply_markup = keyboard.get_storage_itemes_menu(storage_name, user_data))
    elif query.data.startswith("createitem_"):
        username = query.data.split("_")[1]
        storage_name = query.data.split("_")[2]
        data.write_to_log(user_data, f"In storage '{storage_name}' item is creating by @{username}")
        storage_owner_data = data.get_user_data(username)
        storage_owner_data =data.write_to_log(storage_owner_data,f"@{user_data["info"]["username"]} is creating item in your storage '{storage_name}'")
        data.set_state(username, f"itemcreating_{username}_{storage_name}")
        await query.edit_message_text(
            f"Введите имя предмета",
            reply_markup = keyboard.get_creating_item_menu(storage_name, user_data))












    #
    # Admin menu buttons
    #
    elif query.data == "clean_log":
        data.clean_log(user_data)
        data.write_to_log(user_data, f"Logs cleaned by @{update.effective_user.username}")
        await query.edit_message_text(
            "Успех. Все еще админ меню",
            reply_markup = keyboard.get_admin_menu()
        )
    elif query.data == "admin_menu":
        data.write_to_log(user_data, f"Admin menu called")
        user_data = data.get_user_data(user_data.get("info", {"username": None, "admin": False, "state": None}).get("username", None))
        if (not user_data["info"]["admin"]):
            data.write_to_log(user_data, "Admin access denied")
            await query.edit_message_text(
                "У тебя нет админ доступа.\nСвяжись с @artemagant, для его получения",
                reply_markup = keyboard.get_under_construction_menu()
            )
            return
        data.write_to_log(user_data, f"Admin menu opened")
        user_data = data.get_user_data(update.effective_user.username)
        await query.edit_message_text(
            "Реал админ меню",
            reply_markup = keyboard.get_admin_menu()
        )
    elif query.data == "admin_user_data":
        data.write_to_log(user_data, f"User data configuration opened")
        user_data = data.get_user_data(update.effective_user.username)
        await query.edit_message_text(
            "Введите username пользователя без @",
            reply_markup = keyboard.get_return_to_admin_menu()
        )
        data.set_state(user_data["info"]["username"], "admin_username_await")
    elif query.data.startswith("yesforcreatedefaultuserdata_"):
        username = query.data.split("_")[1]
        data.write_to_log(user_data, f"Create default user for @{username}")
        user_data = data.get_default_user(username)
        user_data = data.write_to_log(user_data, f"New user")
        data.save_user_data(user_data)
        await query.edit_message_text(
            "Успех",
            reply_markup = keyboard.get_return_to_admin_menu()
        )
    elif query.data.startswith("adminresetuser_"):
        username = query.data.split("_")[1]
        data.write_to_log(user_data, f"Resets user {username}")
        data.save_user_data(data.get_default_user(username))
        data.write_to_log(data.get_user_data(username), f"User been reseted by @{update.effective_user.username}")
        await query.edit_message_text(
            f"Успех! @{username} сброшен",
            reply_markup = keyboard.get_return_to_admin_menu()
        )
    elif query.data.startswith("admindeleteuser_"):
        username = query.data.split("_")[1]
        data.write_to_log(user_data, f"Deletes user {username}")
        data.delete_user_data(username)
        await query.edit_message_text(
            f"Успех! @{username} удален",
            reply_markup = keyboard.get_return_to_admin_menu()
        )
    elif query.data.startswith("admindeletelogs_"):
        username = query.data.split("_")[1]
        data.write_to_log(user_data, f"Delets logs of {username}")
        data.delete_logs_user(username)
        data.write_to_log(data.get_user_data(username), f"Logs been resets by @{update.effective_user.username}")
        await query.edit_message_text(
            f"Успех! Логи @{username} удалены",
            reply_markup = keyboard.get_return_to_admin_menu()
        )
    elif query.data.startswith("adminchangeadmin_"):
        username = query.data.split("_")[1]
        data.write_to_log(user_data, f"Change admin status of @{username} to {not data.get_user_data(username)["info"]["admin"]}")
        data.change_admin(username)
        data.write_to_log(data.get_user_data(username), f"Admin status been changed to {data.get_user_data(username)["info"]["admin"]} by @{update.effective_user.username}")
        await query.edit_message_text(
            f"Успех! @{username}'s admin статус теперь {data.get_user_data(username)["info"]["admin"]}",
            reply_markup = keyboard.get_return_to_admin_menu()
        )
    #elif query.data.startswith("adminseelogs_"):
    #    username = query.data.split("_")[1]
    #    data.write_to_log(user_data, f"Saw logs of @{username}")
    #    data.write_to_log(data.get_user_data(username), f"Logs seen by @{update.effective_user.username}")
    #    user_logs = data.get_user_data(username).get("Log", {"No logs"})
    #    data.set_state(update.effective_user.username, "doing_logs")
    #    for i in user_logs:
    #        if (data.get_state(update.effective_user.username) != "doing_logs"):
    #            break
    #        await context.bot.send_message(
    #            chat_id=query.message.chat_id, text=f"{i}: {user_logs.get(i, "No Logs")}",
    #            reply_markup = keyboard.get_return_to_admin_menu()
    #        )
        




    else:
        data.write_to_log(user_data, f"Menu '{query.data}' opened")
        await query.edit_message_text(
            f"Функция \"{query.data}\" в разработке",
            reply_markup = keyboard.get_under_construction_menu()
        )
