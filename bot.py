
import os
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await update.message.reply_text("Привіт!")

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("TOKEN environment variable is not set")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    print("Бот запущено... ✅")
    app.run_polling()
