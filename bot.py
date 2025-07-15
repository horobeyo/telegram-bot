import os
import asyncio
from flask import Flask, request, abort
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Завантажуємо змінні середовища
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", "10000"))
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Flask застосунок
app = Flask(__name__)

# Telegram застосунок
telegram_app = Application.builder().token(TOKEN).build()

# Обробник /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює!")

telegram_app.add_handler(CommandHandler("start", start))

# Webhook шляхи
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://{HOSTNAME}{WEBHOOK_PATH}"

# 🔥 Кореневий маршрут (для перевірки Render'ом)
@app.route("/", methods=["GET"])
def index():
    return "Бот працює! Webhook OK ✅"

# 🔁 Webhook маршрут Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, telegram_app.bot)
        telegram_app.update_queue.put(update)
        print("🔔 Отримано update від Telegram:", json_data)
        return "OK"
    except Exception as e:
        print("❌ Помилка при обробці webhook:", e)
        return "Internal Server Error", 500

# 🎯 Основний запуск
if __name__ == "__main__":
    async def main():
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook встановлено за адресою: {WEBHOOK_URL}")
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
