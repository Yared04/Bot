from sqlalchemy import Column, Integer, String, Boolean
from models.base import BaseModel
from database import db

class User(BaseModel):
    __tablename__ = 'users'
    
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"
    
    @classmethod
    def is_authorized(cls, telegram_id):
        """Check if a user is authorized to use the bot"""
        return db.session.query(cls).filter_by(
            telegram_id=telegram_id,
            is_active=True
        ).first() is not None 