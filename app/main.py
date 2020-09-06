from flask import Flask, render_template
import logging
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.db import db_fetch
from app.poker_db import get_season_results, get_game_results_for_season

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/seasons/<season_id>')
def show(season_id: int):
    season_leaderboard_results = get_season_results(season_id=season_id)
    game_results = get_game_results_for_season(season_id=season_id)

    all_data = {
        "season_leaderboard_results" : season_leaderboard_results,
        "game_results" : game_results,
        "season_number" : season_id
    }
    return render_template('index.html', **all_data)


if __name__ == '__main__':
    app.run(debug=True)