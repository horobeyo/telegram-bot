import os
import asyncio
import re
from flask import Flask, request
from telegram import Update, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()
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

# 🛡️ Фільтр китайських та арабських імен
async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(update, ChatMemberUpdated):
        new_user = update.chat_member.new_chat_member.user
        name = (new_user.full_name or "").strip()
        
        # Юнікод діапазони китайських/арабських символів
        if re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\u4E00-\u9FFF]', name):
            try:
                await context.bot.ban_chat_member(update.chat.id, new_user.id)
                print(f"🚫 Заборонено: {name} (id={new_user.id})")
            except Exception as e:
                print(f"⚠️ Помилка при бані: {e}")

telegram_app.add_handler(ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER))

# Webhook маршрут
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    
    async def process():
        await telegram_app.initialize()
        await telegram_app.process_update(update)

    asyncio.run(process())
    return "OK", 200

# Render перевірка живості
@app.route("/", methods=["GET"])
def index():
    return "✅ Бот працює!"

# Стартова точка
if __name__ == "__main__":
    # Встановлення webhook
    async def set_webhook():
        await telegram_app.bot.set_webhook(url=f"https://{HOSTNAME}/{TOKEN}")
        print(f"✅ Webhook встановлено за адресою: https://{HOSTNAME}/{TOKEN}")
    
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=PORT)

