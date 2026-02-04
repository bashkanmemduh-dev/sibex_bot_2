from telegram.ext import Application, CommandHandler
import logging
import traceback  # برای گرفتن جزئیات خطا

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

# 🔹 یک خطای گیرنده جدید اضافه می‌کنیم
async def error_handler(update, context):
    """خطاها را در لاگ ثبت می‌کند."""
    logger.error("یک خطا رخ داد!", exc_info=context.error)
    # چاپ جزئیات خطا در کنسول (که در Railway لاگ می‌شود)
    traceback.print_exception(type(context.error), context.error, context.error.__traceback__)

async def start(update, context):
    """پاسخ به دستور /start (نسخه سازگار)"""
    user_first_name = update.message.from_user.first_name
    user_name = user_first_name if user_first_name else "کاربر عزیز"
    welcome_message = f"سلام {user_name} عزیز! 🤗\nبه ربات سیب‌اکس خوش آمدید."
    await update.message.reply_text(welcome_message)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # 🔹 خطای گیرنده را به اپلیکیشن اضافه می‌کنیم
    application.add_error_handler(error_handler)
    
    print("✅ ربات با خطای گیرنده در حال راه‌اندازی...")
    application.run_polling()

if __name__ == '__main__':
    main()
