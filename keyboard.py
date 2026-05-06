from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def quality_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("360p 🎥", callback_data="360"),
            InlineKeyboardButton("720p 🔥", callback_data="720"),
        ],
        [
            InlineKeyboardButton("MP3 🎧", callback_data="audio")
        ]
    ])
