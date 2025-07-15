import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is not set")

app = Flask(__name__)
WEBHOOK_PATH = f"/{TOKEN}"

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я працюю через вебхук.")

# Ініціалізуємо бота і додаємо хендлери
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Ендпоінт, який приймає webhook від Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    # Встановлюємо webhook (Render сам викликає цей скрипт під час запуску)
    import asyncio

    async def main():
        await application.bot.set_webhook(f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}")
        print("Webhook встановлено!")

        # Запускаємо webhook сервер
        await application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 10000)),
            url_path=TOKEN,
            webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}",
            drop_pending_updates=True,
        )

    asyncio.run(main())

