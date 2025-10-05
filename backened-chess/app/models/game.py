from app.db import db

class Game(db.Model):
    __tablename__="game"
    id = db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"),nullable=True)
    game_status=db.Column(db.String(500),nullable=False)
    winner= db.Column (db.String(500),nullable=False)
    game_state = db.Column (db.Text,nullable=False)
