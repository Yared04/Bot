from telebot import TeleBot, types
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the token and web URL from the environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        "Open Mini App",
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(button)
    bot.send_message(message.chat.id, "Click the button below to launch the Mini App and create a post:", reply_markup=markup)
       
bot.polling()
