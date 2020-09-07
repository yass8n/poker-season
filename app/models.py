from app.db import get_db, query_to_dict, db_fetch
from app.helpers import make_ordinal
from app.db import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(255),
        index=False,
        unique=True,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def get_all_seasons(self):
        sql = f"""
    SELECT * FROM seasons WHERE club_id = {self.id}
    """
        return db_fetch(sql)

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    champion_id = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=True
    )
    club_id = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=True
    )
    season_number = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True
    )
    link = db.Column(
        db.String(255),
        index=False,
        unique=False,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def get_season_results(self):
        sql = f"""
    SELECT SUM(placement_points.points) as total_points,
    players.username,
    players.id as player_id,
    seasons.id as season_id,
    GROUP_CONCAT(
    CASE
        WHEN placement_points.placement = 1 THEN '1st'
        WHEN placement_points.placement = 2 THEN '2nd'
        WHEN placement_points.placement = 3 THEN '3rd'
        ELSE CONCAT(placement_points.placement, 'th')
    END SEPARATOR ', '
    ) as placements
    FROM games JOIN seasons on games.season_id = seasons.id
    JOIN games_placements on games_placements.game_id = games.id
    JOIN players on players.id = games_placements.player_id
    JOIN placement_points on placement_points.player_count = games.player_count 
    AND placement_points.season_id = games.season_id
    AND games_placements.placement = placement_points.placement
    WHERE seasons.id = {self.id}
    GROUP BY players.id
    ORDER BY total_points DESC"""

        season_leaderboard_results = db_fetch(sql)
        hash = {}
        current_placement = 0
        for leaderboard_result in season_leaderboard_results:
            if leaderboard_result['total_points'] not in hash.keys():
                current_placement = current_placement + 1
                leaderboard_result['placement'] = make_ordinal(current_placement)
                hash[leaderboard_result['total_points']] = True
            else:
                leaderboard_result['placement'] = make_ordinal(current_placement)

        return season_leaderboard_results

    def get_game_results_for_season(self):
        sql = f"""
       (
    SELECT
    game_number,
    games.player_count as total_players,
    games.id as id,
    CASE
        WHEN placement_points.placement = 1 THEN "1st"
        WHEN placement_points.placement = 2 THEN "2nd"
        WHEN placement_points.placement = 3 THEN "3rd"
        ELSE CONCAT(placement_points.placement, "th")
    END as placement,
    players.username,
    placement_points.points as points_earned
    FROM games JOIN seasons on games.season_id = seasons.id
    JOIN games_placements on games_placements.game_id = games.id
    JOIN players on players.id = games_placements.player_id
    JOIN placement_points on placement_points.player_count = games.player_count 
    AND placement_points.season_id = games.season_id
    AND games_placements.placement = placement_points.placement
    WHERE seasons.id = {self.id}
    ORDER BY game_number DESC, points_earned DESC
    )

    UNION

    (
    SELECT
    game_number,
    games.player_count as total_players,
    games.id as id,
    NULL as placement,
    players.username,
    0 as points_earned
    FROM games JOIN seasons on games.season_id = seasons.id
    JOIN games_placements on games_placements.game_id = games.id
    JOIN players on players.id = games_placements.player_id
    WHERE games_placements.placement IS NULL AND seasons.id = {self.id}
    ORDER BY game_number DESC, points_earned DESC
    )
    ORDER BY game_number DESC, points_earned DESC"""
        season_game_results = db_fetch(sql)
        hash = {}
        for game_result in season_game_results:
            if game_result['game_number'] not in hash.keys():
                hash[game_result['game_number']] = []
            hash[game_result['game_number']].append(game_result)

        return hash

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    season_id = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
    player_count = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
    game_number = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def populate_game_results(usernames_and_placements: dict, season_id: int, game_number: int, player_count: int,
                              start_date: str):
        find_game_sql = f"""
        SELECT *
        FROM games
        WHERE games.game_number = {game_number}
        AND games.season_id = {season_id}"""
        game_id = db_fetch(find_game_sql)
        if (len(game_id) == 0):
            games_insert_sql = f"""
                INSERT IGNORE INTO games
                (game_number,season_id, player_count, start_date)
                VALUES 
                ({game_number},{season_id},{player_count},{start_date})
                 """
            get_db().execute(games_insert_sql)

        games_sql = f"""
    SELECT games.id 
    FROM games
    WHERE games.game_number = {game_number}
    AND games.season_id = {season_id}
               """
        game_id = db_fetch(games_sql)[0]['id']
        for username in usernames_and_placements:
            placement = usernames_and_placements[username]
            player_sql = f"""
            SELECT players.id 
            FROM players
            WHERE players.username = '{username}'
                       """
            player_id = db_fetch(player_sql)[0]['id']
            games_insert_sql = f"""
            INSERT IGNORE INTO games_placements
            (player_id,game_id,placement)
            VALUES 
            ({player_id},{game_id},{placement})
                       """
            get_db().execute(games_insert_sql)

class GamePlacement(db.Model):
    __tablename__ = 'games_placements'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    player_id = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
    game_id = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
    placement = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

class PlacementPoint(db.Model):
    __tablename__ = 'placement_points'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    placement = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    points = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    player_count = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    season_id = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
