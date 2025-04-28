from functools import wraps
from telebot import types
from models.user import User

def is_authorized(user_id):
    """Check if a user is authorized to use the bot"""
    return User.is_authorized(user_id)

def require_authorization(func):
    """Decorator to check if a user is authorized"""
    @wraps(func)
    def wrapper(message: types.Message, *args, **kwargs):
        if not is_authorized(message.from_user.id):
            return "❌ You're not authorized to use this bot. Contact @yared_04 for access."
        return func(message, *args, **kwargs)
    return wrapper 