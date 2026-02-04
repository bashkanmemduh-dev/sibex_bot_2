from telegram.ext import Application, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🔹 توکن خود را اینجا قرار دهید
TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

async def start(update, context):
    """پاسخ به دستور /start"""
    await update.message.reply_text('ربات فعال شد! به منوی اصلی خوش آمدید.')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("✅ ربات پایه در حال راه‌اندازی...")
    application.run_polling()

if __name__ == '__main__':
    main()
