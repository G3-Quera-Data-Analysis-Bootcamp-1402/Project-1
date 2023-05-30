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
    try:
        for csv_file in os.listdir(CLEANIZED_DIR):
            # remove .csv and get file name
            # beacause we need it (they have same name as db tables)
            csv_file_name = csv_file.split(".")[0]
            df: pd.DataFrame = pd.read_csv(csv_file)
            df.to_sql(csv_file_name, con=db_engine, if_exists="append")
            print(Fore + f"{csv_file_name} table data initialized :)")
    except Exception as err:
        raise err