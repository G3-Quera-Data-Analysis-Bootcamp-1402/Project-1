import numpy as np
import pandas as pd

from transfermarkt_analysis.consts import DATA_DIR, CLEANIZED_DIR
from transfermarkt_analysis.crawl.cleanizers.base import (
    value_cleanizer,
    matches_df_concatenator,
)


__all__ = ["transfers_df_cleanizer", "store_cleanized_transfers_df"]


def transfers_df_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "transfers.csv", index_col=0)
    df = value_cleanizer(df, "fee_of_transfer")
    df = value_cleanizer(df, "market_value")
    home_df = (
        matches_df_concatenator()
        .loc[:, ["home_team", "home_team_id"]]
        .reset_index(drop=True)
    )
    away_df = (
        matches_df_concatenator()
        .loc[:, ["away_team", "away_team_id"]]
        .reset_index()
    )
    df["left_team_id"] = (
        df["left_team"]
        .mask(
            df["left_team"].isin(home_df.loc[:, "home_team"]),
            home_df.loc[:, "home_team_id"],
        )
        .mask(
            df["left_team"].isin(away_df.loc[:, "away_team"]),
            away_df.loc[:, "away_team_id"],
        )
    )
    df["joined_team_id"] = (
        df["joined_team"]
        .mask(
            df["joined_team"].isin(home_df.loc[:, "home_team"]),
            home_df.loc[:, "home_team_id"],
        )
        .mask(
            df["joined_team"].isin(away_df.loc[:, "away_team"]),
            away_df.loc[:, "away_team_id"],
        )
    )

    return df.loc[
        (df["left_team_id"].str.isnumeric()) & (df["joined_team_id"].str.isnumeric()),
        [
            "player_id",
            "season_id",
            "left_team_id",
            "joined_team_id",
            "market_value",
            "fee_of_transfer",
        ],
    ]


def store_cleanized_transfers_df() -> None:
    df: pd.DataFrame = transfers_df_cleanizer()
    df = df.dropna().drop_duplicates()
    df.to_csv(CLEANIZED_DIR / "contracts.csv", index=False)