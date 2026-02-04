from telegram.ext import Application, CommandHandler
import logging
import time  # کتابخانه جدید برای توقف

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

async def start(update, context):
    """پاسخ به دستور /start"""
    user = update.effective_user
    user_name = user.first_name or user.username or "کاربر عزیز"
    welcome_message = f"سلام {user_name} عزیز! 🤗\nبه ربات سیب‌اکس خوش آمدید."
    logger.info(f"دستور /start توسط {user_name} دریافت شد.")
    await update.message.reply_text(welcome_message)

async def error_handler(update, context):
    """خطاها را در لاگ ثبت می‌کند."""
    logger.error("خطا در ربات:", exc_info=context.error)

def main():
    # 🔴 این توقف ۱۰ ثانیه‌ای برای دیدن خطا است
    print("⏳ در حال آماده‌سازی... (اگر خطایی باشد، در ۱۰ ثانیه آینده ظاهر می‌شود)")
    time.sleep(10)
    
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_error_handler(error_handler)
        print("✅ ربات در حال راه‌اندازی...")
        application.run_polling()
    except Exception as e:
        # این خطا را اگر اتفاق بیفتد، حتما Railway در لاگ نشان می‌دهد
        logger.critical(f"خطای بحرانی هنگام راه‌اندازی ربات: {e}", exc_info=True)
        # ربات را برای همیشه متوقف نکن، بگذار خطا را ببینیم
        time.sleep(60)

if __name__ == '__main__':
    main()
