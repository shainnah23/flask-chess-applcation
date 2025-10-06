from flask import Blueprint, request, jsonify
from app.db import db
from app.models import Game
from app.chess_app.pieces import GameManager
from flask_jwt_extended import jwt_required, get_jwt_identity

game_bp = Blueprint("game", __name__)

@game_bp.route("/create", methods=["POST"])
@jwt_required()
def create_game():

    current_user_id = get_jwt_identity() 

    existing_game = Game.query.filter_by(user_id=current_user_id, game_status="active").first()

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

        user_id=current_user_id,
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
@jwt_required()
def get_game(id):
    current_user_id = get_jwt_identity()
    game = Game.query.get(id)

    if not game or game.user_id != current_user_id:
        return jsonify({"error": "Unauthorized or game not found"}), 400
    
    return jsonify({
        "game_id": game.id,
        "game_status": game.game_status,
        "winner": game.winner,
        "game_state": game.game_state
    }), 200