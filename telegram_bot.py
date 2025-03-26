from flask import Flask, request
from telebot import TeleBot, types
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = TeleBot(TOKEN)

app = Flask(__name__)

# Set Webhook
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    success = bot.set_webhook(url=f"{WEBHOOK_URL}webhook")
    return "Webhook set!" if success else "Webhook setup failed!", 200

# Telegram will send updates here
@app.route("/webhook", methods=["POST"])
def receive_update():
    update = request.get_data().decode("utf-8")
    bot.process_new_updates([types.Update.de_json(update)])
    return "OK", 200

# Start command handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Open Mini App", web_app=types.WebAppInfo(url=WEB_APP_URL))
    markup.add(button)
    bot.send_message(message.chat.id, "Click the button below to launch the Mini App and create a post:", reply_markup=markup)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
