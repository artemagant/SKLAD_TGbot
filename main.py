import telegram as tg
import telegram.ext as tgext

import commands as cmd
import button_handler as btn_handler

TOKEN = "no token"
with open("token.txt", "r") as file:
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

    app.add_handler(tgext.CallbackQueryHandler(btn_handler.handle))

    print("\nBot started\n")
    app.run_polling()

if __name__ == "__main__":
    main()
