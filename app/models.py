from __future__ import annotations
from typing import List

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, ForeignKey, ARRAY, String
from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    date_added: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    game_data: Mapped[List["GameData"]] = relationship(back_populates="user")

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
    __tablename__ = "base_game_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    time_start: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="game_data")
    racer: Mapped["GameDataRacer"] = relationship(back_populates="base_data")
    flappybird: Mapped["GameDataFlappybird"] = relationship(back_populates="base_data")


class GameDataRacer(GameData):
    __tablename__ = "racer"
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("base_game_data.id"))
    lap_splits: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    top_speed: Mapped[float] = mapped_column()
    place_finished: Mapped[str] = mapped_column()
    # play_duration: Mapped[] = Column(Interval)

    base_data: Mapped["GameData"] = relationship(
        back_populates="racer", single_parent=True
    )


class GameDataFlappybird(GameData):
    __tablename__ = "flappybird"
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("base_game_data.id"))
    score: Mapped[int] = mapped_column()
    high_score: Mapped[int] = mapped_column()

    base_data: Mapped["GameData"] = relationship(
        back_populates="flappybird", single_parent=True
    )
