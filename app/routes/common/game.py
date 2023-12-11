from flask import Blueprint, request, jsonify, session
from app.models import User, GameData
from app.extensions import db

game = Blueprint('game', __name__)

@game.route("/save_game_data", methods=["POST"])
def save_game_data():
    data = request.get_json()
    game_data = GameData(
        user_id = session["_user_id"],
        game_name = data["game_name"],
        time_start = data["time_start"],
        # play_duration = data["play_duration"],
        last_score = data["last_score"],
        # status = data["status"]
    )

    user = User.query.get(game_data.user_id)

    if user:
        high_score_col = f"high_score_{game_data.game_name}"
        if game_data.last_score > getattr(user, high_score_col):
            setattr(user, high_score_col, game_data.last_score)
    db.session.add(game_data)
    db.session.commit()
    return jsonify(message="Game data stored successfully")
