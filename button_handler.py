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
            "Меню складов",
            reply_markup = keyboard.get_storage_menu()
        )
    elif query.data == "info":
        info_keyboard = None
        if user_data["info"]["admin"]:
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
    elif query.data == "add_storage":
        data.write_to_log(user_data, f"Add storage menu opened")
        await query.edit_message_text(
            "Введите имя склада",
            reply_markup = keyboard.get_add_storage_menu()
        )
    elif query.data == "cancel_bot_creation":
        data.write_to_log(user_data, f"Storage menu opened")
        await query.edit_message_text(
            "Меню складов",
            reply_markup = keyboard.get_storage_menu()
        )
    elif query.data == "clean_log":
        data.clean_log(user_data)
        data.write_to_log(user_data, f"Logs cleaned by @{update.effective_user.username}")
        await query.edit_message_text(
            "Успех. Все еще админ меню",
            reply_markup = keyboard.get_admin_menu()
        )
    elif query.data == "admin_menu":
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





    else:
        data.write_to_log(user_data, f"Menu '{query.data}' opened")
        await query.edit_message_text(
            f"Функция \"{query.data}\" в разработке",
            reply_markup = keyboard.get_under_construction_menu()
        )
