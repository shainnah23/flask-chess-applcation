class Queen:
    
    white_queen = "♕"
    blue_queen = "♛"
    def __init__(self,color,x,y):
        self.x = x
        self.y = y
        self._color = color
        if color == "white":
            self.symbol = self.white_queen
        else:
            self.symbol = self.blue_queen

    def valid_moves(self, board):
        moves = []
        directions = [
            (0, 1), (0, -1),
            (1, 0), (-1, 0),
            (1, 1), (1, -1),
            (-1, 1), (-1, -1)
        ]
        for direction in directions:
            moves.extend(self._get_moves_in_direction(board, direction))
        return moves

    def _get_moves_in_direction(self, board, direction):
        moves = []
        for step in range(1, 8):
            new_x = self.x + direction[0] * step
            new_y = self.y + direction[1] * step

            if not (0 <= new_x < 8 and 0 <= new_y < 8):
                break

            piece_at_square = board.board[new_y][new_x]
            if piece_at_square is not None:
                if piece_at_square._color != self._color:
                    moves.append((new_x, new_y))
                break

            moves.append((new_x, new_y))

        return moves
    def move(self, new_x, new_y, board):
        valid_moves = self.valid_moves(board)
        if (new_x, new_y) not in valid_moves:
            print(f"Invalid move! Valid moves are: {valid_moves}")
            return False

        board.board[self.y][self.x] = None
        self.x, self.y = new_x, new_y
        board.board[new_y][new_x] = self
        print(f"Moved Queen to ({new_x}, {new_y})")
        return True    