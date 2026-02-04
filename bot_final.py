from telegram.ext import Application, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🔹 توکن خود را اینجا قرار دهید
TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

async def start(update, context):
    """پاسخ به دستور /start با نام کاربر"""
    # دریافت اطلاعات کاربر
    user = update.effective_user
    # استفاده از اسم اول یا نام کاربری
    user_name = user.first_name or user.username or "کاربر عزیز"

    # ساخت پیام شخصی‌سازی شده
    welcome_message = f"سلام {user_name} عزیز! 🤗\nبه ربات سیب‌اکس خوش آمدید."
    await update.message.reply_text(welcome_message)
