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



def read_player_urls() -> Series:
    """
    Reads and retrns urls from file: data/player_urls.csv
    """
    return pd.read_csv(URLS_DIR / "player_urls.csv")["url"]


def scrape_player_data(player_url: str, http, headers) -> tuple:
    """
    gets player data
    """
    
    def reset_user_agent(http, headers):
        headers = {
            "User-Agent": provider.internet.user_agent()
        }
        timeout = Timeout(connect = 10, read = 10)
        http = urllib3.PoolManager(headers=headers, timeout= timeout)
        return http, headers
    
    def generate_player_id(player_url: str) -> int:
        """
        Finds the player_id from extracted url in data/player_urls.csv
        """
        team_id = int(player_url.split("/")[6])
        return team_id
    
    def load_page_soup(player_url: str, http) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the player page
        """
        resp = http.request(
            "GET",
            player_url
        )
        soup = BeautifulSoup(resp.data, "html.parser")
        return soup
    
    def get_player_name(soup: BeautifulSoup) -> str:
        """
        returns player name
        """
        name_string = soup.find("h1", attrs= {"class": "data-header__headline-wrapper"}).strong.text.strip()
        if "\n" in name_string:
            name_string = name_string.split("\n")[1].strip()
        return name_string
    
    def get_dob(soup: BeautifulSoup) -> int:
        """
        returns player's date of birth as POSIX timestamp
        """
        dob = soup.find("span", attrs= {"itemprop": "birthDate"}).text.strip().lower()[:12].strip()
        try:
            datetime_object = datetime.strptime(dob, '%d.%m.%Y')
            timestamp = int(datetime.timestamp(datetime_object))
        except:
            return 0
        return timestamp
    
    def get_height(soup: BeautifulSoup) -> int:
        """
        returns player height in cm
        """
        try:
            height_string = soup.find("span", attrs= {"itemprop": "height"}).text.strip()
            meters = int(height_string[:4].split(",")[0])
            centimeters = int(height_string[:4].split(",")[1])
            height_in_cm = meters * 100 + centimeters
        except:
            height_in_cm = 0
        return height_in_cm
    
    def get_citizenship(soup: BeautifulSoup) -> str:
        """
        returns player citizenship
        """
        try:
            citizenship_string = soup.find("span", attrs= {"itemprop": "nationality"}).text.strip()
            return citizenship_string
        except:
            return "None"
    
    def get_foot(soup: BeautifulSoup) -> str:
        """
        returns foot preference for player
        """
        try:
            elements = soup.find_all("span", attrs= {"class": "info-table__content info-table__content--bold"})
            for element in elements:
                if element.text in ["rechts", "links", "beidfüßig"]:
                    if element.text == "rechts":
                        return FootType.right
                    elif element.text == "links":
                        return FootType.left
                    else:
                        return FootType.both
            else:
                return FootType.right
        except:
            return FootType.right

    http, headers = reset_user_agent(http, headers)
    try:
        soup = load_page_soup(player_url, http)
        player_id = generate_player_id(player_url)
        player_name = get_player_name(soup)
        date_of_birth = get_dob(soup)
        height = get_height(soup)
        citizenship = get_citizenship(soup)
        foot = get_foot(soup)
        return (player_id, player_name, date_of_birth, height, citizenship, foot)
    except:
        time.sleep(5)
        return scrape_player_data(player_url, http, headers)



def get_players_df():
    lock = threading.Lock()
    results = []
    headers = {
            "User-Agent": provider.internet.user_agent()
        }
    timeout = Timeout(connect = 10, read = 10)
    http = urllib3.PoolManager(headers=headers, timeout= timeout)
    def process_input(player_url: str, http, headers):

        (player_id, player_name, date_of_birth, height, citizenship, foot) = scrape_player_data(player_url, http, headers)
        with lock:
            results.append((player_id, player_name, date_of_birth, height, citizenship, foot))
    
    player_urls = read_player_urls()
    threads = []
    for player_url in tqdm(player_urls, desc= "Scraping players"):
        thread = threading.Thread(target= process_input, args=(player_url, http, headers))
        thread.start()
        threads.append(thread)
        if (len(threads) % 20) == 0:
            for thread in threads:
                thread.join()

    for thread in threads:
                thread.join()
    
    players = pd.DataFrame(columns= ["player_id", "player_name", "date_of_birth", "height", "citizenship", "foot"])
    
    for result in results:
        player_id = result[0]
        player_name = result[1]
        date_of_birth = result[2]
        height = result[3]
        citizenship = result[4]
        foot = result[5]
        players.loc[len(players)] = {"player_id": player_id, "player_name": player_name, "date_of_birth": date_of_birth,\
                                     "height": height, "citizenship": citizenship, "foot": foot}

    players.set_index("player_id", drop= True, inplace= True)
    return players


def insert_players_into_db(players: DataFrame) -> None:
    players.to_csv("data/players.csv")
    print(players)
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    with db_engine.connect() as connection:
        for row in players.itertuples():
            player_id = row[0]
            player_name = row[1]
            date_of_birth = row[2]
            height = row[3]
            citizenship = row[4]
            foot = row[5]
            try:
                connection.execute(text(f"INSERT INTO player (player_name,date_of_birth,height,citizenship,foot) VALUES ('{player_name}',{date_of_birth},{height},'{citizenship}',{foot})"))
            except:
                pass
            connection.commit()


#insert_players_into_db(get_players_df())