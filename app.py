from flask import Flask, request
from telebot import TeleBot, types
from dotenv import load_dotenv
import os
from database import init_db, db
from models.user import User
from auth import require_authorization

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# Initialize database
init_db(app)

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
@require_authorization
def send_welcome(message):
    user_id = message.from_user.id
    mini_app_url = f"{WEB_APP_URL}?client_id={user_id}"
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Open Mini App", web_app=types.WebAppInfo(url=mini_app_url))
    markup.add(button)
    bot.send_message(message.chat.id, "Click the button below to launch the Mini App and create a post:", reply_markup=markup)

# Return user's data
@bot.message_handler(commands=["me"])
@require_authorization
def send_user_data(message):
    user_data = message.from_user
    formatted_message = (
        f"🆔 ID: {user_data.id}\n"
        f"👤 Username: @{user_data.username if user_data.username else 'N/A'}\n"
        f"📛 Name: {user_data.first_name} {user_data.last_name or ''}\n"
    )
    bot.send_message(message.chat.id, formatted_message)

# Admin command to add new users
@bot.message_handler(commands=["add_user"])
def add_user(message):
    # Check if the command sender is an admin
    if not User.is_authorized(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ You don't have permission to use this command.")
    
    try:
        # The command should be in the format: /add_user <telegram_id>
        _, telegram_id = message.text.split()
        telegram_id = int(telegram_id)
        
        # Create new user
        new_user = User(
            telegram_id=telegram_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        bot.send_message(message.chat.id, f"✅ User {telegram_id} has been added successfully!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error adding user: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
