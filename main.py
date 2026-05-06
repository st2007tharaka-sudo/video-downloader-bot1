import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from config import BOT_TOKEN
from downloader import download_video
from keyboard import quality_keyboard
from utils import clean_file

# create downloads folder
if not os.path.exists("downloads"):
    os.makedirs("downloads")

user_links = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Send me a video link!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_links[update.message.chat_id] = url

    await update.message.reply_text(
        "🎯 Choose quality:",
        reply_markup=quality_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    quality = query.data
    chat_id = query.message.chat_id
    url = user_links.get(chat_id)

    await query.edit_message_text("⏳ Downloading...")

    try:
        file_path = download_video(url, quality)

        if quality == "audio":
            await context.bot.send_audio(chat_id, audio=open(file_path, "rb"))
        else:
            await context.bot.send_video(chat_id, video=open(file_path, "rb"))

        clean_file(file_path)

    except Exception as e:
        await context.bot.send_message(chat_id, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Bot Running...")
    app.run_polling()
