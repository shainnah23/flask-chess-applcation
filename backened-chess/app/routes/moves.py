from flask import Blueprint, request, jsonify
from app.db import db
from app.models import Game, Moves
from app.chess_app.pieces import GameManager
from flask_jwt_extended import jwt_required, get_jwt_identity


moves_bp = Blueprint("moves", __name__)

@moves_bp.route("/<int:game_id>", methods=["POST"])
@jwt_required()
def make_move(game_id):
    
    current_user_id = int(get_jwt_identity()) 
    
    data = request.get_json()
    player = data.get("player")
    from_x = data.get("from_x") - 1
    from_y = data.get("from_y") - 1
    to_x = data.get("to_x") - 1
    to_y = data.get("to_y") - 1

    print(f"Player move: {player} from ({from_x},{from_y}) to ({to_x},{to_y})")

    game = Game.query.get(game_id)
    if not game or game.user_id != current_user_id: 
        return jsonify({"error": "Unauthorized or game not found"}), 400

    game_manager = GameManager(game_id, player_color="white")
    game_manager.load_state(game.game_state)


    result = game_manager.execute_player_move(from_x, from_y, to_x, to_y, player)
    success = result.get("success") if result else False

    if not success:
        error_msg = result.get("error") if result else "No result returned"
        print(f"Move failed: {error_msg}")
        return jsonify({"error": error_msg}), 400

    game.game_state = game_manager.board.to_json()
    game.game_status = game_manager.game_status
    game.winner = ""

    player_move = result.get("move")

    move = Moves(

        game_id=game_id,
        player=player,
        from_square=f"{from_x},{from_y}",
        to_square=f"{to_x},{to_y}",
        game_state_after=game.game_state
    )
    db.session.add(move)

    ai_move = None
    if game_manager.current_turn == "blue":
        print("Executing AI move...")
        ai_result = game_manager.execute_ai_move()
        ai_success = ai_result.get("success") if ai_result else False

        if ai_success:
            game.game_state = game_manager.board.to_json()
            game.game_status = game_manager.game_status
            game.winner = ""

            ai_move = ai_result.get("move")

            ai_move_record = Moves(
                game_id=game_id,
                player="blue",
                from_square=f"{ai_move['from']['x']},{ai_move['from']['y']}",
                to_square=f"{ai_move['to']['x']},{ai_move['to']['y']}",
                game_state_after=game.game_state
            )
            db.session.add(ai_move_record)

            print(f"AI moved: {ai_move}")
        else:
            error = ai_result.get("error") if ai_result else "ai failed to move"
            print(f"AI move failed: {error}")

    db.session.commit()

    return jsonify({
        "message": "Move executed",
        "player_move": player_move,
        "ai_move": ai_move,
        "game_state": game.game_state,
        "current_turn": game_manager.current_turn,
    }), 201