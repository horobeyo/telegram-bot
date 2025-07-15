from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7533758655:AAFEs4I4KC7IuyjhGERycgiMlIs98klr1pI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот і я працюю на Render! 🔥")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущено... ✅")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())