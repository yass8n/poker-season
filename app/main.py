from flask import Flask, render_template
import logging
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.db import get_db

@app.route('/')
def index():
    app.logger.info('logged in successfully')
    result = get_db().execute("SELECT * from players")
    names = [row.username for row in result]
    logging.warning(names)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)