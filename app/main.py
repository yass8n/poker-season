from flask import Flask, render_template
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.models import Season, Club

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/clubs/<club_id>/seasons/<season_id>')
def show(club_id: int, season_id: int):
    season_leaderboard_results = Season.get_season_results(season_id=season_id)
    game_results = Season.get_game_results_for_season(season_id=season_id)
    club_seasons = Club.get_all_seasons(club_id=club_id)
    all_data = {
        "club_seasons" : club_seasons,
        "season_leaderboard_results" : season_leaderboard_results,
        "game_results" : game_results,
        "season_number" : season_id
    }
    return render_template('index.html', **all_data)


if __name__ == '__main__':
    app.run(debug=True)