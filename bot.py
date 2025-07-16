import os
import re
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ChatMemberHandler,
    ContextTypes
)
import asyncio

# Ініціалізація Flask
app = Flask(__name__)

# Змінні середовища
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", "10000"))
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Telegram Application
telegram_app = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює!")

telegram_app.add_handler(CommandHandler("start", start))

# Регулярка: китайські та арабські символи
chinese_or_arabic_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u4E00-\u9FFF]')

# Перевірка нових учасників
async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    if chat_member.new_chat_member and chat_member.new_chat_member.user:
        user = chat_member.new_chat_member.user
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        if chinese_or_arabic_re.search(name):
            try:
                await context.bot.ban_chat_member(chat_member.chat.id, user.id)
                await context.bot.unban_chat_member(chat_member.chat.id, user.id)  # kick
                print(f"🚫 Видалено користувача {name} через підозріле ім’я")
            except Exception as e:
                print(f"⚠️ Помилка при видаленні {name}: {e}")

telegram_app.add_handler(ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER))

# Webhook шлях і URL
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://{HOSTNAME}{WEBHOOK_PATH}"

# Render health-check
@app.route("/", methods=["GET"])
def index():
    return "✅ Бот запущено!"

# Основний webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        asyncio.run(telegram_app.initialize())  # Ініціалізує Application
        asyncio.run(telegram_app.process_update(update))
    except Exception as e:
        print(f"❌ Помилка в webhook: {e}")
        return "ERROR", 500
    return "OK", 200

# Встановлення webhook при запуску
if __name__ == "__main__":
    import threading

    async def set_webhook():
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook встановлено за адресою: {WEBHOOK_URL}")

    threading.Thread(target=lambda: asyncio.run(set_webhook())).start()
    app.run(host="0.0.0.0", port=PORT)
