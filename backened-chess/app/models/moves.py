from app.db import db


class Moves(db.Model):
    __tablename__="moves"
    id = db.Column (db.Integer,primary_key=True)
    game_id=db.Column (db.Integer,db.ForeignKey("game.id"),nullable=True)
    player=db.Column (db.Text,nullable=False)
    from_square= db.Column (db.String(500),nullable=False)
    to_square= db.Column(db.String(500),nullable=False)
    game_state_after=db.Column (db.Text,nullable=False)
    

    
