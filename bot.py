import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Налаштування логів
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Змінні оточення
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ініціалізація Flask та Telegram Application
app = Flask(__name__)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Приклад команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює 🚀")

telegram_app.add_handler(CommandHandler("start", start))


# === ASYNC Webhook handler ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.initialize()
    await telegram_app.process_update(update)
    return "ok", 200


# === Проста перевірка доступності головної сторінки ===
@app.route("/", methods=["GET"])
def index():
    return "Бот працює!", 200


# === Основний блок запуску бота та встановлення вебхука ===
if __name__ == "__main__":
    import asyncio

    async def set_webhook():
        bot = Bot(token=BOT_TOKEN)
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
        await bot.set_webhook(webhook_url)
        logging.info(f"✅ Webhook встановлено за адресою: {webhook_url}")

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=10000)


