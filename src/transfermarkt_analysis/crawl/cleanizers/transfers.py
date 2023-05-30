from typing import Dict

import pandas as pd

from transfermarkt_analysis.consts import DATA_DIR, CLEANIZED_DIR
from transfermarkt_analysis.crawl.cleanizers.base import (
    value_cleanizer,
)


__all__ = ["transfers_df_cleanizer", "store_cleanized_transfers_df"]


def transfers_df_cleanizer() -> Dict[str, pd.DataFrame]:
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "transfers.csv", index_col=0)
    df = value_cleanizer(df, "fee_of_transfer")
    df = value_cleanizer(df, "market_value")

    df = df.drop_duplicates().dropna()

    contracts_df: pd.DataFrame = df.loc[:, ["player_id", "season_id", "left_team_id", "joined_team_id", "fee_of_transfer"]]
    marktet_value_df: pd.DataFrame = df.loc[:, ["player_id", "season_id", "market_value"]]

    return {
        "contracts": contracts_df, 
        "market_value": marktet_value_df
    }


def store_cleanized_transfers_df() -> None:
    dfs: pd.DataFrame = transfers_df_cleanizer()
    dfs["contracts"].to_csv(CLEANIZED_DIR / "contracts.csv", index=False)
    dfs["market_value"].to_csv(CLEANIZED_DIR / "market_values.csv", index=False)
