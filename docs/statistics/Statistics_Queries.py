#KPI Definition and Normalization




#Importing Liberaries
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

#Player's Request
query_player = text("""select *
from (select team_id, position_code_abstract, avg(KPI) as KPI_per_position_per_team
      from player_appearances
      group by team_id, position_code_abstract) as t1
where position_code_abstract = 'B'
  AND KPI_per_position_per_team > (SELECT KPI_per_position_per_team
                                   FROM t1
                                   WHERE team_id = t1.team_id
                                     AND position_code_abstract = 'F');""")

conn = pymysql.connect(host='localhost', user='root', password='Mba4957@ms3#13', db='transfermarkt')

# Retrieve the market_value column from table1
with conn.cursor() as cursor:
    cursor.execute(query_player)
    table__player_data = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the query results to dataframes
df = pd.DataFrame(table__player_data, columns=['team_id', 'position_code_abstract', 'KPI_per_position_per_team'])

# Export the dataframes to CSV files: this line can be ingnored and it's just for a better documntation.
df.to_csv('phase3_table_players.csv', index=False)


#Coach 1

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='Mba4957@ms3#13', db='transfermarkt')

query = text("""
select *
select Player_ID, Player_Name, KPI_per_player, Market_value
from (select player_id, KPI_per_player
      from (select player_id, avg(KPI) as KPI_per_player
            group by player_id) t1
      order by KPI_per_player desc
      limit round
      (0.3*(count(*) from t1))) t2
         join
     (select player_id, Market_value
      from (select player_id, Market_value
            from (select player_id, Market_value
                  from Market_value MV
                           join season s
                  where season.season == "21/22") t3
            order by Market_value asc
            limit round
            (0.4*(count(*) from t3)))) on t2.player_id = t3.player_id) join (SELECT player_id, MAX(position_code_count.position_code) AS most_frequent_position_code
FROM (
  SELECT player_id, position_code, COUNT(*) AS count
  FROM player_appearances
  GROUP BY player_id, position_code
) AS position_code_count
GROUP BY player_id;
) join Player;
""" )

# Retrieve the market_value column from table1
with conn.cursor() as cursor:
    cursor.execute(query)
    table_data = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the query results to dataframes
df = pd.DataFrame(table_data, columns=['Player_ID', 'Player_Name', 'KPI_per_player', 'Market_value'])

# Export the dataframes to CSV files: this line can be ingnored and it's just for a better documntation.
df.to_csv('table_part1.csv', index=False)

######################################################################
#Coach 2

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='Mba4957@ms3#13', db='transfermarkt')

# query1 = text("""
# select Player_ID, Player_Name, KPI_per_player, Market_value
# from (select player_id, KPI_per_player
#       from (select player_id, avg(KPI) as KPI_per_player
#             from player_appearances
#             group by player_id) t1
#       order by KPI_per_player desc
#       limit round
#       (0.3*(count(*) from t1))) t2
#          join
#      (select player_id, Market_value
#       from (select player_id, Market_value
#             from (select player_id, Market_value
#                   from Market_value MV
#                            join season s
#                   where season.season == "21/22") t3
#             order by Market_value asc
#             limit round
#             (0.4*(count(*) from t3)))) on t2.player_id = t3.player_id) join Player;
# """ )

# # Retrieve the market_value column from table1
# with conn.cursor() as cursor:
#     cursor.execute(query1)
#     table1_data = cursor.fetchall()

# Retrieve the market_value column from table2
with conn.cursor() as cursor:
    cursor.execute('select Market_value from Market_value inner join season.season where season.season = "21/22";')
    table2_data = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the query results to dataframes
# df1 = pd.DataFrame(table1_data, columns=['market_value'])
df2 = pd.DataFrame(table2_data, columns=['market_value'])

# Export the dataframes to CSV files: this line can be ingnored and it's just for a better documntation.
# df1.to_csv('table1.csv', index=False)
df2.to_csv('table2.csv', index=False)

# Load the CSV files into Pandas dataframes
df1 = pd.read_csv('table_part1.csv')
df2 = pd.read_csv('table2.csv')

# Create the histograms
plt.hist(df1['market_value'], bins=20, alpha=0.5)
plt.hist(df2['market_value'], bins=20, alpha=0.5)

# Add labels and legend
plt.xlabel('Market Value')
plt.ylabel('Frequency')
plt.title('Distribution of Market Value: A Comaprison View')
plt.legend(['Good Players with Low Price', 'All Players'])

# Show the plot
plt.show()

####################################################
#Coach 3

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='Mba4957@ms3#13', db='transfermarkt')

# query1 = text("""
# select KPI_per_player
# from (select player_id, KPI_per_player
#       from (select player_id, avg(KPI) as KPI_per_player
#             from player_appearances
#             group by player_id) t1
#       order by KPI_per_player desc
#       limit round
#       (0.3*(count(*) from t1))) t2
#          join
#      (select player_id, Market_value
#       from (select player_id, Market_value
#             from (select player_id, Market_value
#                   from Market_value MV
#                            join season s
#                   where season.season == "21/22") t3
#             order by Market_value asc
#             limit round
#             (0.4*(count(*) from t3)))) on t2.player_id = t3.player_id;
# """ )

# # Retrieve the market_value column from table1
# with conn.cursor() as cursor:
#     cursor.execute(query1)
#     table1_data = cursor.fetchall()

