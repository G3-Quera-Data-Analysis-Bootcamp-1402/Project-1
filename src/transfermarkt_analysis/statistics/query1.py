import pandas as pd
from transfermarkt_analysis.consts import CLEANIZED_DIR


def games_played():
    df = pd.read_csv(CLEANIZED_DIR / "player_appearances.csv").reset_index(drop= True)
    matchs_df = pd.read_csv(CLEANIZED_DIR / "matches.csv").reset_index(drop= True)
    concat_df = pd.concat([df,matchs_df], axis=1)
    result = concat_df.loc[concat_df['season_id'] == 2021 ].groupby('player_id').count().reset_index().loc[:,['player_id','season_id']]
    return result['season_id']



# Calculate the distribution of the number of games played by players
match_count = games_played()
games_played_distribution = match_count.value_counts(normalize=True)


# Calculate the percentage of games that players participate in
total_games = match_count.sum()
player_games_percentage = (match_count / total_games) * 100

print(games_played_distribution)
print(player_games_percentage)
