import ast
from typing import Any, Dict, List

import pandas as pd

from transfermarkt_analysis.consts import DATA_DIR, CLEANIZED_DIR
from transfermarkt_analysis.crawl.cleanizers.base import matches_df_concatenator


def list_df_cleanizer(df: pd.DataFrame, col: str, team_id_col: str = None) -> pd.DataFrame:
    """
    convert List[Dict] representation to List[Dict]
    used for home_goals, away_goals, home_substutations,
    away_substutations, home_cards, away_cards
    """
    data = []

    def append_data(string_list, team_id: Any = None):
        try:
            for obj in ast.literal_eval(string_list):
                if team_id is not None:
                    data.append({"team_id": team_id, **obj})
                else:
                    data.append(obj)
        except Exception:
            pass

    if team_id_col is not None:
        for team_id, string_list in zip(df.loc[:, team_id_col], df.loc[:, col]):
            append_data(string_list, team_id)
    else:
        for string_list in df.loc[:, col]:
            append_data(string_list)


    return pd.DataFrame(data)


def list_df_concatenator(df: pd.DataFrame, target_cols: List[str], result_cols: List[str]) -> pd.DataFrame:
    """
        used to concatenate home* away* dataframes
        target_cols: [home_goals, away_goals], ...
        resutls_cols: [match_id, team_id, ...]
    """
    home: pd.DataFrame = list_df_cleanizer(df, target_cols[0], "home_team_id")
    away: pd.DataFrame = list_df_cleanizer(df, target_cols[1], "away_team_id")
    all: pd.DataFrame = pd.concat([home, away])
    return all.loc[:, result_cols]


def statistics_df_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Like list_df_cleanizer but the difference is it converts
    Dict representation to Dict
    """
    data: List[Dict[str, Any]] = [
        ast.literal_eval(statistics)
        for statistics in df.loc[df["statistics"].notna(), "statistics"]
    ]
    return pd.DataFrame(data)


def result_df_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
    def home_score(result: str) -> int:
        return int(result[: result.index(":")])

    def away_score(result: str) -> int:
        return int(result[result.index(":") + 1 :])

    data: List[Dict[str, Any]] = [
        {
            "home_team_score": home_score(result),
            "away_team_score": away_score(result),
            "home_team_win": 1 if home_score(result) > away_score(result) else 0,
            "away_team_win": 1 if home_score(result) < away_score(result) else 0,
            "draw": 1 if home_score(result) == away_score(result) else 0,
        }
        for result in df.loc[:, "result"]
    ]

    return pd.DataFrame(data)


def date_df_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
    def get_date(date: float) -> str:
        date_list: List[str] = str(date).split(".")
        seasons: List[str] = ["15", "16", "17", "18", "19", "20", "21"]
        if date_list[-1] in seasons:
            return "-".join(["20" + date_list[2], date_list[1], date_list[0]])
        return "-".join(["00-00-00"])

    data: List[Dict[str, Any]] = [
        {"season": get_date(str(date)).split("-")[0], "date": get_date(str(date))}
        for date in df.loc[:, "match_date"]
    ]

    return pd.DataFrame(data)


def matches_df_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
    removed_columns: List[str] = [
        "url_id",
        "home_goals",
        "away_goals",
        "home_substitutions",
        "away_substitutions",
        "home_cards",
        "away_cards",
    ]
    matches_df: pd.DataFrame = df.loc[:, ~df.columns.isin(removed_columns)]
    statistics_df: pd.DataFrame = statistics_df_cleanizer(matches_df).reset_index(
        drop=True
    )
    result_df: pd.DataFrame = result_df_cleanizer(matches_df).reset_index(drop=True)
    date_df: pd.DataFrame = date_df_cleanizer(matches_df).reset_index(drop=True)
    matches_df = matches_df.loc[
        :, ~matches_df.columns.isin(["result", "statistics", "match_date"])
    ].reset_index(drop=True)
    return pd.concat([matches_df, statistics_df, result_df, date_df], axis=1)


def penalties_df_cleanizer() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "matches/penalties.csv")
    df = list_df_cleanizer(df, "penalties")
    return df


def appearances_df_cleanizer() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "matches/appearances.csv")

    df["position_name"] = df["position_name"].str.strip()
    df["position_code"] = df["position_name"].copy()
    de_position_names: List[str] = df.groupby("position_name").count().index.tolist()
    position_names: List[str] = [
        "defensive-midfielder",
        "hanging-striker",
        "centre-back",
        "sweeper",
        "left-back",
        "left-midfielder",
        "left-winger",
        "centre-forward",
        "offensive-midfielder",
        "right-back",
        "right-midfielder",
        "right-winger",
        "goal-keeper",
        "central-midfielder",
    ]
    position_codes: List[str] = [
        "DM",
        "HS",
        "CB",
        "S",
        "LB",
        "LM",
        "LW",
        "ST",
        "OM",
        "RB",
        "RM",
        "RW",
        "GK",
        "CM",
    ]

    for de_pos_name, pos_name, pos_code in zip(
        de_position_names, position_names, position_codes
    ):
        df["position_name"] = df["position_name"].mask(
            df["position_name"].isin([de_pos_name]), pos_name
        )
        df["position_code"] = df["position_code"].mask(
            df["position_name"].isin([pos_name]), pos_code
        )

    return df.loc[:, ~df.columns.isin(["url_id"])]


def matches_related_df_cleanizer() -> Dict[str, pd.DataFrame]:
    concated_matches_df: pd.DataFrame = matches_df_concatenator()
    return {
        "matches_df": matches_df_cleanizer(concated_matches_df),
        "goals_df": list_df_concatenator(concated_matches_df, ["home_goals", "away_goals"], ["match_id", "team_id", "scorrer_id", "assist_id", "goal_type"]),
        "substitutions_df": list_df_concatenator(concated_matches_df, ["home_substitutions", "away_substitutions"], ["match_id", "team_id", "player_in_id", "player_out_id"]),
        "cards_df": list_df_concatenator(concated_matches_df, ["home_cards", "away_cards"], ["match_id", "team_id", "player_id", "card"]),
        "penalties": penalties_df_cleanizer(),
        "appearances": appearances_df_cleanizer()
    }


def store_cleanized_matches_dfs() -> None:
    dfs: Dict[str, pd.DataFrame] = matches_related_df_cleanizer()
    dfs["matches_df"].to_csv(CLEANIZED_DIR / "matches.csv", index=False)
    dfs["goals_df"].to_csv(CLEANIZED_DIR / "goals.csv", index=False)
    dfs["substitutions_df"].to_csv(CLEANIZED_DIR / "substitutions.csv", index=False)
    dfs["cards_df"].to_csv(CLEANIZED_DIR / "cards.csv", index=False)
    dfs["penalties"].to_csv(CLEANIZED_DIR / "penalties.csv", index=False)
    dfs["appearances"].to_csv(CLEANIZED_DIR / "player_appearances.csv", index=False)