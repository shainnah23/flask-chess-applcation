import json
from .board import Board
from .move import MoveLogic
from .ai_logic import AILogic

class GameManager:

    def __init__(self, game_id, player_color="white"):
        self.game_id = game_id
        self.player_color = player_color
        self.ai_color = "blue"
        self.current_turn = "white"
        self.board = Board(player_color)
        self.board.display_pieces()
        self.move_logic = MoveLogic(self.board)
        self.ai = AILogic(self.ai_color)
        self.move_history = []
        self.game_status = "active"
        self.winner = None

    def get_state(self):
        return {
            "game_id": self.game_id,
            "board_state": self.board.to_json(),
            "current_turn": self.current_turn,
            "move_history": self.move_history,
            "game_status": self.game_status,
            "winner": self.winner
        }

    def load_state(self, game_state_json):
        self.board.from_json(game_state_json)

    def is_valid_turn(self, color):
        return self.current_turn == color

    def get_valid_moves_for_piece(self, x, y):
        if not self.board.is_inbounds(x, y):
            return []

        piece = self.board.board[y][x]
        if piece and piece._color == self.current_turn:
            return piece.valid_moves(self.board)
        return []
    
    def execute_move(self, piece, from_x, from_y, to_x, to_y, player_color):
        captured = self.board.board[to_y][to_x]
        self.move_logic.execute_move(piece, (to_x, to_y))
        captured_type = type(captured).__name__ if captured else None
        self.move_history.append({
            "from": {"x": from_x, "y": from_y},
            "to": {"x": to_x, "y": to_y},
            "player": player_color,
            "piece": type(piece).__name__,
            "captured": captured_type
        })
        self.switch_turn()

    def execute_player_move(self, from_x, from_y, to_x, to_y, player_color):
        if not self.is_valid_turn(player_color):
            return {
                "error": f"Not {player_color}'s turn",
                "current_turn": self.current_turn,
                "success": False
            }

        # Validate coordinates
        for c in (from_x, from_y, to_x, to_y):
            if c < 0 or c >= 8:
                return {
                    "error": "Coordinates out of bounds",
                    "success": False
                }

        piece = self.board.board[from_y][from_x]
        if not piece or piece._color != player_color:
            return {
                "error": f"No valid piece at position or piece doesn't belong to {player_color}", 
                "success": False
            }

        if not self.move_logic.is_valid_move(piece, (to_x, to_y)):
            return {
                "error": "Move is invalid", 
                "success": False
            }

        # Execute the move
        self.execute_move(piece, from_x, from_y, to_x, to_y, player_color)

        # After executing the move, update the turn to reflect the next player
        if player_color == "white":
            self.current_turn = "blue"  # It's now the AI's turn
        else:
            self.current_turn = "white"  # It's now the human player's turn

        # Prepare the response payload with detailed move info
        response = {
            "move": self.move_history[-1],  # The most recent move added to history
            "game_state": self.get_state(),  # Serialized board state after the move
            "success": True,  # Indicates the move was successfully executed
            "next_turn": self.current_turn  # Explicitly include who's up next
        }

        return response


    def execute_ai_move(self):
        if self.current_turn != self.ai_color:
            return {
                "error": "Not AI turn",
                "success": False
            }

        choice = self.ai.choose_move(self.board)
        if not choice:
            return {
                "error": "AI has no valid moves", 
                "success": False
            }

        piece, (to_x, to_y) = choice
        piece_current_position = self.board.find_piece_coords(piece)
        if not piece_current_position or not self.move_logic.is_valid_move(piece, (to_x, to_y)):
            return {
                "error": "Move invalid",
                "success": False
            }

        from_x, from_y = piece_current_position
        self.execute_move(piece, from_x, from_y, to_x, to_y, self.ai_color)
        return {
            "move": self.move_history[-1],
            "game_state": self.get_state(),
            "success": True
        }

    def switch_turn(self):
        if self.current_turn == "white":
            self.current_turn = "blue"
        else:
            self.current_turn = "white"