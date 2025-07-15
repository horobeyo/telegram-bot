import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://yourapp.onrender.com/webhook/yourtoken

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("TOKEN або WEBHOOK_URL не задані")

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт!")

telegram_app = Application.builder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

async def main():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    port = int(os.environ.get("PORT", 5000))
    # Запускаємо Flask у окремому потоці, тому запускаємо у звичайному режимі
    # Інакше треба складніше інтегрувати asyncio + Flask (через aiohttp або quart)
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(main())

