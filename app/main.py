from flask import Flask, render_template
import logging
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.db import db_fetch
from app.poker_db import get_season_results

@app.route('/')
def index():
    data = get_season_results(season_id=1)
    all_data = {
        "data" : data,
        "season_number" : 2
    }
    return render_template('index.html', **all_data)


if __name__ == '__main__':
    app.run(debug=True)