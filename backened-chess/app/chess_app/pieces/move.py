class MoveLogic:
    def __init__(self, board):
        self.board = board

    def is_valid_move(self, piece, target_pos):
        # Check if a move is valid for the given piece.
        valid_moves = piece.valid_moves(self.board)
        return target_pos in valid_moves

    def execute_move(self, piece, move):
        new_x, new_y = move
        return piece.move(new_x, new_y, self.board)


    def get_all_moves_for_piece(self, piece):
        # Return all valid moves for a given piece.
        return piece.valid_moves(self.board)

    def get_all_moves_for_color(self, color):
        # Return all valid moves for all pieces of a given color.
        moves = []
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece._color == color:
                    for move in piece.valid_moves(self.board):
                        moves.append((piece, move))
        return moves