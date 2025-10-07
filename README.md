# Chess Game API

A full-featured chess game backend built with Flask, featuring an AI opponent, user authentication, and persistent game state management.

# Table of Contents
### Overview
### Features
### Installation
### API Endpoints
### Game Logic
### Database Models
### Chess Pieces
### Usage Examples
### Project Structure

## Overview

This is a backend chess application that allows users to play chess against an AI opponent. The game features complete chess rules implementation, move validation, game state persistence, and JWT-based authentication.

## Features

- User Authentication: Secure registration and login with JWT tokens
- AI Opponent: Random move AI opponent (blue pieces vs white pieces)
- Complete Chess Rules: All standard chess pieces with proper movement rules
- Game State Management: Persistent storage of game states and move history
- Game History: Complete move-by-move history tracking


## Technology Stack

- Framework: Flask
- Database: SQLAlchemy ORM
- Authentication: Flask-JWT-Extended
- Password Hashing: Flask-Bcrypt
- Game Engine: Custom Python chess implementation

## Installation

### Prerequisites

- Python 3.8+
- pip
- PostgreSQL/MySQL (or SQLite for development)

### Setup

#### 1. Clone the repository
```bash
git clone <https://github.com/shainnah23/flask-chess-applcation.git>
cd backened-chess
```

#### 2. Create a virtual environment
```bash
pipenv shell 
```

#### 3. Install dependencies
```bash
pipenv install
```

#### 4. Configure environment variables

**Mac/Linux:**
```bash
export FLASK_APP=app
export JWT_SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

**Windows:**
```cmd
set FLASK_APP=app
set JWT_SECRET_KEY=your-secret-key
set DATABASE_URL=your-database-url
```

#### 5. Run the application
```bash
piepenv main.py
```

---

## API Endpoints

### Authentication

#### Register User
```http
POST /users/add
Content-Type: application/json

{
  "username": "player1",
  "email": "player1@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "message": "Member added successfully",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "player1",
    "email": "player1@example.com",
    "created_at": "2025-10-07T10:30:00Z"
  }
}
```

#### Login
```http
POST /users/login
Content-Type: application/json

{
  "email": "player1@example.com",
  "password": "securepassword"
}
```

---

### Game Management

#### Create Game
```http
POST /game/create
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "game_id": 1,
  "game_state": "[{\"type\":\"Rook\",\"color\":\"blue\",\"x\":0,\"y\":0}...]",
  "message": "New game created"
}
```

#### Get Game
```http
GET /game/game/<game_id>
Authorization: Bearer <token>
```

---

### Making Moves

#### Execute Move
```http
POST /moves/<game_id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "player": "white",
  "from_x": 5,
  "from_y": 7,
  "to_x": 5,
  "to_y": 6
}
```

**Note:** Coordinates are 1-indexed (1-8) in the API request but converted to 0-indexed internally.

**Response:**
```json
{
  "message": "Move executed",
  "player_move": {
    "from": {"x": 4, "y": 6},
    "to": {"x": 4, "y": 5},
    "player": "white",
    "piece": "Pawn",
    "captured": null
  },
  "ai_move": {
    "from": {"x": 3, "y": 1},
    "to": {"x": 3, "y": 2},
    "player": "blue",
    "piece": "Pawn",
    "captured": null
  },
  "game_state": "[...]",
  "current_turn": "white"
}
```
## Game Logic

- Board Representation
- The chess board is represented as an 8x8 2D array:

- Index [0][0] = top-left (a8 in chess notation)
- Index [7][7] = bottom-right (h1 in chess notation)
- Blue pieces start at rows 0-1 (top of board)
- White pieces start at rows 6-7 (bottom of board)
- Coordinate System
- The game uses a 0-indexed coordinate system internally:

   0   1   2   3   4   5   6   7
0  r   n   b   q   k   b   n   r   (Blue)
1  p   p   p   p   p   p   p   p
2  .   .   .   .   .   .   .   .
3  .   .   .   .   .   .   .   .
4  .   .   .   .   .   .   .   .
5  .   .   .   .   .   .   .   .
6  P   P   P   P   P   P   P   P
7  R   N   B   Q   K   B   N   R   (White)

Turn System
White always moves first
After a player move, if successful, the AI automatically responds
Turn switches after each move
The current_turn field tracks whose turn it is
Move Validation
The MoveLogic class handles:

Validating moves are within piece's valid move set
Checking board boundaries
Ensuring pieces don't jump over other pieces (except knights)
Verifying correct piece color for current turn

# Database Models

## Users
```python
- id: Integer (Primary Key)
- username: String(250)
- email: String(500) 
- password: Text(hashed)
- created_at: DateTime