# Retrieve the market_value column from table2
with conn.cursor() as cursor:
    cursor.execute("""select KPI_per_player from player_appearances
    inner join (select match_id from match inner join season.season where season.season = "21/22") t1
    on player_appearances.match_id = t1.match_id;""")
    table2_data = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the query results to dataframes
# df1 = pd.DataFrame(table1_data, columns=['KPI_per_player'])
df2 = pd.DataFrame(table2_data, columns=['KPI_per_player'])

# Export the dataframes to CSV files: this line can be ingnored and it's just for a better documntation.
# df1.to_csv('table1.csv', index=False)
df2.to_csv('table2.csv', index=False)

# Load the CSV files into Pandas dataframes
df1 = pd.read_csv('table_part1.csv')
df2 = pd.read_csv('table2.csv')

# Create the histograms
plt.hist(df1['KPI_per_player'], bins=20, alpha=0.5)
plt.hist(df2['KPI_per_player'], bins=20, alpha=0.5)

# Add labels and legend
plt.xlabel('KPI Per Player')
plt.ylabel('Frequency')
plt.title('Distribution of KPIs: A Comparison View')
plt.legend(['Good Players with Low Price', 'All Players'])

# Show the plot
plt.show()

####################################################
#Coach 4

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='Mba4957@ms3#13', db='transfermarkt')

query1 = text("""
select player_id, most_frequent_position_code
from (select player_id, KPI_per_player
      from (select player_id, avg(KPI) as KPI_per_player
            group by player_id) t1
      order by KPI_per_player desc
      limit round
      (0.3*(count(*) from t1))) t2
         join
     (select player_id, Market_value
      from (select player_id, Market_value
            from (select player_id, Market_value
                  from Market_value MV
                           join season s
                  where season.season = "21/22") t3
            order by Market_value asc
            limit round
            (0.4*(count(*) from t3)))) on t2.player_id = t3.player_id) join
            (SELECT player_id, MAX(position_code_count.position_code) AS most_frequent_position_code
FROM (
  SELECT player_id, position_code, COUNT(*) AS count
  FROM player_appearances
  GROUP BY player_id, position_code
) AS position_code_count
GROUP BY player_id;
) join Player;
""" )

query2 = text("""
SELECT player_id, MAX(position_code_count.position_code) AS most_frequent_position_code
FROM (
  SELECT player_id, position_code, COUNT(*) AS count
  FROM player_appearances
  GROUP BY player_id, position_code
) AS position_code_count
GROUP BY player_id;
""")
# Retrieve the market_value column from table1
with conn.cursor() as cursor:
    cursor.execute(query1)
    table1_data = cursor.fetchall()

# Retrieve the market_value column from table2
with conn.cursor() as cursor:
    cursor.execute(query2)
    table2_data = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the query results to dataframes
df1 = pd.DataFrame(table1_data, columns=['most_frequent_position_code'])
df2 = pd.DataFrame(table2_data, columns=['most_frequent_position_code'])

# Export the dataframes to CSV files: this line can be ingnored and it's just for a better documntation.
df1.to_csv('table1.csv', index=False)
df2.to_csv('table2.csv', index=False)

# Load the CSV files into Pandas dataframes
df1 = pd.read_csv('table1.csv')
df2 = pd.read_csv('table2.csv')

# Create the histograms
plt.hist(df1['most_frequent_position_code'], bins=20, alpha=0.5)
plt.hist(df2['most_frequent_position_code'], bins=20, alpha=0.5)

# Add labels and legend
plt.xlabel('Most Frequent Position Code')
plt.ylabel('Frequency')
plt.title('Distribution of Position: A Comparison View')
plt.legend(['Good Players with Low Price', 'All Players'])

# Show the plot
plt.show()

###############################################
#chams2122 = [Paris SG, Manchester City, real Madrid, AC Milan, Bayern Munich]
conn = pymysql.connect(host='localhost', user='root', password='Mba4957@ms3#13', db='transfermarkt')
query = text(""""
select team_name, Player_Name, KPI_per_player from (select team_id, team_name from teams where team_name in [Paris SG, Manchester City, real Madrid, AC Milan, Bayern Munich])t0 join
(select Player_ID, Player_Name, KPI_per_player
from (select player_id, KPI_per_player
      from (select player_id, avg(KPI) as KPI_per_player
            from player_appearances
            group by player_id
            having KPI_per_player<0.3) t1)) t2
     ))) on t2.player_id = t3.player_id) join Player) t4;
""")

# Retrieve the market_value column from table1
with conn.cursor() as cursor:
    cursor.execute(query)
    table_data = cursor.fetchall()

conn.close()

# Convert the query results to dataframes
df = pd.DataFrame(table_data, columns=['team_name', 'Player_Name', 'KPI_per_player'])

# Export the dataframes to CSV files: this line can be ingnored and it's just for a better documntation.
df.to_csv('table.csv', index=False)

#test1
query_test1_1 = text("""select player_id, date_of_birth, season_id, league_id
        from players
         join player_appearances pa on players.player_id = pa.player_id
         join matches m on pa.match_id = m.match_id
         join League_start_time lst on match.league_id = lst.league_id;""")

# Retrieve the market_value column from table1
with conn.cursor() as cursor:
    cursor.execute(query_test1_1)
    table_data = cursor.fetchall()

conn.close()

# Convert the query results to dataframes
df1 = pd.DataFrame(table_data, columns=['player_id', 'date_of_birth', 'season_id', 'league_id'])
for season_iterator in range(1, 8):
  for league_iterator in range(1, 7):
      end_life = df_league_start[season_iterator, league_iterator]
      age = end_life - df1['date_of_birth']