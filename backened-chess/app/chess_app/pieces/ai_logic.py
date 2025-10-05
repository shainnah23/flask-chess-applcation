from .move import MoveLogic
import random

class AILogic:
    def __init__(self, color):
        self.color = color

    def get_all_possible_moves(self, board):
        moves = []
        for y in range(8):
            for x in range(8):
                piece = board.board[y][x]
                if piece and piece._color == self.color:
                    for move in piece.valid_moves(board):
                        moves.append((piece, move))
        return moves

    def choose_move(self, board):
        all_moves = self.get_all_possible_moves(board)
        if not all_moves:
            print(f"No valid moves for {self.color}")
            return None
        return random.choice(all_moves)