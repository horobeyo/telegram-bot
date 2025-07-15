import os
from flask import Flask, request, abort
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

# Шлях і URL для webhook
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://{HOSTNAME}{WEBHOOK_PATH}"

# Кореневий маршрут (Render перевіряє, чи сервіс живий)
@app.route("/", methods=["GET"])
def index():
    return "Бот працює! Webhook OK ✅"

# Webhook маршрут для отримання оновлень від Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        # Обробляємо оновлення асинхронно
        asyncio.create_task(telegram_app.process_update(update))
        return "OK"
    else:
        abort(405)

# Запуск сервера і встановлення webhook
if __name__ == "__main__":
    async def main():
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook встановлено за адресою: {WEBHOOK_URL}")
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
