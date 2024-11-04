import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your bot token or set it as an environment variable in Vercel
BOT_TOKEN = os.getenv("BOT_TOKEN", "8090790327:AAGmgV4EmrKWqndCp056Hz8bSyyBhfd5U4Y")
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dp.process_update(update)
        return "ok", 200

def start(update: Update, context) -> None:
    """Sends a message when the /start command is issued."""
    update.message.reply_text("Welcome! Send me a video link, and I'll show it to you using the Terabox video downloader.")

def handle_url(update: Update, context) -> None:
    """Handles user input URL and returns the processed video link."""
    user_url = update.message.text
    if user_url.startswith("http"):
        video_url = f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={user_url}"
        update.message.reply_text(
            f"Here is your video link:\n{video_url}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Open Video", url=video_url)]
            ])
        )
    else:
        update.message.reply_text("Please send a valid URL starting with http or https.")

if __name__ == "__main__":
    from telegram.ext import CallbackContext

    dp = Dispatcher(bot, None, workers=0)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_url))

    # Set the webhook URL to your Vercel app's URL
    bot.set_webhook('https://your-vercel-app.vercel.app/webhook')

    app.run(port=8443)
