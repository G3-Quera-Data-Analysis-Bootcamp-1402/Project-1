import os
import re

import numpy as np
import pandas as pd

from transfermarkt_analysis.consts import DATA_DIR


__all__ = [
    "value_cleanizer",
    "matches_df_concatenator",
]


def value_cleanizer(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    cleanize column used for fee, market_value, income
    1- replace -, ? with np.nan
    2- replace leihe with loan -> 1
    3- replace leih-ende with end-loan -> -1.0
    4- replace ablösefrei with free -> 0.0
    5- replace <num>,<num> Mio with <num><num>0000.0
    6- replace <num>,<num> Tsd with <num><num>000.0
    7- replace <num>,<num> € with <num><num>
    """
    df[col] = (
        df[col]
        .mask(df[col].str.lower() == "leihe", "1")
        .mask(df[col].str.contains("Leih-Ende"), "-1")
        .mask(df[col].str.contains("ablösefrei"), "0")
        .apply(
            lambda x: ",".join(re.findall(r"\d+", x)).replace(",", "") + "0000"
            if "Mio" in x
            else x
        )
        .apply(lambda x: "".join(re.findall(r"\d+", x)) + "000" if "Tsd" in x else x)
        .apply(lambda x: "".join(re.findall(r"\d+", x)) if "€" in x else x)
        .mask(df[col].isin(["-", "?", "draft"]), np.nan)
        .astype("float")
    )
    return df


def matches_df_concatenator() -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame()
    MATCHES_DATA_DIR = DATA_DIR / "matches"
    for pt_csv in os.listdir(MATCHES_DATA_DIR):
        if "pt" in pt_csv:
            pt_df: pd.DataFrame = pd.read_csv(MATCHES_DATA_DIR / pt_csv)
            df = pd.concat([df, pt_df])
    df = df.drop_duplicates().dropna()
    return df