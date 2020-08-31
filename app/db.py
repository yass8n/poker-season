from flask_sqlalchemy import SQLAlchemy
from app.main import app

db = SQLAlchemy(app)

def get_db():
    return db.engine

def db_fetch(sql):
    return query_to_dict(get_db().execute(sql).fetchall())

def query_to_dict(ret):
    if ret is not None:
        return [{key: value for key, value in row.items()} for row in ret if row is not None]
    else:
        return [{}]