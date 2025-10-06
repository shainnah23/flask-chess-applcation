from flask import Flask
from .config import Config
from .db import db, migrate
from .chess_app import *
from app.models import *
from app.routes import *
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt=Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    
    # Initialize migrate with both app and db
    migrate.init_app(app, db)

    migrate.init_app(app,db)
    bcrypt.init_app(app)
    jwt.init_app(app)
   # Register blueprints
    app.register_blueprint(game_bp, url_prefix="/game")
    app.register_blueprint(moves_bp, url_prefix="/move") 
   
    
    return app