import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# Ініціалізація Flask
flask_app = Flask(__name__)

# Зчитуємо токен і URL із змінних середовища
TOKEN = os.environ["TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Створюємо Telegram Application
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт із Webhook! ✅")

# Додаємо обробник до Telegram Application
telegram_app.add_handler(CommandHandler("start", start))

# Роут для перевірки, що сервер працює
@flask_app.route("/", methods=["GET"])
def index():
    return "Бот запущено ✅"

# Роут, куди Telegram надсилає оновлення
@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"

# Запускаємо Telegram Webhook + Flask сервер
if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
        flask_app=flask_app,
    )

