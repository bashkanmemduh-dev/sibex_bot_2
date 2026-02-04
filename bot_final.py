from telegram.ext import Application, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

async def start(update, context):
    """پاسخ به دستور /start"""
    user = update.effective_user
    user_name = user.first_name or user.username or "کاربر عزیز"
    welcome_message = f"سلام {user_name} عزیز! 🤗\nبه ربات سیب‌اکس خوش آمدید."
    # چاپ لاگ برای اطمینان از اجرای تابع
    logger.info(f"دستور /start توسط {user_name} (ID: {user.id}) دریافت شد.")
    await update.message.reply_text(welcome_message)

async def error_handler(update, context):
    """خطاها را در لاگ ثبت می‌کند."""
    logger.error("خطا در ربات:", exc_info=context.error)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_error_handler(error_handler)
    print("✅ ربات نهایی در حال راه‌اندازی...")
    application.run_polling()

if __name__ == '__main__':
    main()
