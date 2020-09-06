from flask import Flask, render_template
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.models import Season, Club

@app.route('/<club_id>')
@app.route('/')
def index(club_id: int = 1):
    club = Club.query.get(club_id)
    club_seasons = Club.get_all_seasons(club_id=club.id)
    all_data = {
        "club_seasons" : club_seasons,
        "club" : club
    }
    return render_template('index.html', **all_data)

@app.route('/club/<club_id>/season/<season_id>')
def show(club_id: int, season_id: int):
    season_leaderboard_results = Season.get_season_results(season_id=season_id)
    game_results = Season.get_game_results_for_season(season_id=season_id)
    club = Club.query.get(club_id)
    club_seasons = Club.get_all_seasons(club_id=club_id)
    all_data = {
        "club_seasons" : club_seasons,
        "season_leaderboard_results" : season_leaderboard_results,
        "game_results" : game_results,
        "season_number" : season_id,
        "club": club
    }
    return render_template('show.html', **all_data)


if __name__ == '__main__':
    app.run(debug=True)