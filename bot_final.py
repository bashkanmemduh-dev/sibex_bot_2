from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters                                              from telegram import InlineKeyboardButton, InlineKeyboardMarkup                    import logging
                                                                                   logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)                                                                
TOKEN = '8576859515:AAFD5HaPh0Y8w7FyazLFrKslB_O514ahzqM'                           
# مراحل مکالمه (State) برای خرید هات ووچر                                          AMOUNT, PHOTO = range(2)
                                                                                   # تابع بررسی عضویت
async def check_user_membership(bot, user_id):                                         try:                                                                                   chat_member = await bot.get_chat_member(chat_id="@Cibexi", user_id=user_id)
        member_status = chat_member.status
        return member_status in ("member", "administrator", "creator")                 except Exception as e:                                                                 logging.error(f"خطا در بررسی عضویت: {e}")
        return False

# نمایش منوی اصلی                                                                  async def show_main_menu(update, user, context):
    user_name = user.first_name or user.username or "کاربر عزیز"
    welcome_text = f"{user_name} عزیز، به ربات سیب‌اکس خوش اومدی! 🚀\nلطفا خدمات مورد نظرت رو انتخاب کن:"                                                              
    keyboard = [
        [InlineKeyboardButton("خرید ووچر", callback_data="buy_voucher")],                  [InlineKeyboardButton("فروش ووچر", callback_data="sell_voucher")],                 [InlineKeyboardButton("خرید ارز", callback_data="buy_currency")],
        [InlineKeyboardButton("فروش ارز", callback_data="sell_currency")],                 [InlineKeyboardButton("پشتیبانی 📞", callback_data="support")]
    ]                                                                                  reply_markup = InlineKeyboardMarkup(keyboard)                                                                                                                         if update.callback_query:                                                              await update.callback_query.edit_message_text(text=welcome_text, reply_markup=reply_markup)                                                                       else:                                                                                  await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# نمایش زیرمنوی خرید ووچر                                                          async def show_buy_voucher_menu(update):
    menu_text = "✅ لطفا نوع ووچر مورد نظر برای خرید رو انتخاب کن:"

    keyboard = [                                                                           [InlineKeyboardButton("هات ووچر", callback_data="voucher_hot")],
        [InlineKeyboardButton("پرمیوم ووچر", callback_data="voucher_premium")],
        [InlineKeyboardButton("یو ووچر", callback_data="voucher_u")],                      [InlineKeyboardButton("بازگشت ↩️", callback_data="back_to_main")]               ]
    reply_markup = InlineKeyboardMarkup(keyboard)
                                                                                       await update.callback_query.edit_message_text(text=menu_text, reply_markup=reply_markup)

# مرحله ۱: شروع فرآیند خرید هات ووچر                                               async def start_hot_voucher_purchase(update, context):
    query = update.callback_query
    await query.answer()                                                                                                                                                  context.user_data['voucher_type'] = 'هات ووچر'

    await query.edit_message_text(                                                         text="🎫 **خرید هات ووچر**\n\n"                                                         "لطفا مبلغ مورد نظر را وارد نمائید (حداقل مبلغ خرید ۵۰۰ هزار تومان)\n\n"
             "⚠️ توجه: فقط عدد وارد کنید (مثال: 500000 یا 1000000)"                     )                                                                                  return AMOUNT

# مرحله ۲: دریافت و بررسی مبلغ از کاربر                                            async def receive_amount(update, context):                                             user_message = update.message.text.strip()

    try:                                                                                   amount = int(user_message)                                                         if amount < 500000:
            await update.message.reply_text("❌ حداقل مبلغ خرید ۵۰۰,۰۰۰ تومان است. لطفا مجددا مبلغ را وارد کنید:")
            return AMOUNT                                                          
        context.user_data['amount'] = amount

        await update.message.reply_text(                                                       f"✅ مبلغ {amount:,} تومان ثبت شد.\n\n"
            "💳 **لطفا مبلغ را به حساب زیر واریز کنید:**\n"                                    "`6274121198470841`\n"
            "(سینا عبدوئی)\n\n"                                                                "📸 پس از واریز کردن مبلغ، **عکس رسید تراکنش** را ارسال نمائید.\n\n"
            "🔙 برای لغو خرید از دستور /cancel استفاده کنید."                              )                                                                                  return PHOTO

    except ValueError:                                                                     await update.message.reply_text("❌ فرمت مبلغ نامعتبر است. لطفا فقط عدد وارد کنید (مثال: 1000000):")
        return AMOUNT
                                                                                   # مرحله ۳: دریافت عکس رسید
