import telegram as tg
import telegram.ext as tgext

import keyboard as keyboard

async def start(update: Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    print(f"Main menu opened by @{update.effective_user.username}")
    await update.message.reply_text(
        "Главное меню",
        reply_markup = keyboard.get_main_menu() 
    )
    return 0

async def storage(update: Update, context: tgext.ContextTypes.DEFAULT_TYPE):
    print(f"Storage menu opened by @{update.effective_user.username}")
    await update.message.reply_text(
        "Меню складов",
        reply_markup = keyboard.get_storage_menu()
    )
    return 0
