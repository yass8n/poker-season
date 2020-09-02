from flask import Flask, render_template
import logging
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.db import db_fetch
from app.poker_db import get_season_results, get_game_results_for_season
from app.helpers import make_ordinal

@app.route('/')
def index():
    season_id = 1
    leaderboard_results = get_season_results(season_id=season_id)
    game_results = get_game_results_for_season(season_id=season_id)
    hash = {}
    current_placement = 0
    for leaderboard_result in leaderboard_results:
        if leaderboard_result['total_points'] not in hash.keys():
            current_placement = current_placement + 1
            leaderboard_result['placement'] = make_ordinal(current_placement)
            hash[leaderboard_result['total_points']] = True
        else:
            leaderboard_result['placement'] = make_ordinal(current_placement)
    all_data = {
        "leaderboard_results" : leaderboard_results,
        "game_results" : game_results,
        "season_number" : season_id
    }
    return render_template('index.html', **all_data)


if __name__ == '__main__':
    app.run(debug=True)