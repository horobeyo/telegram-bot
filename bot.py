import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Наприклад: https://yourapp.onrender.com/webhook/yourtoken

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("TOKEN або WEBHOOK_URL не задані в змінних середовища")

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт!")

telegram_app = Application.builder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    # Отримуємо апдейт від Telegram
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    # Відправляємо апдейт в обробку
    telegram_app.update_queue.put_nowait(update)
    return "OK"

if __name__ == "__main__":
    # Встановлюємо webhook на сервері Telegram
    telegram_app.bot.set_webhook(WEBHOOK_URL)

    # Запускаємо Flask на потрібному порті
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

