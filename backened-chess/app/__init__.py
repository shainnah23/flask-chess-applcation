from flask import Flask
from .config import Config
from .db import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    
    # Initialize migrate with both app and db
    migrate.init_app(app, db)
    
   
    
    return app