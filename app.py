import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext

# Your actual bot token
BOT_TOKEN = "8090790327:AAGmgV4EmrKWqndCp056Hz8bSyyBhfd5U4Y"
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)
dp = Dispatcher(bot, None, workers=0)

# Set the webhook automatically when the app starts
def set_webhook():
    webhook_url = "https://telegram-bot-crackroach7js-projects.vercel.app/webhook"
    bot.setWebhook(webhook_url)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        dp.process_update(update)
    except Exception as e:
        print(f"Error: {e}")  # Log error to Vercel logs
        return "Error occurred", 500
    return "ok", 200

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message when the /start command is issued."""
    update.message.reply_text("Welcome! Send me a video link, and I'll show it to you using the Terabox video downloader.")

def handle_url(update: Update, context: CallbackContext) -> None:
    """Handles user input URL and returns the processed video link."""
    user_url = update.message.text
    if user_url.startswith("http"):
        video_url = f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={user_url}"
        update.message.reply_text(f"Here is your video link:\n{video_url}")
    else:
        update.message.reply_text("Please send a valid URL starting with http or https.")

# Add handlers for commands and messages
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_url))

# Set the webhook when the application starts
set_webhook()

if __name__ == "__main__":
    app.run()
