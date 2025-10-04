class Knight:

    white_knight = "♘"
    blue_knight = "♞"

    def __init__(self,color,x,y):

        self._color=color
        self.x= x
        self.y = y
        self.has_moved = False

        if color == "white":
            self.symbol =self.white_knight
        else:
            self.symbol =self.blue_knight
    
    def valid_moves(self,board):
        x,y = self.x,self.y

        all_moves = [
            (x+2, y+1),(x+2, y-1),
            (x-2, y+1),(x-2, y-1),
            (x+1, y+2),(x+1, y-2),
            (x-1, y+2),(x-1, y-2),
        ]
        valid_moves=[]
        for nx, ny in all_moves:
            if 0 <= nx < 8 and 0 <= ny < 8 :
                piece = board.board[ny][nx]
                if piece is None or piece._color != self._color:
                    valid_moves.append((nx,ny))

        return valid_moves
    
    def move(self, new_x, new_y, board):
        valid_moves = self.valid_moves(board)
        if (new_x, new_y) not in valid_moves:
            print(f"Invalid move! Valid moves are: {valid_moves}")
            return False

        board.board[self.y][self.x] = None
        self.x, self.y = new_x, new_y
        board.board[new_y][new_x] = self
        print(f"Moved Knight to ({new_x}, {new_y})")
        return True