class Pawn:
    white_pawn = "♙"
    blue_pawn = "♟"
    start_row_white = 6
    start_row_black = 1
    
    def __init__(self, color, x, y):
        self._color = color
        self.x = x
        self.y = y
        self.has_moved = False

        if color == "white":
            self.symbol = self.white_pawn
        else:
            self.symbol = self.blue_pawn
    
    def display_pawn(self):

        if self._color == "white":

            print(f"{self.white_pawn}")
        else:
            print(f"{self.blue_pawn}")

    def valid_moves(self, board):
        movements = []

        if self._color == "white":
            direction = -1
            start_y = self.start_row_white
        else:
            direction = 1
            start_y = self.start_row_black

        new_y = self.y + direction

        if board.is_inbounds(self.x, new_y) and board.is_square_empty(self.x, new_y):
            movements.append((self.x, new_y))

        if self.y == start_y:
            new_y_two = self.y + 2 * direction
            if board.is_inbounds(self.x, new_y_two) and board.is_square_empty(self.x, new_y_two):
                movements.append((self.x, new_y_two))

        for dx in [-1, 1]:
            target_x = self.x + dx
            target_y = self.y + direction
            if board.is_inbounds(target_x, target_y) and board.is_enemy_piece(self._color, target_x, target_y):
                movements.append((target_x, target_y))

        return movements        
    
    def move(self, new_x, new_y, board):

        valid_moves = self.valid_moves(board)

        if (new_x, new_y) not in valid_moves:
            print(f"Invalid move! Valid moves are: {valid_moves}")
            return False
        
        # Clear current position

        board.board[self.y][self.x] = None
        
        # Update pawn position

        prev_x, prev_y = self.x, self.y
        self.x = new_x
        self.y = new_y
        self.has_moved = True
        
        # Place pawn in new position

        board.board[new_y][new_x] = self
        
        print(f"Moved pawn from ({prev_x}, {prev_y}) to ({new_x}, {new_y})")
        return True