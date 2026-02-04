from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'

# 🔹 تابع بررسی عضویت در کانال
async def check_user_membership(bot, user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id="@Cibexi", user_id=user_id)
        member_status = chat_member.status
        return member_status in ("member", "administrator", "creator")
    except Exception as e:
        logger.error(f"خطا در بررسی عضویت: {e}")
        return False

# 🔹 تابع اصلی start با بررسی عضویت
async def start(update, context):
    user = update.effective_user
    user_id = user.id
    user_name = user.first_name or user.username or "کاربر عزیز"

    is_member = await check_user_membership(context.bot, user_id)

    if is_member:
        # کاربر عضو است
        welcome_text = f"سلام {user_name} عزیز! 🤗\nعضویت شما تأیید شد. به ربات سیب‌اکس خوش آمدید.\n(منوی اصلی به زودی فعال می‌شود)"
        await update.message.reply_text(welcome_text)
    else:
        # کاربر عضو نیست
        welcome_text = f"سلام {user_name}!\nبرای استفاده از ربات سیب‌اکس، لازمه ابتدا در کانال ما عضو بشی 🤗"
        keyboard = [
            [InlineKeyboardButton("🔗 عضویت در کانال", url="https://t.me/Cibexi")],
            [InlineKeyboardButton("✅ عضو شدم / بررسی مجدد", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# 🔹 تابع مدیریت کلیک روی دکمه «عضو شدم»
async def button_callback(update, context):
    query = update.callback_query
    user = query.from_user
    await query.answer()  # حذف حالت منتظر در دکمه

    if query.data == "check_membership":
        is_member = await check_user_membership(context.bot, user.id)
        if is_member:
            await query.edit_message_text(text=f"عالیه {user.first_name}! ✅\nعضویت شما تأیید شد.")
        else:
            new_text = f"متأسفم {user.first_name} ❌\nهنوز در کانال @Cibexi عضو نشدی."
            keyboard = [
                [InlineKeyboardButton("🔗 عضویت در کانال", url="https://t.me/Cibexi")],
                [InlineKeyboardButton("✅ عضو شدم / بررسی مجدد", callback_data="check_membership")]
            ]
            new_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=new_text, reply_markup=new_markup)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("✅ ربات با قابلیت بررسی عضویت فعال شد!")
    application.run_polling()

if __name__ == '__main__':
    main()
