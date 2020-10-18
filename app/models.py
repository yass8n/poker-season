from app.db import get_db, query_to_dict, db_fetch
from app.helpers import make_ordinal
from app.db import db
from app.helpers import get_datetime_from_string
import datetime

class BaseModel(db.Model):
    __abstract__ = True
    def save(self):
        db.session.add(self)
        db.session.commit()

class Player(BaseModel):
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
        nullable=False,
        default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    @classmethod
    def create_player_with_username(cls, username):
        player = Player()
        player.username = username
        player.save()
        return player


class Club(BaseModel):
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
        nullable=True,
        default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.datetime.utcnow
    )

    def get_all_seasons(self):
        sql = f"""
    SELECT * FROM seasons WHERE club_id = {self.id}
    """
        return db_fetch(sql)

class Season(BaseModel):
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
        nullable=True,
        default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.datetime.utcnow
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
    END 
    ORDER BY games.start_date ASC
    SEPARATOR ', '
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
    games.season_id as season_id,
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
    games.season_id as season_id,
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

class Game(BaseModel):
    __tablename__ = 'games'
    id = db.Column(
        db.Integer,
        primary_key=True
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
    start_date = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.datetime.utcnow
    )

    def get_total_player_count(self):
        sql = f"""
SELECT COUNT(*) as total 
FROM games_placements 
INNER JOIN games ON games.id = games_placements.game_id 
WHERE games.id = {self.id} 
GROUP BY games.id"""
        game_result = db_fetch(sql)
        return game_result[0]['total']

    def populate_game_results(usernames_and_placements: dict,
                              season_id: int,
                              game_number: int,
                              start_date: str):
        game = Game.query.filter_by(game_number=game_number, season_id=season_id).first()
        if game is None:
            # create game model if not exists
            game = Game(game_number=game_number, season_id=season_id, start_date=get_datetime_from_string(start_date))
            game.save()

        # delete all existing games placements
        db.session.query(GamePlacement).filter_by(game_id=game.id).delete()
        db.session.commit()

        for username in usernames_and_placements:
            player = Player.query.filter_by(username=username).first()
            if player is None:
                # create player if not exists
                player = Player(username=username)
                player.save()
            placement = usernames_and_placements[username]

            # create game_placement
            game_placement = GamePlacement(player_id=player.id, game_id=game.id, placement=placement)
            game_placement.save()

        # update player count
        game.player_count = game.get_total_player_count()
        game.save()

class GamePlacement(BaseModel):
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
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.datetime.utcnow
    )

class PlacementPoint(BaseModel):
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

