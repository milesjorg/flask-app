from flask import Blueprint, request, jsonify, session
from app.models import User, GameData, GameDataRacer, GameDataFlappybird
from app.extensions import db

game = Blueprint('game', __name__)

@game.route("/save_game_data/<game_name>", methods=["POST"])
def save_game_data(game_name):
    data = request.get_json()
    user_id = session["_user_id"]

    game = GameData.query.filter_by(game_name=game_name).first()

    if game:
        if game.game_name == "racer":
            game_data = GameDataRacer(
                user_id = user_id,
                game_id = game.game_id,
                lap_splits = data["lap_splits"],
                top_speed = data["top_speed"],
                place_finished = data["place_finished"],
            )

        db.session.add(game_data)
        db.session.commit()
        return jsonify(message="Game data stored successfully")
    
    # For setting high score
    # user = User.query.get(game_data.user_id)

    # if user:
    #     high_score_col = f"high_score_{game_data.game_name}"
    #     if game_data.last_score > getattr(user, high_score_col):
    #         setattr(user, high_score_col, game_data.last_score)
    # db.session.add(game_data)
    # db.session.commit()
    # return jsonify(message="Game data stored successfully")
