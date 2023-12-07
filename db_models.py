from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Interval, Integer, ForeignKey
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True, nullable=False)
    password = Column(String(15), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User (username='{self.username}', date_added='{self.date_added}')>"


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
