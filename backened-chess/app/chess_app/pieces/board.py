from .pawn import Pawn
from .rook import Rook
from .bishop import Bishop
from .queen import Queen
from .knight import Knight
from .king import King
import json

class Board:

    blue_pieces = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]  
    white_pieces = ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]  
    blue_pawn = "♟"
    white_pawn = "♙"

    def __init__(self, color):
        
        self.board = []
        self._color = color

        for i in range(8):
            y = []
            for j in range(8):
                y.append(None)
            self.board.append(y)

    def display_board(self):
        print("       1         2          3          4          5          6           7         8")
        print("  ---------" * 8)
    
        for i in range(8):
            y = self.board[i]
            display_row = []
        
            for square in y:
                if square is None:
                    display_row.append("|        |")
                elif isinstance(square, Pawn):
                    display_row.append(f"|   {square.symbol}    |")
                elif isinstance(square, (Rook, Bishop, Knight, Queen, King)):
                    display_row.append(f"|   {square.symbol}    |")    
                else:
                    display_row.append(square)
        
            print(f"{8-i}:{' '.join(display_row)}")
            print("  ---------" * 8)
    
        print("       1         2          3          4          5          6           7         8")

    def display_pieces(self):
        

        self.board[0][0] = Rook("blue", 0, 0)
        self.board[0][1] = Knight("blue", 1, 0)  
        self.board[0][2] = Bishop("blue", 2, 0)
        self.board[0][3] = Queen("blue", 3, 0) 
        self.board[0][4] = King("blue", 4, 0)
        self.board[0][5] = Bishop("blue", 5, 0)
        self.board[0][6] = Knight("blue", 6, 0)
        self.board[0][7] = Rook("blue", 7, 0)
        

        for i in range(8):
            self.board[1][i] = Pawn("blue", i, 1)
        

        for i in range(8):
            self.board[6][i] = Pawn("white", i, 6)
            
        self.board[7][0] = Rook("white", 0, 7)
        self.board[7][1] = Knight("white", 1, 7)  
        self.board[7][2] = Bishop("white", 2, 7)
        self.board[7][3] = Queen("white", 3, 7)  
        self.board[7][4] = King("white", 4, 7)  
        self.board[7][5] = Bishop("white", 5, 7)
        self.board[7][6] = Knight("white", 6, 7)  
        self.board[7][7] = Rook("white", 7, 7)

    def is_inbounds(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        else:
            return False

    def is_square_empty(self, x, y):
        return self.is_inbounds(x, y) and self.board[y][x] is None

    def is_enemy_piece(self, color, x, y):
        if not self.is_inbounds(x, y) or self.is_square_empty(x, y):
            return False
        piece = self.board[y][x]
        
        if hasattr(piece, '_color'):
            return piece._color != color
        return False

    def get_piece(self, x, y):
        board_x = x - 1 
        board_y = 8 - y
        
        if not self.is_inbounds(board_x, board_y):
            return None
        
        return self.board[board_y][board_x]
    
    def find_piece_coords(self, target_piece):
        for y, row in enumerate(self.board):  
            for x, piece in enumerate(row):
                if piece == target_piece:
                    return (x, y)
        return None



    def to_json(self):
        board_pieces = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None:
                    board_pieces.append({
                        "type": type(piece).__name__,
                        "color": piece._color,
                        "x": x,
                        "y": y
                    })
        return json.dumps(board_pieces)

    def from_json(self, data):

        pieces= {
            "Pawn": Pawn,
            "Rook": Rook,
            "Bishop": Bishop,
            "Queen": Queen,
            "Knight": Knight,
            "King": King
        }

        pieces_data = json.loads(data)
        
    
        self.board = [[None for y in range(8)] for x in range(8)]

        for piece_info in pieces_data:

            piece_type = piece_info["type"]
            color = piece_info["color"]
            x = piece_info["x"]
            y = piece_info["y"]
            
            piece_class= pieces.get(piece_type)

            if piece_class:
                self.board[y][x] = piece_class(color, x, y)