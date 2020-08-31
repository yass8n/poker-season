from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:jdauWEFhuwifdwF238fh2i2ASDFsd@prod-poker.cigqpokdjq46.us-west-1.rds.amazonaws.com/poker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def get_db():
    return db.engine