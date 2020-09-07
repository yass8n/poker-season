from flask import Flask, render_template
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.models import Season, Club

@app.route('/club/<club_id>')
@app.route('/')
def index(club_id: int = 1):
    club = Club.query.get(club_id)
    club_seasons = club.get_all_seasons()
    all_data = {
        "club_seasons" : club_seasons,
        "club" : club
    }
    return render_template('index.html', **all_data)

@app.route('/season/<season_id>')
def show(season_id: int):
    season = Season.query.get(season_id)
    club = Club.query.get(season.club_id)
    season_leaderboard_results = season.get_season_results()
    game_results = season.get_game_results_for_season()
    club_seasons = club.get_all_seasons()
    all_data = {
        "club_seasons" : club_seasons,
        "season_leaderboard_results" : season_leaderboard_results,
        "game_results" : game_results,
        "season" : season,
        "club": club
    }
    return render_template('season_leaderboard.html', **all_data)

@app.route('/season/<season_id>/streaks')
def show_season_streaks(season_id: int):
    season = Season.query.get(season_id)
    club = Club.query.get(season.club_id)
    club_seasons = club.get_all_seasons()
    all_data = {
        "club_seasons": club_seasons,
        "season": season,
        "club": club
    }
    return render_template('season_player_stats.html', **all_data)


if __name__ == '__main__':
    app.run(debug=True)