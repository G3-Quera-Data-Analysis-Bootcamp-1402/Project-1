import pandas as pd
from transfermarkt_analysis.consts import CLEANIZED_DIR


def games_played():
    df = pd.read_csv(CLEANIZED_DIR / "player_appearances.csv").reset_index(drop= True)
    matchs_df = pd.read_csv(CLEANIZED_DIR / "matches.csv").reset_index(drop= True)
    concat_df = pd.concat([df,matchs_df], axis=1)
    result = concat_df.loc[concat_df['season_id'] == 2021 ].groupby('player_id').count().reset_index().loc[:,['player_id','season_id']]
    match_count = result['season_id']
    games_played_distribution = match_count.value_counts(normalize=True)
    total_games = match_count.sum()
    player_games_percentage = (match_count / total_games) * 100
    print(games_played_distribution)
    print(player_games_percentage)









def goal_market_value():
    goal_df = pd.read_csv(CLEANIZED_DIR / "goals.csv")
    mv_df= pd.read_csv(CLEANIZED_DIR / "market_values.csv")
    matchs_df = pd.read_csv(CLEANIZED_DIR / "matches.csv").reset_index(drop= True)
    concat_df = pd.concat([goal_df,mv_df,matchs_df], axis=1)


    x = concat_df.loc[concat_df['season_id'] == 2021].groupby('scorrer_id').count().loc[:,'match_id']
    print(x)

goal_market_value
