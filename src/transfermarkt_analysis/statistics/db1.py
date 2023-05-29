import csv
import mysql.connector


cnx = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1379Amir@",
    database = "test4"
)

cursor = cnx.cursor()

if cnx.is_connected():
    print("Connected to MySQL server")
else:
    print("Connection to MySQL server failed")

cnx.close()

# #  توزیع تعداد بازی هایی که بازیکنان در یک فصل انجام می دهند
# games_query = """
# SELECT num_games, COUNT(*) AS  num_players,
#     COUNT(*) / (SELECT COUNT(*) FROM players) 100 AS percentage 
# FROM players 
# WHERE season = '2021-2022' 
# GROUP BY num_games 
# ORDER BY num_games
# """

# query = "SELECT * FROM teams"

# cursor.execute(query)


# if cursor.with_rows:
#     print("Query executed successfully")
# else:
#     print("An error occurred during query execution")


# results = cursor.fetchall()
# for row in results:
#     print(row)

# cursor.close()
# cnx.close()

# cursor.execute(games_query)
# games_results = cursor.fetchall()

# # Save the query results to a CSV file
# with open('games_distribution.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Number of Games', 'Number of Players', 'Percentage'])
#     writer.writerows(games_results)

# # رابطه بین تعداد گل های زده شده و قیمت تخمینی سایت برای یک بازیکن
# goals_price_query = """
# SELECT goals_scored, estimated_price
# FROM players
# WHERE season = '2021-2022'
# """

# cursor.execute(goals_price_query)
# goals_price_results = cursor.fetchall()

# with open('goals_price_regression.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Goals Scored', 'Estimated Price'])
#     writer.writerows(goals_price_results)

# # رابطه بین تعداد گل های زده شده و قیمت تخمینی سایت برای یک مهاجم
# striker_query = """
# SELECT goal_scored, estimated_price
# FROM players
# WHERE season = '2021-2022' AND position = 'Striker' 
# """

# cursor.execute(striker_query)
# striker_results = cursor.fetchall()

# with open('striker_regression.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Goals Scored', 'Estimated Price'])
#     writer.writerows(striker_results)

# #  توزیع تخمینی قیمت بازیکنان  با تفکیک موقعیت های بازیکنان
# price_distribution_query = """
# SELECT position, estimated_price, COUNT(*) AS num_players
# FROM players
# WHERE season = '2021-2022'
# GROUP BY position, estimated_price
# ORDER BY position, estimated_pric
# """


# cursor.execute(price_distribution_query)
# price_distribution_results = cursor.fetchall()

# # Save the query results to a CSV file
# with open('price_distribution.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Position', 'Estimated Price', 'Number of Players'])
#     writer.writerows(price_distribution_results)

# # عداد گل های زده شده در لیگ های مختلف را با استفاده از داده های فصل های 2018-2019 تا 2021-2022
# goals_leagues_query = """
# SELECT season, league, SUM(goals_scored) AS total_goals
# FROM players
# WHERE season BETWEEN '2018-2019' AND '2021-2022'
# GROUP BY season, league
# ORDER BY season, league
# """

# cursor.execute(goals_leagues_query)
# goals_leagues_results = cursor.fetchall()

# with open('goals_leagues.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Season', 'League', 'Total Goals'])
#     writer.writerows(goals_leagues_results)

# # داده‌های فصل‌های 2018-2019 تا 2021-2022،  برای توزیع مبلغی  که تیم‌ها برای جذب بازیکن در هر فصل خرج کرده‌اند
# team_spending_query = """
# SELECT season, team, SUM(spent_amount) AS total_spending
# FROM teams
# WHERE season BETWEEN '2018-2019' AND '2021-2022'
# GROUP BY season, team
# ORDER BY season, team
# """

# cursor.execute(team_spending_query)
# team_spending_results = cursor.fetchall()

# with open('team_spending.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Season', 'Team', 'Total Spending'])
#     writer.writerows(team_spending_results)

# # Close the cursor and connection
# cursor.close()
# cnx.close()
