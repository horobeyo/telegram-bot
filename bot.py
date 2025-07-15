
import os
from dotenv import load_dotenv

load_dotenv()  # Завантажує змінні з .env у середовище

from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ваш URL з Render або іншого сервісу

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("TOKEN або WEBHOOK_URL не встановлені у .env файлі")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт!")

telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return "OK"

@app.route('/')
def index():
    return "Бот працює!", 200

if __name__ == '__main__':
    # Встановити вебхук (потрібно зробити один раз при запуску)
    import asyncio
    async def set_webhook():
        await telegram_app.bot.set_webhook(WEBHOOK_URL + '/' + TOKEN)
    asyncio.run(set_webhook())

    # Запуск Flask сервера
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))

