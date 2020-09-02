from app.db import get_db, query_to_dict, db_fetch

def get_season_results(season_id: int):
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
JOIN placement_points on placement_points.player_count = games.player_count AND games_placements.placement = placement_points.placement
WHERE seasons.id = {season_id}
GROUP BY players.id
ORDER BY total_points DESC"""
    return db_fetch(sql)

def get_game_results_for_season(season_id: int):
    sql = f"""
   (
SELECT
game_number,
games.player_count as total_players,
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
JOIN placement_points on placement_points.player_count = games.player_count AND games_placements.placement = placement_points.placement
WHERE seasons.id = {season_id}
ORDER BY game_number DESC, points_earned DESC
)

UNION

(
SELECT
game_number,
games.player_count as total_players,
NULL as placement,
players.username,
0 as points_earned
FROM games JOIN seasons on games.season_id = seasons.id
JOIN games_placements on games_placements.game_id = games.id
JOIN players on players.id = games_placements.player_id
WHERE games_placements.placement IS NULL AND seasons.id = {season_id}
ORDER BY game_number DESC, points_earned DESC
)
ORDER BY game_number DESC, points_earned DESC"""
    return db_fetch(sql)

def populate_game_results(usernames_and_placements: dict, season_id: int, game_number: int):
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
        INSERT INTO games_placements
        (player_id,game_id,placement)
        VALUES 
        ({player_id},{game_id},{placement})
                   """
        get_db().execute(games_insert_sql)

# poker
# flask shell
# from app.poker_db import populate_game_results
# user_dict = {
#     'KittyKatMonk': 'NULL',
#     'JPoka19': 'NULL'
# }
# season_ids = 1
# game_numbers = 3
# populate_game_results(user_dict, season_ids, game_numbers)



# WITH placement_users as (
# SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS ranking,
# SUM(placement_points.points) as total_points,
# players.username,
# players.id as player_id,
# count(*) as number_of_games_cashed,
# GROUP_CONCAT(placement_points.placement) as placements
# FROM games JOIN seasons on games.season_id = seasons.id
# JOIN games_placements on games_placements.game_id = games.id
# JOIN players on players.id = games_placements.player_id
# JOIN placement_points on placement_points.player_count = games.player_count AND games_placements.placement = placement_points.placement
# WHERE seasons.id = 1
# GROUP BY players.id
# ORDER BY total_points DESC
# ), no_placement_users as (
# SELECT 0 as total_points,
# players.username,
# players.id as player_id,
# 0 as number_of_games_cashed,
# '' as  placements
# FROM players
# WHERE players.id NOT IN (
# SELECT placement_users.player_id
# FROM placement_users
# )
# )
#
# SELECT ranking, total_points, username, number_of_games_cashed, placements from placement_users
#




# CREATE VIEW game_results_view AS
# (
# SELECT
# game_number,
# games.player_count as total_players,
# CASE
#     WHEN placement_points.placement = 1 THEN "1st"
#     WHEN placement_points.placement = 2 THEN "2nd"
#     WHEN placement_points.placement = 3 THEN "3rd"
#     ELSE CONCAT(placement_points.placement, "th")
# END as placement,
# players.username,
# placement_points.points as points_earned
# FROM games JOIN seasons on games.season_id = seasons.id
# JOIN games_placements on games_placements.game_id = games.id
# JOIN players on players.id = games_placements.player_id
# JOIN placement_points on placement_points.player_count = games.player_count AND games_placements.placement = placement_points.placement
# WHERE seasons.id = 1
# ORDER BY game_number DESC, points_earned DESC
# )
#
# UNION
#
# (
# SELECT
# game_number,
# games.player_count as total_players,
# NULL as placement,
# players.username,
# 0 as points_earned
# FROM games JOIN seasons on games.season_id = seasons.id
# JOIN games_placements on games_placements.game_id = games.id
# JOIN players on players.id = games_placements.player_id
# WHERE games_placements.placement IS NULL AND seasons.id = 1
# ORDER BY game_number DESC, points_earned DESC
# )
# ORDER BY game_number DESC, points_earned DESC



#
#
# CREATE VIEW leaderboard_view AS SELECT total_points, username, placements, season_id from (
# SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS ranking,
# SUM(placement_points.points) as total_points,
# players.username,
# players.id as player_id,
# seasons.id as season_id,
# GROUP_CONCAT(
# CASE
#     WHEN placement_points.placement = 1 THEN "1st"
#     WHEN placement_points.placement = 2 THEN "2nd"
#     WHEN placement_points.placement = 3 THEN "3rd"
#     ELSE CONCAT(placement_points.placement, "th")
# END
# ) as placements
# FROM games JOIN seasons on games.season_id = seasons.id
# JOIN games_placements on games_placements.game_id = games.id
# JOIN players on players.id = games_placements.player_id
# JOIN placement_points on placement_points.player_count = games.player_count AND games_placements.placement = placement_points.placement
# GROUP BY players.id
# ORDER BY total_points DESC
#
# ) as leaderboard_table;




