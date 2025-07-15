import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
)

TOKEN = os.environ["TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # наприклад: https://your-service.onrender.com

# Flask server
flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює через Render Webhook ✅")


telegram_app.add_handler(CommandHandler("start", start))


@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "ok"


@flask_app.route("/", methods=["GET"])
def index():
    return "Привіт від бота! ✅"


if __name__ == "__main__":
    import threading
    import asyncio

    threading.Thread(target=telegram_app.run_polling, daemon=True).start()
    asyncio.run(telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}"))

    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
