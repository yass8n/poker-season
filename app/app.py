from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)


#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:jdauWEFhuwifdwF238fh2i2ASDFsd@prod-poker.cigqpokdjq46.us-west-1.rds.amazonaws.com/poker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'prod-poker.cigqpokdjq46.us-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'jdauWEFhuwifdwF238fh2i2ASDFsd'
app.config['MYSQL_DB'] = 'poker'

mysql = MySQL(app)

@app.route('/')
def index():
    app.logger.info('logged in successfully')
    result = db.engine.execute("SELECT * from players")
    names = [row.username for row in result]
    logging.warning(names)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)