async def receive_photo(update, context):
    if update.message.photo:
        voucher_type = context.user_data.get('voucher_type', 'هات ووچر')                   amount = context.user_data.get('amount', 0)                                        user = update.message.from_user

        await update.message.reply_text(                                                       f"✅ **تراکنش شما ثبت شد!**\n\n"                                                   f"📋 **جزئیات خرید:**\n"
            f"• نوع ووچر: {voucher_type}\n"                                                    f"• مبلغ: {amount:,} تومان\n"                                                      f"• کاربر: {user.first_name}\n\n"                                                  f"🕐 به زودی بررسی و انجام می‌شود.\n\n"
            f"📞 برای پیگیری می‌توانید از قسمت پشتیبانی اقدام کنید."
        )                                                                                                                                                                     logging.info(f"خرید جدید: {voucher_type} - {amount} تومان - کاربر: {user.id}")                                                                                                                                                                           context.user_data.clear()

        await show_main_menu(update, user, context)                                        return ConversationHandler.END

    else:                                                                                  await update.message.reply_text("❌ لطفا فقط عکس رسید تراکنش را ارسال کنید.")
        return PHOTO                                                                                                                                                  # تابع لغو مکالمه
async def cancel(update, context):                                                     user = update.message.from_user
    logging.info(f"کاربر {user.id} فرآیند خرید را لغو کرد.")                                                                                                              await update.message.reply_text("❌ فرآیند خرید لغو شد.")
    context.user_data.clear()                                                      
    await show_main_menu(update, user, context)                                        return ConversationHandler.END
                                                                                   async def start(update, context):
    user = update.effective_user                                                       user_id = user.id
                                                                                       is_member = await check_user_membership(context.bot, user_id)
                                                                                       if is_member:
        await show_main_menu(update, user, context)                                    else:
        welcome_text = f"سلام {user.first_name}!\nبرای استفاده از خدمات ربات سیب‌اکس، لازمه ابتدا در کانال ما عضو بشی 🤗"
        keyboard = [                                                                           [InlineKeyboardButton("🔗 عضویت در کانال", url="https://t.me/Cibexi")],
            [InlineKeyboardButton("✅ عضو شدم / بررسی مجدد", callback_data="check_membership")]
        ]                                                                                  reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)   
async def button_callback(update, context):                                            query = update.callback_query
    user = query.from_user                                                             await query.answer()

    if query.data == "check_membership":
        is_member = await check_user_membership(context.bot, user.id)
        if is_member:                                                                          await show_main_menu(update, user, context)
        else:                                                                                  new_text = f"متأسفم {user.first_name} ❌\nهنوز در کانال @Cibexi عضو نشدی."                                                                                            keyboard = [
                [InlineKeyboardButton("🔗 عضویت در کانال", url="https://t.me/Cibexi")],
                [InlineKeyboardButton("✅ عضو شدم / بررسی مجدد", callback_data="check_membership")]                                                                               ]
            new_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=new_text, reply_markup=new_markup)  
    elif query.data == "buy_voucher":
        await show_buy_voucher_menu(update)                                        
    elif query.data == "voucher_hot":                                                      return await start_hot_voucher_purchase(update, context)
                                                                                       elif query.data in ["voucher_premium", "voucher_u"]:                                   voucher_type = "پرمیوم ووچر" if query.data == "voucher_premium" else "یو ووچر"                                                                                        await query.answer(f"خرید {voucher_type} به زودی فعال می‌شود. 🛒", show_alert=True)                                                                            
    elif query.data == "back_to_main":                                                     await show_main_menu(update, user, context)
                                                                                       else:                                                                                  option_name = "این گزینه"                                                          if query.data == "sell_voucher":
            option_name = "فروش ووچر"                                                      elif query.data == "buy_currency":                                                     option_name = "خرید ارز"
        elif query.data == "sell_currency":                                                    option_name = "فروش ارز"
        elif query.data == "support":                                                          option_name = "پشتیبانی"                                                       await query.answer(f"شما گزینه '{option_name}' را انتخاب کردید. 🛠️\n(این بخش در حال توسعه است)", show_alert=True)                                                                                                                                 def main():                                                                            # 🔧 این بخش اصلاح شده و timeouts اضافه شده‌اند
    application = Application.builder() \                                                  .token(TOKEN) \
        .read_timeout(30) \                                                                .write_timeout(30) \
        .build()                                                                   
    # ساخت ConversationHandler برای مدیریت فرآیند خرید                                 purchase_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_hot_voucher_purchase, pattern="^voucher_hot$")],
        states={                                                                               AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_amount)],                                                                                            PHOTO: [MessageHandler(filters.PHOTO, receive_photo)],
        },                                                                                 fallbacks=[CommandHandler("cancel", cancel)],
    )                                                                              
    application.add_handler(CommandHandler("start", start))                            application.add_handler(purchase_conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))                 
    print("✅ ربات با تنظیمات افزایش تایم‌اوت (Conflict Fixed) فعال شد!")
    application.run_polling()                                                                                                                                         if __name__ == '__main__':                                                             main()
