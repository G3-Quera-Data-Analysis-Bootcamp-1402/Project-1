import os

import pandas as pd
from colorama import Fore
from sqlalchemy import create_engine, Engine


from transfermarkt_analysis.db import db_url
from transfermarkt_analysis.consts import CLEANIZED_DIR


__all__ = [
    "initialize_db",
]


def initialize_db():
    db_engine: Engine = create_engine(db_url)
    
    def get_df(csv_file: str) -> pd.DataFrame:
        return pd.read_csv(CLEANIZED_DIR / f"{csv_file}")
    
    try:
        for csv_file in os.listdir(CLEANIZED_DIR):
            # remove .csv format name.csv -> [name, csv] -> name
            file_name: str = csv_file.split(".")[0]
            db_table: str = file_name
            df: pd.DataFrame = get_df(csv_file)
            df.to_sql(name=db_table, con=db_engine, if_exists="append", index=False)
            print(Fore.GREEN + f"{db_table} table initialized :)")
    except Exception as err:
        raise err