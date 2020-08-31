from flask import Flask, render_template
from flask_mysqldb import MySQL
import logging

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'prod-poker.cigqpokdjq46.us-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'jdauWEFhuwifdwF238fh2i2ASDFsd'
app.config['MYSQL_DB'] = 'poker'

mysql = MySQL(app)

@app.route('/')
def index():
    app.logger.info('logged in successfully')
    cur = mysql.connection.cursor()
    value = cur.select("SELECT * from players")
    logging.warning(value[0])
    mysql.connection.commit()
    cur.close()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)