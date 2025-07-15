from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await update.message.reply_text("Привіт!")

async def main():
    app = ApplicationBuilder().token("7533758655:AAFEs4I4KC7IuyjhGERycgiMlIs98klr1pI").build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
