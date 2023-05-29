import time
from transfermarkt_analysis.crawl.url_extractors import *
import threading
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
module = sys.modules[__name__]

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


def read_team_urls() -> Series:
    """
    Reads and retrns urls from file: data/team_urls.csv
    """
    return pd.read_csv(URLS_DIR / "team_urls.csv")["url"]




def scrape_team_data(team_url: str, http, headers) -> tuple:
    """
    Gets team id, team name and stadium name for a team url
    """
    
    def reset_user_agent(http, headers):
        headers = {
            "User-Agent": provider.internet.user_agent()
        }
        timeout = Timeout(connect = 10, read = 10)
        http = urllib3.PoolManager(headers=module.headers, timeout= timeout)
        return http, headers


    def generate_team_id(team_url: str) -> int:
        """
        Finds the team_id from extracted url in data/team_urls.csv
        """
        team_id = int(team_url.split("/")[6])
        return team_id
    
    def load_page_soup(team_url: str, http) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the team page
        """
        resp = http.request(
            "GET",
            team_url
        )
        soup = BeautifulSoup(resp.data, "html.parser")
        return soup

    def get_team_name(soup: BeautifulSoup) -> str:
        """
        Gets team name from webpage
        """
        team_name = soup.find("h1",\
            attrs= {"class": "data-header__headline-wrapper data-header__headline-wrapper--oswald"}).text.strip()
        return team_name

    http, headers = reset_user_agent(http, headers)
    try:
        soup = load_page_soup(team_url, http)
        team_id = generate_team_id(team_url)
        team_name = get_team_name(soup)
        return (team_id, team_name)
    except:
        return scrape_team_data(team_url, http, headers)
    
 
def get_teams_df():
    headers = {
            "User-Agent": provider.internet.user_agent()
        }
    timeout = Timeout(connect = 10, read = 10)
    http = urllib3.PoolManager(headers=module.headers, timeout= timeout)
    teams = pd.DataFrame(columns= ["team_id", "team_name"])
    team_urls = read_team_urls()
    for team_url in tqdm(team_urls, desc= "Scraping teams"):
        (team_id, team_name) = scrape_team_data(team_url, http, headers)
        teams.loc[len(teams)] = {"team_id": team_id, "team_name": team_name}
    teams.set_index("team_id", drop= True, inplace= True)
    return teams


def insert_teams_into_db(teams: DataFrame) -> None:
    print(teams)
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    with db_engine.connect() as connection:
        for row in teams.itertuples():
            team_id = row[0]
            team_name = row[1]
            try:
                if len(connection.execute(text(f"SELECT * FROM teams WHERE team_name = '{team_name}'")).fetchall()) == 0:
                    connection.execute(text(f"INSERT INTO teams (team_name) VALUES ('{team_name}')"))
            except:
                pass
            connection.commit()
