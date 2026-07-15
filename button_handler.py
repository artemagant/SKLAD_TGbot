import telegram as tg
import telegram.ext as tgext

import keyboard as keyboard

async def handle(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "storage":
        print(f"Storage menu opened by @{update.effective_user.username}")
        await query.edit_message_text(
            "Меню складов",
            reply_markup = keyboard.get_storage_menu()
        )
    elif query.data == "info":
        print(f"Info menu opened by @{update.effective_user.username}")
        await query.edit_message_text(
            "Меню информации",
            reply_markup = keyboard.get_info_menu()
        )
    elif query.data == "return":
        print(f"Main menu opened by @{update.effective_user.username}")
        await query.edit_message_text(
            "Главное меню",
            reply_markup = keyboard.get_main_menu()
        )
    elif query.data == "add_storage":
        print(f"Add storage menu opened by @{update.effective_user.username}")
        await query.edit_message_text(
            "Введите имя склада",
            reply_markup = keyboard.get_add_storage_menu()
        )
    elif query.data == "cancel_bot_creation":
        print(f"Storage menu opened by @{update.effective_user.username}")
        await query.edit_message_text(
            "Меню складов",
            reply_markup = keyboard.get_storage_menu()
        )



    else:
        print(f"Menu \"{query.data}\" opened by @{update.effective_user.username}")
        await query.edit_message_text(
            f"Функция {query.data} в разработке",
            reply_markup = keyboard.get_under_construction_menu()
        )
