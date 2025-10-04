class Rook:
    
    white_rook = "♖"
    blue_rook = "♜"

    def __init__(self, color, x, y):
        self._color = color
        self.x = x
        self.y = y
        if color == "white" :
            self.symbol = self.white_rook
        else:
            self.symbol=self.blue_rook

        self.has_moved = False

    def valid_moves(self, board):
        valid_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 

        for dx, dy in directions:
            new_x, new_y = self.x, self.y
            while True:
                new_x = new_x + dx
                new_y = new_y + dy
                if not board.is_inbounds(new_x, new_y):
                    break
                if board.is_square_empty(new_x, new_y):
                    valid_moves.append((new_x, new_y))
                elif board.is_enemy_piece(self._color, new_x, new_y):
                    valid_moves.append((new_x, new_y))
                    break
                else:
                    break
        return valid_moves

    def move(self, new_x, new_y, board):
        valid_moves = self.valid_moves(board)
        if (new_x, new_y) not in valid_moves:
            print(f"Invalid move! Valid moves are: {valid_moves}")
            return False

        board.board[self.y][self.x] = None
        self.x = new_x
        self.y = new_y
        self.has_moved = True
        board.board[new_y][new_x] = self
        print(f"Moved rook to ({new_x}, {new_y})")
        return True