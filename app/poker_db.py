from app.db import get_db


def get_season_results(season_id: int):
    sql = f"""
         SELECT SUM(placement_points.points), players.username, count(*) as number_of_games_played, GROUP_CONCAT(placement_points.placement) as placements
FROM games JOIN seasons on games.season_id = seasons.id
JOIN games_placements on games_placements.game_id = games.id
JOIN players on players.id = games_placements.player_id
JOIN placement_points on placement_points.player_count = games.player_count AND games_placements.placement = placement_points.placement
WHERE seasons.id = {season_id}
GROUP BY players.id"""
    return get_db().execute(sql)

# WITH placement_users as (
# SELECT SUM(placement_points.points) as total_points,
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
# SELECT total_points, username, number_of_games_cashed, placements from placement_users
#
# UNION
#
# SELECT total_points, username, number_of_games_cashed, placements from no_placement_users
#
#
