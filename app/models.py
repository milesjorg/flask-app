from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, DateTime, Interval, Integer, ForeignKey
from datetime import datetime
from app.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    high_score_flappybird = Column(Integer, default=0)

    def __repr__(self):
        return f"<User (username='{self.username}', date_added='{self.date_added}')>"
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return True
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameData(db.Model):
    __tablename__ = "scoreboard"
    game_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    game_name = Column(String(255))
    time_start = Column(DateTime, default=datetime.utcnow)
    play_duration = Column(Interval)
    last_score = Column(Integer)
    high_score = Column(Integer)
    status = Column(String(255))
