import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Logging
logging.basicConfig(level=logging.INFO)

# Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{BOT_TOKEN}"
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}{WEBHOOK_PATH}"

# Telegram App
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
app = Flask(__name__)


# === Команди ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює ✅")

telegram_app.add_handler(CommandHandler("start", start))


# === Webhook маршрут ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        return "ok", 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "error", 500


@app.route("/")
def index():
    return "Бот працює!", 200


# === Головна функція ===
if __name__ == "__main__":
    import asyncio
    from telegram import Bot

    async def main():
        await telegram_app.initialize()
        bot = Bot(token=BOT_TOKEN)
        await bot.set_webhook(WEBHOOK_URL)
        logging.info(f"✅ Webhook встановлено: {WEBHOOK_URL}")

    asyncio.run(main())
    app.run(host="0.0.0.0", port=10000)



