from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, ARRAY, Float, DateTime, Interval, Integer, ForeignKey
from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

    game_data = relationship('GameData', back_populates='user')

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
    __tablename__ = 'base_game_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(255))
    time_start = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='game_data')

class GameDataRacer(GameData):
    __tablename__ = 'racer'
    lap_splits = Column(ARRAY(String))
    top_speed = Column(Float)
    place_finished = Column(String)
    play_duration = Column(Interval)

    base_data = relationship('GameData', back_populates='user')

class GameDataFlappybird(GameData):
    __tablename__ = 'flappybird'
    score = Column(Integer)
    high_score = Column(Integer)

    base_data = relationship('GameData', back_populates='user')