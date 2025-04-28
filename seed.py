from app import app, db
from models.user import User

def add_admin_user(telegram_id, username, first_name, last_name):
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(telegram_id=telegram_id).first()
        if existing_user:
            print(f"User {telegram_id} already exists!")
            return
        
        # Create new admin user
        admin_user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user {telegram_id} added successfully!")

if __name__ == "__main__":
    # Replace these values with your actual Telegram user information
    add_admin_user(
        telegram_id=366965858,  # Your Telegram ID
        username="yared_04",    # Your Telegram username
        first_name="Yared",     # Your first name
        last_name=""           # Your last name (if any)
    ) 