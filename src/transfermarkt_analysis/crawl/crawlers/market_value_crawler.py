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
    https://transfermarkt.de/inter-mailand/transfers/verein/46/saison_id/2015
    https://transfermarkt.de/inter-mailand/startseite/verein/46/saison_id/2016
    https://transfermarkt.de/fc-chelsea/kader/verein/631/saison_id/2015
    """
    urls = pd.read_csv(URLS_DIR / "team_urls.csv")["url"]
    urls = pd.Series([url.split("transfers")[0] + f"kader/verein/{url.split('/')[6]}/saison_id/" + url.split("/")[-1] for url in urls])
    return urls

def scrape_team_data(team_url, http, headers) -> tuple:
    """
    Gets team id, team name and stadium name for a team url
    """
    
    def reset_user_agent(http, headers):
        headers = {
            "User-Agent": provider.internet.user_agent()
        }
        timeout = Timeout(connect = 10, read = 10)
        http = urllib3.PoolManager(headers=headers, timeout= timeout)
        return http, headers
    
    def load_page_soup(team_url, http) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the team page
        """
        resp = http.request(
            "GET",
            team_url
        )
        soup = BeautifulSoup(resp.data, "html.parser")
        return soup

    def get_player_market_values(soup):
        
        df = pd.DataFrame(columns = ["player_name", "season", "market_value"])
        rows = soup.find_all("tr")
        for row in rows:
            try:                       
                market_value = row.find("td", attrs= {"class": "rechts hauptlink"}).text.strip()
            except:
                continue
            links = row.find_all("a") 
            for link in links:
                if "profil/spieler" in link["href"]:
                    player_name = link.text.strip()
                df.loc[len(df)] = {"player_name": player_name, "season": team_url.split("/")[-1], "market_value": market_value}
            else:
                continue
        df.drop_duplicates("player_name", inplace= True)
        return df


    http, headers = reset_user_agent(http, headers)
    try:
        soup = load_page_soup(team_url, http)
        player_market_values = get_player_market_values(soup)
        return player_market_values
    except:
        http, headers = reset_user_agent(http, headers)
        return scrape_team_data(team_url, http, headers)
    
 
def get_market_values_df():
    lock = threading.Lock()
    results = []
    headers = {
            "User-Agent": provider.internet.user_agent()
        }
    timeout = Timeout(connect = 10, read = 10)
    http = urllib3.PoolManager(headers=headers, timeout= timeout)

    def proccess_input(team_url, http, headers):
        df = scrape_team_data(team_url, http, headers)
        with lock:
            results.append(df)

    team_urls = read_team_urls()

    threads = []

    for team_url in tqdm(team_urls, desc= "Scraping market values"):
        thread = threading.Thread(target = proccess_input, args = (team_url, http, headers))
        thread.start()
        threads.append(thread)
        if (len(threads) % 20) == 0:
            for thread in threads:
                thread.join()
    for thread in threads:
                thread.join()
    
    market_values_df = pd.concat(results, ignore_index = True)
    return market_values_df


def insert_market_values_into_db(market_values: DataFrame) -> None:
    print(market_values)
    market_values.to_csv("data/market_values.csv")
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    with db_engine.connect() as connection:
        for row in market_values.itertuples():
            pass


#insert_market_values_into_db(get_market_values_df())
