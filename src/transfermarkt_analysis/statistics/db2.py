import mysql.connector

cnx = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1379Amir#",
    database = "transfermarkt"
)


karshenas = """
SELECT * FROM  Contracts JOIN market_values   
Contracts.player_id = market_values.player_id AND Contracts.season_id = market_values.season_id
"""