import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.error import BadRequest

BOT_TOKEN = os.environ.get("8226668423:AAFR7Te5Oz7-zh84CI1ujruZkzfAwnc01v8")
REQUIRED_CHANNELS = ["@hawksdb", "@hawksdb", "@hawksdb"]

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    not_joined = []

    for channel in REQUIRED_CHANNELS:
        try:
            member = context.bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except BadRequest:
            not_joined.append(channel)

    if not_joined:
        keyboard = [[InlineKeyboardButton(ch, url=f"https://t.me/{ch.strip('@')}")] for ch in not_joined]
        keyboard.append([InlineKeyboardButton("I have joined", callback_data="joined")])
        update.message.reply_text(
            "📢 Please join the required channels below and then press 'I have joined':",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        main_menu(update, context)

def main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Login", callback_data="login")],
        [InlineKeyboardButton("Claim Your MB", callback_data="claim")]
    ]
    if update.callback_query:
        update.callback_query.edit_message_text(
            "✅ You have joined all required channels.\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        update.message.reply_text(
            "✅ You have joined all required channels.\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "joined":
        start(update, context)
    elif query.data == "login":
        query.edit_message_text("🔑 Please enter your login details...")
    elif query.data == "claim":
        query.edit_message_text("🎁 Claim process started...")

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
