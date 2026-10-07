import os
import logging
import asyncio
import datetime
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    ContextTypes, 
    ChatJoinRequestHandler, 
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = "8684962736:AAGyFQOjw2RLq7FvZbBJVSGMpTHu2GURHdE"
BOT_NAME = "𝐌.𝐊 𝐓𝐑𝐀𝐃𝐄𝐑 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐎𝐓"
LOG_CHANNEL_ID = -1003724080321  
ANNOUNCEMENT_CHANNEL_ID = -1003931319011  
USERS_FILE = "users.txt"
PHOTO_URL = "https://i.postimg.cc/YSLc1PgP/file-00000000ec7881f794c7447fe7e6ddd3.png"

def save_user(user_id):
    try:
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w") as f:
                f.write("")
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
        if str(user_id) not in users:
            with open(USERS_FILE, "a") as f:
                f.write(str(user_id) + "\n")
    except Exception as e:
        print(f"Error saving user: {e}")

async def send_data_to_log_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, source_action: str):
    try:
        user = update.effective_user if update.effective_user else getattr(update.chat_join_request, 'from_user', None)
        if not user:
            return

        user_id = user.id
        save_user(user_id)

        username = f"@{user.username}" if user.username else "No Username"
        first_name = user.first_name or "N/A"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        pkt_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        current_time = pkt_time.strftime("%d %b %Y, %I:%M %p")
        
        log_msg = (
            f"🔥 NEW USER DATA CAPTURED 🔥\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Bot Name: {BOT_NAME}\n"
            f"👑 Brand: 𝐌.𝐊 𝐓𝐑𝐀𝐃𝐄𝐑\n"
            f"🆔 User ID: {user_id}\n"
            f"👤 Username: {username}\n"
            f"📛 Name: {full_name}\n"
            f"🕐 Time: {current_time}\n"
            f"📱 Source: {source_action}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        try:
            photos = await context.bot.get_user_profile_photos(user_id=user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                await context.bot.send_photo(chat_id=LOG_CHANNEL_ID, photo=file_id, caption=log_msg)
            else:
                await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_msg + "\n\n*(User has no Profile Picture)*")
        except Exception as inner_e:
            print(f"Photo sending error: {inner_e}")
    except Exception as e:
        print(f"Log channel error: {e}")

async def send_welcome_post(chat_id, user, context):
    try:
        user_first_name = user.first_name or "Trader"
        
        welcome_caption = (
            f"🔥 ━━━━━━━━━━━━━━━━━━━━━━━━━━ 🔥\n"
            f"✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌.𝐊 𝐓𝐑𝐀𝐃𝐄𝐑 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐙𝐎𝐍𝐄 ✨\n"
            f"🔥 ━━━━━━━━━━━━━━━━━━━━━━━━━━ 🔥\n\n"
            f"👋 𝐇𝐞𝐥𝐥𝐨, {user_first_name}!\n"
            f"𝐀𝐚𝐩𝐤𝐢 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐤𝐢 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐚𝐜𝐜𝐞𝐩𝐭 𝐡𝐨 𝐜𝐡𝐮𝐤𝐢 𝐡𝐚𝐢. 𝐌.𝐊 𝐓𝐑𝐀𝐃𝐄𝐑 𝐨𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐟𝐚𝐦𝐢𝐥𝐲 𝐦𝐞𝐢𝐧 𝐚𝐚𝐩𝐤𝐚 𝐝𝐢𝐥 𝐬𝐞 𝐤𝐡𝐚𝐢𝐫-𝐦𝐚𝐪𝐝𝐚𝐦 𝐡𝐚𝐢! 🖤👑\n\n"
            f"📋 𝐈𝐌𝐏𝐎𝐑𝐓𝐀𝐍𝐓 𝐆𝐔𝐈𝐃𝐄𝐋𝐈𝐍𝐄𝐒 & 𝐏𝐑𝐎𝐅𝐄𝐒𝐒𝐈𝐎𝐍𝐀𝐋 𝐒𝐘𝐒𝐓𝐄𝐌𝐒:\n\n"
            f"𝟏. 𝐒𝐞𝐬𝐬𝐢𝐨𝐧𝐬 𝐅𝐨𝐥𝐥𝐨𝐰 𝐊𝐚𝐫𝐧𝐚𝐲 𝐊𝐚 𝐓𝐚𝐫𝐞𝐞𝐪𝐚:\n"
            f"🎯 𝐇𝐚𝐦𝐞𝐬𝐡𝐚 𝐡𝐚𝐦𝐚𝐫𝐞 𝐝𝐢𝐲𝐞 𝐠𝐚𝐲𝐞 𝐫𝐮𝐥𝐞𝐬, 𝐩𝐫𝐞𝐜𝐢𝐬𝐞 𝐬𝐢𝐠𝐧𝐚𝐥𝐬, 𝐚𝐮𝐫 𝐬𝐭𝐫𝐢𝐜𝐭 𝐫𝐢𝐬𝐤 𝐦𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐭𝐫𝐚𝐝𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧𝐬 𝐣𝐨𝐢𝐧 𝐤𝐚𝐫𝐞𝐢𝐧 𝐭𝐚𝐚𝐤𝐞 𝐡𝐚𝐫 𝐭𝐫𝐚𝐝𝐞 𝐦𝐞𝐢𝐧 𝟏𝟎𝟎% 𝐩𝐫𝐨𝐟𝐢𝐭 𝐦𝐢𝐥 𝐬𝐚𝐤𝐞.\n\n"
            f"𝟐. 𝐅𝐞𝐞𝐝𝐛𝐚𝐜𝐤𝐬 𝐒𝐞𝐧𝐝 𝐊𝐚𝐫𝐧𝐚:\n"
            f"💬 𝐀𝐩𝐧𝐞 𝐩𝐫𝐨𝐟𝐢𝐭 𝐲𝐚 𝐥𝐨𝐬𝐬 𝐤𝐞 𝐬𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭𝐬 𝐚𝐮𝐫 𝐚𝐩𝐧𝐚 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐟𝐞𝐞𝐝𝐛𝐚𝐜𝐤 𝐥𝐚𝐳𝐦𝐢 𝐬𝐡𝐚𝐫𝐞 𝐤𝐚𝐫𝐞𝐢𝐧 𝐭𝐚𝐚𝐤𝐞 𝐚𝐚𝐩𝐤𝐨 𝐦𝐚𝐳𝐞𝐞𝐝 𝐛𝐞𝐡𝐭𝐚𝐫 𝐠𝐮𝐢𝑑𝐚𝐧𝐜𝐞 𝐚𝐮𝐫 𝟐𝟒/𝟕 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐤𝐢𝐲𝐚 𝐣𝐚 𝐬𝐚𝐤𝐞.\n\n"
            f"𝟑. 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐒𝐞𝐬𝐬𝐢𝐨𝐧𝐬 & 𝐋𝐨𝐬𝐬 𝐑𝐞𝐜𝐨𝐯𝐞𝐫𝐲:\n"
            f"📈 𝐀𝐠𝐚𝐫 𝐚𝐚𝐩𝐤𝐞 𝐩𝐮𝐫𝐚𝐧𝐞 𝐥𝐨𝐬𝐬𝐞𝐬 𝐡𝐚𝐢𝐧, 𝐭𝐨𝐡 𝐡𝐚𝐦𝐚𝐫𝐞 𝐩𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐫𝐞𝐜𝐨𝐯𝐞𝐫𝐲 𝐬𝐞𝐬𝐬𝐢𝐨𝐧𝐬 𝐚𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧𝐬 𝐤𝐞 𝐳𝐚𝐫𝐢𝐲𝐞 𝐚𝐩𝐧𝐚 𝐩𝐨𝐫𝐭𝐟𝐨𝐥𝐢𝐨 𝐟𝐚𝐬𝐭 𝐫𝐞𝐜𝐨𝐯𝐞𝐫 𝐤𝐚𝐫 𝐬𝐚𝐤𝐭𝐞 𝐡𝐚𝐢𝐧! 💯🚀\n\n"
            f"𝟒. 𝐕𝐈𝐏 𝐉𝐨𝐢𝐧 𝐒𝐲𝐬𝐭𝐞𝐦 & 𝐄𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐑𝐞𝐰𝐚𝐫𝐝𝐬:\n"
            f"💎 𝐕𝐈𝐏 𝐦𝐞𝐦𝐛𝐞𝐫𝐬𝐡𝐢𝐩 𝐡𝐚𝐬𝐢𝐥 𝐤𝐚𝐫𝐧𝐞 𝐤𝐞 𝐥𝐢𝐲𝐞 𝐧𝐞𝐞𝐜𝐡𝐞 𝐝𝐢𝐲𝐞 𝐠𝐚𝐲𝐞 𝐨𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐥𝐢𝐧𝐤 𝐬𝐞 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐛𝐚𝐧𝐚𝐲𝐞𝐢𝐧, 𝐝𝐞𝐩𝐨𝐬𝐢𝐭 𝐤𝐚𝐫𝐞𝐢𝐧 𝐚𝐮𝐫 𝐚𝐩𝐧𝐢 𝐓𝐫𝐚𝐝𝐞𝐫 𝐈𝐃 𝐛𝐡𝐞𝐣𝐞𝐢𝐧 𝐭𝐚𝐚𝐤𝐞 𝐚𝐚𝐩𝐤𝐨 𝐟𝐫𝐞𝐞 𝐬𝐭𝐚𝐫𝐬 𝐚𝐮𝐫 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐞𝐬𝐬 𝐦𝐢𝐥 𝐬𝐚𝐤𝐞.\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🎯 𝐒𝐭𝐞𝐩 𝟏: 𝐂𝐫𝐞𝐚𝐭𝐞 𝐑𝐞𝐜𝐨𝐯𝐞𝐫𝐲 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 (𝐐𝐮𝐨𝐭𝐞𝐱)\n"
            f"🔗 https://broker-qx.pro/?lid=1614510\n\n"
            f"🏦 𝐒𝐭𝐞ፕ 𝟐: 𝐒𝐞𝐧𝐝 𝐓𝐫𝐚𝐝𝐞𝐫 𝐈𝐃 𝐟𝐨𝐫 𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐈𝐏 𝐀𝐜𝐜𝐞𝐬𝐬!\n"
            f"👉 𝐃𝐌 𝐎𝐰𝐧𝐞𝐫: @MK_TRADER586\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👑 𝐌.𝐊 𝐓𝐑𝐀𝐃𝐄𝐑 | 𝐕𝐈𝐏 𝐙𝐎𝐍𝐄 ⚡"
        )
        
        keyboard = [
            [InlineKeyboardButton("🚀 𝐉𝐎𝐈𝐍 𝐕𝐈𝐏 & 𝐂𝐑𝐄𝐀𝐓𝐄 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 🚀", url="https://broker-qx.pro/?lid=1614510")],
            [
                InlineKeyboardButton("📈 𝐋𝐨𝐬𝐬 𝐑𝐞𝐜𝐨𝐯𝐞𝐫𝐲", callback_data="btn_recovery"),
                InlineKeyboardButton("🎯 𝐒𝐞𝐬𝐬𝐢𝐨𝐧𝐬 𝐑𝐮𝐥𝐞𝐬", callback_data="btn_sessions")
            ],
            [
                InlineKeyboardButton("💬 𝐒𝐞𝐧𝐝 𝐅𝐞𝐞𝐝𝐛𝐚𝐜𝐤", callback_data="btn_feedback"),
                InlineKeyboardButton("👑 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫", url="https://t.me/MK_TRADER586")
            ]
        ]
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=PHOTO_URL,
            caption=welcome_caption,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(f"Welcome post error: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "btn_recovery":
        text = (
            f"📈 𝐏𝐄𝐑𝐒𝐎𝐍𝐀𝐋 𝐋𝐎𝐒𝐒 𝐑𝐄𝐂𝐎𝐕𝐄𝐑𝐘 𝐙𝐎𝐍𝐄 💯\n\n"
            f"Agar aapka purana loss ho chuka hai, toh pareshan hone ki koi zaroorat nahi hai! Humare VIP recovery sessions join karein.\n\n"
            f"🎯 Recovery Steps:\n"
            f"1. Naya account is link se banayein:\n🔗 https://broker-qx.pro/?lid=1614510\n"
            f"2. Deposit karein aur apni Trader ID note karein.\n"
            f"3. Foran owner ko DM karein VIP access ke liye:\n👉 @MK_TRADER586"
        )
        await query.message.reply_text(text)
        
    elif data == "btn_sessions":
        text = (
            f"🎯 𝐒𝐄𝐒𝐒𝐈𝐎𝐍𝐒 𝐅𝐎𝐋𝐋𝐎𝐖 𝐊𝐀𝐑𝐍𝐀𝐘 𝐊𝐀 𝐓𝐀𝐑𝐄𝐄𝐐𝐀 📊\n\n"
            f"✅ Hamesha time par session join karein.\n"
            f"✅ Stop-loss aur proper risk management lazmi follow karein.\n"
            f"✅ Over-trading bilkul na karein.\n"
            f"✅ Signals milte hi fast execution rakhein taake 100% profit gain ho sake! 🚀"
        )
        await query.message.reply_text(text)
        
    elif data == "btn_feedback":
        text = (
            f"💬 𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐕𝐀𝐋𝐔𝐀𝐁𝐋𝐄 𝐅𝐄𝐄𝐃𝐁𝐀𝐂𝐊 ⭐\n\n"
            f"Aapka feedback hamare liye bohot ahem hai! Apne profit ke screenshots, trade results, aur reviews seedha yahan send karein:\n\n"
            f"👉 DM Owner for Feedback: @MK_TRADER586"
        )
        await query.message.reply_text(text)

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await send_data_to_log_channel(update, context, "Channel Join Request Accepted")
    await send_welcome_post(user.id, user, context)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_data_to_log_channel(update, context, "Bot /start Command")
    await send_welcome_post(user.id, user, context)

async def broadcast_announcement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_chat and update.effective_chat.id == ANNOUNCEMENT_CHANNEL_ID:
            if not os.path.exists(USERS_FILE):
                return
            with open(USERS_FILE, "r") as f:
                users = f.read().splitlines()
            success_count = 0
            for user_id in users:
                try:
                    await update.message.copy(chat_id=int(user_id))
                    success_count += 1
                    await asyncio.sleep(0.05)
                except Exception as e:
                    print(f"Failed to send to {user_id}: {e}")
            print(f"Broadcast completed! Sent to {success_count} users.")
    except Exception as e:
        print(f"Broadcast error: {e}")

async def handle_web(request):
    return web.Response(text="M.K Trader Bot is running 24/7!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_web)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Chat(chat_id=ANNOUNCEMENT_CHANNEL_ID) & ~filters.COMMAND, broadcast_announcement))

    # Start web server for Render port check
    await start_web_server()

    print("𝐌.𝐊 𝐓𝐑𝐀𝐃𝐄𝐑 Bot is starting polling...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
