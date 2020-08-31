from flask_sqlalchemy import SQLAlchemy
from app.main import app

db = SQLAlchemy(app)

def get_db():
    return db.engine
