import time
from transfermarkt_analysis.crawl.url_extractors import *
import pandas as pd
from urllib3 import Timeout
from transfermarkt_analysis.db.schema import FootType
from pandas import DataFrame, Series
from tqdm import tqdm
from datetime import datetime
from os import getenv
import dotenv
from sqlalchemy import (TIMESTAMP, Boolean, Column, Date, Enum, ForeignKey, Integer,
                        MetaData, String, Table, Text, create_engine, text)
import regex as re
import sys

from mimesis import Generic, Locale
provider = Generic(Locale.EN)


def load_db_config():
    dotenv.load_dotenv()
    db_conf = {
        "user": getenv("DB_USER", "root"),
        "password": getenv("DB_PASSWORD", ""),
        "host": getenv("DB_HOST", "localhost"),
        "port": getenv("DB_PORT", "3306"),
        "name": getenv("DB_NAME", "transfermarkt"),
    }
    db_url = f"mysql+mysqlconnector://{db_conf['user']}:{db_conf['password']}@{db_conf['host']}:{db_conf['port']}/{db_conf['name']}"
    return db_conf, db_url


def insert_leagues_into_db():
    leagues = pd.DataFrame({"league_id": [0,1,2,3,4,5],\
               "league_name": ["UEFA Champions League", "Premier League", "LaLiga", "Bundesliga", "Serie A", "Ligue 1"],\
               "uefa_coefficient": [1,1,1,1,1,1]})
    print(leagues)
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    with db_engine.connect() as connection:
        for row in leagues.itertuples():
            league_id = row[1]
            league_name = row[2]
            uefa_coefficient = row[3]
            try:
                if len(connection.execute(text(f"SELECT * FROM leagues WHERE league_name = '{league_name}'")).fetchall()) == 0:
                    connection.execute(text(f"INSERT INTO leagues (league_name, uefa_coefficient) VALUES ('{league_name}',{uefa_coefficient})"))
            except:
                pass
            connection.commit()


def insert_seasons_into_db():
    seasons = pd.DataFrame({"season_name": ["20152016","20162017","20172018","20182019","20192020","20202021","20212022"]})
    print(seasons)
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    with db_engine.connect() as connection:
        for row in seasons.itertuples():
            season_name = row[1]
            try:
                if len(connection.execute(text(f"SELECT * FROM seasons WHERE season_name = '{season_name}'")).fetchall()) == 0:
                    connection.execute(text(f"INSERT INTO seasons (season_name) VALUES ('{season_name}')"))
            except:
                pass
            connection.commit()


insert_seasons_into_db()
insert_leagues_into_db()



