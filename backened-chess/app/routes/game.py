from flask import Blueprint, request, jsonify
from app.db import db
from app.models import Game
from app.chess_app.pieces import GameManager

game_bp = Blueprint("game", __name__)

@game_bp.route("/create", methods=["POST"])
def create_game():

    user_id = request.json.get("user_id")  

    existing_game = Game.query.filter_by(user_id=user_id, game_status="active").first()

    if existing_game:
        return jsonify({
            "success": True,
            "game_id": existing_game.id,
            "game_state": existing_game.game_state,
            "message": "Game returned"
        }), 200

    manager = GameManager(game_id=None)
    initial_state = manager.board.to_json()


    new_game = Game(

        user_id=user_id,
        game_status="active",
        winner="",
        game_state=initial_state
    )

    db.session.add(new_game)
    db.session.commit()

    return jsonify({

        "success": True,
        "game_id": new_game.id,
        "game_state": initial_state,
        "message": "New game created"
    }), 201

@game_bp.route("/game/<int:id>", methods=["GET"])
def get_game(id):
    
    game = Game.query.get(id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    return jsonify({
        "game_id": game.id,
        "game_status": game.game_status,
        "winner": game.winner,
        "game_state": game.game_state
    }), 200