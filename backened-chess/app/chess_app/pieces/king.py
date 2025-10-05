class King:

    def __init__(self, color,x,y):
        self._color = color
        self.x = x
        self.y = y
        if color == "white":
            self.symbol = "♔"
        else:
            self.symbol = "♚"

    def valid_moves(self,board):
        valid_moves = []
        directions = [
             (-1, 0), (0, -1), (0, 1), (1, 0)
        ]
        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy
            if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                piece = board.board[ny][nx]
                if piece is None or piece._color != self._color:
                    valid_moves.append((nx, ny))
        return valid_moves
    
    def move(self, new_x, new_y, board):
        valid_moves = self.valid_moves(board)
        if (new_x, new_y) not in valid_moves:
            print(f"Invalid move! Valid moves are: {valid_moves}")
            return False

        board.board[self.y][self.x] = None
        self.x, self.y = new_x, new_y
        board.board[new_y][new_x] = self
        print(f"Moved King to ({new_x}, {new_y})")
        return True