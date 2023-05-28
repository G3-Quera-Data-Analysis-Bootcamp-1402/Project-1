import re

import numpy as np
import pandas as pd

from transfermarkt_analysis.crawl.consts import DATA_DIR

CLEANIZED_DIR = DATA_DIR / "cleanized"
DF: pd.DataFrame = pd.read_csv(DATA_DIR / "transfers.csv")


def fee_cleanizer(df: pd.DataFrame) -> pd.DataFrame:
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
            lambda x: ",".join(re.findall(r"\d+", x)).replace(",", "") + "0000" if "Mio" in x else x
        )
        .apply(
            lambda x: "".join(re.findall(r"\d+", x)) + "000" if "Tsd" in x else x
        )
        .apply(
            lambda x: "".join(re.findall(r"\d+", x)) if "€" in x else x
        )
        .mask(df["fee_of_transfer"].isin(["-", "?", "draft"]), np.nan)
        .astype("float")
    )
    return df


def transfers_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "transfers.csv", index_col=0)
    df = fee_cleanizer(df)
    return df


def initialize_cleanized_transfers() -> None:
    df: pd.DataFrame = transfers_cleanizer()
    df = df.dropna().drop_duplicates()
    df.to_csv(CLEANIZED_DIR / "transfers.csv", index=False)

initialize_cleanized_transfers()