Game
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key → Users.id)
- game_status: String(500)
- winner: String(500)
- game_state: Text 

Moves

- id: Integer (Primary Key)
- game_id: Integer (Foreign Key -> Game.id)
- player: Text - "white" or "blue"
- from_square: String(500) - "x,y" format
- to_square: String(500) - "x,y" format
- game_state_after: Text (JSON serialized)

```


## Chess Pieces
#### Pawn
- Moves forward one square (two on first move)
- Captures diagonally
- Direction depends on color (white moves up, blue moves down)

#### Rook
- Moves horizontally or vertically any number of squares
- Cannot jump over pieces

### Knight
- Moves in L-shape (2 squares in one direction, 1 in perpendicular)
- Can jump over other pieces

### Bishop
- Moves diagonally any number of squares
- Cannot jump over pieces

#### Queen
- Combines rook and bishop movement
- Most powerful piece

#### King
- Moves one square in any direction (horizontal, vertical)
- Note: Diagonal moves are currently limited in the implementation

## Usage Examples
#### Complete Game Flow
python
# 1. Register a user
POST /users/add
{
  "username": "ChessPlayer",
  "email": "chess@example.com",
  "password": "password123"
}

# 2. Login (or use token from registration)
POST /users/login
{
  "email": "chess@example.com",
  "password": "password123"
}

# 3. Create a game
POST /game/create
Headers: Authorization: Bearer <token>

# 4. Make a move (e.g., move pawn from e2 to e4)
POST /moves/<game_id>
Headers: Authorization: Bearer <token>
{
  "player": "white",
  "from_x": 5,  # Column e (1-indexed)
  "from_y": 7,  # Row 2 (1-indexed, converted from display)
  "to_x": 5,
  "to_y": 5
}

# 5. AI automatically responds, game state updated
# 6. Continue making moves until game ends
Getting Valid Moves
python
# In GameManager
game_manager = GameManager(game_id, player_color="white")
game_manager.load_state(game_state_json)

# Get valid moves for a piece at position (x, y)
valid_moves = game_manager.get_valid_moves_for_piece(x, y)

## Project Structure
chess-game/
├── app/
│   ├── chess_app/
│   │   ├── pieces/
│   │   │   ├── __init__.py
│   │   │   ├── ai_logic.py      # AI opponent logic
│   │   │   ├── bishop.py        # Bishop piece
│   │   │   ├── board.py         # Board management
│   │   │   ├── gameManager.py   # Main game controller
│   │   │   ├── king.py          # King piece
│   │   │   ├── knight.py        # Knight piece
│   │   │   ├── move.py          # Move validation logic
│   │   │   ├── pawn.py          # Pawn piece
│   │   │   ├── queen.py         # Queen piece
│   │   │   └── rook.py          # Rook piece
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── game.py          # Game creation endpoints
│   │       ├── moves.py         # Move execution endpoints
│   │       └── users.py         # Authentication endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── game.py              # Game model
│   │   ├── moves.py             # Moves model
│   │   └── users.py             # Users model
│   ├── __init__.py
│   └── db.py                    # Database configuration
├── requirements.txt
└── README.md

### Key Classes
#### GameManager

Central orchestrator for game flow:

Manages turn switching
Validates moves
Coordinates player and AI moves
Maintains game state
Serializes/deserializes board state
Board
Manages the chess board:

8x8 grid representation
Piece placement and retrieval
Boundary checking
Display formatting
JSON serialization

#### AILogic
- Handles AI opponent:

- Gets all possible moves for AI color
- Randomly selects a valid move
- Currently implements random strategy (can be enhanced)

#### MoveLogic
- Move validation and execution:
- Validates moves against piece rules
- Executes validated moves
- Updates board state

#### Future Enhancements
- Implement check and checkmate detection
- Add castling and en passant
- Enhance AI 
- Add pawn promotion
- Implement move history navigation
- Add game timer/clock
- Support for multiplayer (two human players)
- Game replay functionality
- Error Handling

### The API returns appropriate HTTP status codes:

200: Success
201: Resource created
400: Bad request / Invalid move
401: Unauthorized / Invalid credentials
404: Resource not found
Error responses include descriptive messages:

json
{
  "error": "Invalid move",
  "success": false
}

License
This project is done for educational purposes under Moringa school.


