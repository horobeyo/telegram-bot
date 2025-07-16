import os
import logging
import asyncio

from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, MessageHandler, filters, ContextTypes
)
from telegram.error import TelegramError
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Налаштування логування
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask сервер
app = Flask(__name__)

# Telegram Application
telegram_app = Application.builder().token(TOKEN).build()


# === Хендлери ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    username = update.effective_user.full_name
    logger.info(f"📨 Повідомлення від {username}: {text}")
    await update.message.reply_text("Привіт! Я бот, який модеруватиме канал 👮‍♂️")


# === Webhook маршрут ===
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    async def process():
        await telegram_app.initialize()
        await telegram_app.process_update(update)

    asyncio.run(process())
    return "OK", 200


# === Головна сторінка ===
@app.route("/", methods=["GET"])
def index():
    return "✅ Бот працює!"


# === Головна функція запуску ===
if __name__ == "__main__":
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Встановлення webhook
    async def set_webhook():
        url = f"https://{HOSTNAME}/{TOKEN}"
        try:
            await telegram_app.bot.set_webhook(url)
            print(f"✅ Webhook встановлено за адресою: {url}")
        except TelegramError as e:
            print(f"❌ Помилка при встановленні webhook: {e}")

    asyncio.run(set_webhook())

    # Запуск Flask
    app.run(host="0.0.0.0", port=10000)


