import ast
import os
import re
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from transfermarkt_analysis.crawl.consts import DATA_DIR

CLEANIZED_DIR = DATA_DIR / "cleanized"

# transfers cleanizer


def fee_col_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
    """
    cleanize fee_of_transfer column
    1- replace -, ? with np.nan
    2- replace leihe with loan -> 1
    3- replace leih-ende with end-loan -> -1.0
    4- replace ablösefrei with free -> 0.0
    5- replace <num>,<num> Mio with <num><num>0000.0
    6- replace <num>,<num> Tsd with <num><num>000.0
    7- replace <num>,<num> € with <num><num>
    """
    df["fee_of_transfer"] = (
        df["fee_of_transfer"]
        .mask(df["fee_of_transfer"].str.lower() == "leihe", "1")
        .mask(df["fee_of_transfer"].str.contains("Leih-Ende"), "-1")
        .mask(df["fee_of_transfer"].str.contains("ablösefrei"), "0")
        .apply(
            lambda x: ",".join(re.findall(r"\d+", x)).replace(",", "") + "0000"
            if "Mio" in x
            else x
        )
        .apply(lambda x: "".join(re.findall(r"\d+", x)) + "000" if "Tsd" in x else x)
        .apply(lambda x: "".join(re.findall(r"\d+", x)) if "€" in x else x)
        .mask(df["fee_of_transfer"].isin(["-", "?", "draft"]), np.nan)
        .astype("float")
    )
    return df


def transfers_df_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "transfers.csv", index_col=0)
    df = fee_col_cleanizer(df)
    return df


def store_cleanized_transfers_df() -> None:
    df: pd.DataFrame = transfers_df_cleanizer()
    df = df.dropna().drop_duplicates()
    df.to_csv(CLEANIZED_DIR / "transfers.csv", index=False)


# matches cleanizers


def matches_df_concatenator() -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame()
    MATCHES_DATA_DIR = DATA_DIR / "matches"
    for pt_csv in os.listdir(MATCHES_DATA_DIR):
        pt_df: pd.DataFrame = pd.read_csv(MATCHES_DATA_DIR / pt_csv)
        df = pd.concat([df, pt_df])
    df = df.drop_duplicates().dropna()
    return df


def list_df_cleanizer(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    convert List[Dict] representation to List[Dict]
    used for home_goals, away_goals, home_substutations,
    away_substutations, home_cards, away_cards
    """
    data = []

    for string_list in df.loc[:, col]:
        try:
            for obj in ast.literal_eval(string_list):
                data.append(obj)
        except SyntaxError:
            pass

    return pd.DataFrame(data)


def statistics_df_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Like list_df_cleanizer but the difference is it converts
    Dict representation to Dict
    """
    data: List[Dict[str, Any]] = [
        ast.literal_eval(statistics) for statistics in df["statistics"]
    ]
    return pd.DataFrame(data)


def matches_df_cleanizer() -> Dict[str, pd.DataFrame]:
    concated_matches_df: pd.DataFrame = matches_df_concatenator()
    list_dfs: Dict[str, pd.DataFrame] = {
        "home_goals": list_df_cleanizer(concated_matches_df, "home_goals"),
        "away_goals": list_df_cleanizer(concated_matches_df, "home_goals"),
        "home_substitutions": list_df_cleanizer(
            concated_matches_df, "home_substitutions"
        ),
        "away_substitutions": list_df_cleanizer(
            concated_matches_df, "home_substitutions"
        ),
        "home_cards": list_df_cleanizer(concated_matches_df, "home_cards"),
        "away_cards": list_df_cleanizer(concated_matches_df, "home_cards"),
    }
    removed_columns: List[str] = [
        "url_id",
        "home_goals",
        "away_goals",
        "home_substitutions",
        "away_substitutions",
        "home_cards",
        "away_cards",
    ]
    matches_df: pd.DataFrame = concated_matches_df.loc[
        :, ~concated_matches_df.columns.isin(removed_columns)
    ]
    statistics_df: pd.DataFrame = statistics_df_cleanizer(matches_df).reset_index(drop=True)
    matches_df = matches_df.reset_index(drop=True).loc[
        :, ~matches_df.columns.isin(["statistics"])
    ]
    return {
        "matches_df": pd.concat([matches_df, statistics_df], axis=1),
        "goals_df": pd.concat([list_dfs["home_goals"], list_dfs["away_goals"]]),
        "substitutions_df": pd.concat(
            [list_dfs["home_substitutions"], list_dfs["away_substitutions"]]
        ),
        "cards_df": pd.concat([list_dfs["home_cards"], list_dfs["away_cards"]]),
    }


def store_cleanized_matches_dfs() -> None:
    dfs: Dict[str, pd.DataFrame] = matches_df_cleanizer()
    dfs["matches_df"].to_csv(CLEANIZED_DIR / "matches.csv", index=False)
    dfs["goals_df"].to_csv(CLEANIZED_DIR / "goals.csv", index=False)
    dfs["substitutions_df"].to_csv(CLEANIZED_DIR / "substitutions.csv", index=False)
    dfs["cards_df"].to_csv(CLEANIZED_DIR / "cards.csv", index=False)


store_cleanized_matches_dfs()
