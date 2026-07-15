import telegram as tg
import telegram.ext as tgext

import commands as cmd # commands.py - for CommandHandler functions
import button_handler as btn_handler # button_handler.py - for handle function
import message_handler as mes_handler
import data as data

TOKEN = "no token"
with open("../TgBotsTokens/SKLAD_token.txt", "r") as file:
    TOKEN = file.read().strip()

#async def command_start(update: tg.Update, context: tgext.ContextTypes.DEFAULT_TYPE):
#    print(f"Start been pressed by @{update.effective_user.username}")
#    await update.message.reply_text("Bot started")


def main():
    if TOKEN == "no token" or TOKEN is None:
        print("No token. It is null")
        return 1

    app = tgext.Application.builder().token(TOKEN).build()

    app.add_handler(tgext.CommandHandler("start", cmd.start))
    app.add_handler(tgext.CommandHandler("storage", cmd.storage))
    app.add_handler(tgext.CommandHandler("info", cmd.info))
    app.add_handler(tgext.CommandHandler("admin", cmd.admin))

    app.add_handler(tgext.CallbackQueryHandler(btn_handler.handle))
    app.add_handler(tgext.MessageHandler(tgext.filters.TEXT & ~tgext.filters.COMMAND, mes_handler.handle_text))

    print("\nBot started\n")
    app.run_polling()

if __name__ == "__main__":
    main()
