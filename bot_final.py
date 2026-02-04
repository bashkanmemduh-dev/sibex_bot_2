from telegram.ext import Application, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توکن خود را اینجا قرار دهید
TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

async def start(update, context):
    await update.message.reply_text('ربات تست موفقیت‌آمیز است!')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ ربات تست در حال راه‌اندازی...")
    app.run_polling()

if __name__ == '__main__':
    main()
