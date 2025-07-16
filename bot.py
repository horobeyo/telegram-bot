import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Завантаження змінних середовища
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", "10000"))
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Flask застосунок
app = Flask(__name__)

# Telegram застосунок
telegram_app = Application.builder().token(TOKEN).build()

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ /start від користувача {update.effective_user.id}")
    await update.message.reply_text("Привіт! Бот працює!")

telegram_app.add_handler(CommandHandler("start", start))

# Webhook шлях
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://{HOSTNAME}{WEBHOOK_PATH}"

# Кореневий маршрут (перевірка Render)
@app.route("/", methods=["GET"])
def index():
    return "✅ Бот працює!"

# Webhook маршрут (POST)
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)

    async def process():
        await telegram_app.initialize()  # ініціалізація
        await telegram_app.process_update(update)

    asyncio.run(process())
    return "ok"

# Встановлення webhook після запуску
if __name__ == "__main__":
    async def main():
        await telegram_app.initialize()
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook встановлено за адресою: {WEBHOOK_URL}")
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
