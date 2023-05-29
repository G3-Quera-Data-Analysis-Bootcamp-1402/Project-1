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


   

def scrape_transfers_data(season_start_year: int, league_url: str, http, headers) -> DataFrame:
    
    def reset_user_agent(http, headers):
        headers = {
            "User-Agent": provider.internet.user_agent()
        }
        timeout = Timeout(connect = 10, read = 10)
        http = urllib3.PoolManager(headers=module.headers, timeout= timeout)
        return http, headers

    def generate_url(league_url, season_start_year: int):
        """
        generates transfers_url
        """
        url_parts = league_url.split("/")
        
        transfers_url = url_parts[0] + "/" + url_parts[1] + "/" + url_parts[2] + "/" + url_parts[3] + "/transfers/" + url_parts[5] + "/" + url_parts[6] + f"/plus/?saison_id={str(season_start_year)}&s_w=&leihe=1&intern=0&intern=1"

        return transfers_url
    

    def load_page_soup(transfers_url: str, http) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the league transfers page
        """
        resp = http.request(
            "GET",
            transfers_url
        )
        soup = BeautifulSoup(resp.data, "html.parser")
        return soup
    
    def get_transfers(soup: BeautifulSoup) -> DataFrame:
        df = pd.DataFrame(columns = ["player_name","player_id", "season_id", "left_team", "joined_team", "market_value", "fee_of_transfer"])
        def decode_market_value(player_market_value):
            player_market_value = player_market_value.replace(",", ".")
            if "k" in player_market_value: 
                numeric_part = re.match("[^k]+", player_market_value).captures()[0].strip()
                player_market_value = float(numeric_part) * 1000
            elif "thousand" in player_market_value:
                numeric_part = re.match("[^thousand]+", player_market_value).captures()[0].strip()
                player_market_value = float(numeric_part) * 1000
            elif "m" in player_market_value:
                numeric_part = re.match("[^m€]+", player_market_value).captures()[0].strip()
                player_market_value = float(numeric_part) * 1000000
            elif "Mio" in player_market_value:
                numeric_part = re.match("[^Mio]+", player_market_value).captures()[0].strip()
                player_market_value = float(numeric_part) * 1000000
            elif "Tsd" in player_market_value:
                numeric_part = re.match("[^Tsd]+", player_market_value).captures()[0].strip()
                player_market_value = float(numeric_part) * 1000
            else:
                player_market_value = 0
            return player_market_value

        team_tables = soup.find_all("div", attrs= {"class": "box"})[3:-2]
        team_income_expenditure = pd.DataFrame(columns= ["team_name", "income", "expenditure"])
        for team_table in team_tables:
            
            try:
                expenditure = team_table.find("div", attrs= {"class": "transfer-zusatzinfo-box"}).find("span", attrs= {"class": "transfer-einnahmen-ausgaben redtext"}).text.strip()
            except:
                expenditure = 0
            
            try:
                income = team_table.find_all("div", attrs= {"class": "responsive-table"})[1].find("div", attrs= {"class": "transfer-zusatzinfo-box"}).find("span", attrs= {"class": "transfer-einnahmen-ausgaben greentext"}).text.strip()
            except:
                income = 0
            
            try:
                team_name = team_table.h2.a["title"]
                transfer_tables = team_table.find_all("div", attrs= {"class": "responsive-table"})
            except:
                pass
            
            team_income_expenditure.loc[len(team_income_expenditure)] = {"team_name": team_name, "income": income, "expenditure": expenditure}
            
            for row_element in transfer_tables[0].table.tbody.find_all("tr"):
                cell_elements = row_element.find_all("td")
                try:
                    player_name = cell_elements[0].div.span.a["title"].strip()
                except:
                    player_name = "error"
                player_id = int(cell_elements[0].div.span.a["href"].split("/")[-1])
                try:
                    player_age = int(cell_elements[1].font.font.text.strip())
                except:
                    try:
                        player_age = int(cell_elements[1].text.strip())
                    except:
                        player_age = int(cell_elements[1].text.strip()[1:])
                try:
                    player_nationality = cell_elements[2].img["title"].strip()
                except:
                    player_nationality = "0"
                try:
                    player_position = cell_elements[3].font.font.text.strip()
                except:
                    player_position = cell_elements[3].text.strip()
                try:
                    player_market_value = cell_elements[5].text.strip()
                except:
                    player_market_value = 0
                try:
                    from_club = cell_elements[7].a["title"].strip()
                except: 
                    from_club = "0"
                try:
                    from_club_nationality = cell_elements[7].img["title"].strip()
                except:
                    from_club_nationality = "0"
                try:
                    fee = cell_elements[-1].a.font.font.text.strip()
                except:
                    fee = cell_elements[-1].a.text.strip()
                try:
                    trasnfer_id = int(cell_elements[-1].a["href"].split("/")[-1].strip())
                except:
                    trasnfer_id = 0
                #print(from_club, from_club_nationality, team_name, player_name, player_id, player_age, player_nationality, player_position, player_market_value, fee, trasnfer_id)
                df.loc[len(df)] = {"player_name": player_name ,"player_id": player_id, "season_id": season_start_year, "left_team": from_club, "joined_team": team_name, "market_value": player_market_value, "fee_of_transfer": fee}
            
            for row_element in transfer_tables[1].table.tbody.find_all("tr"):
                cell_elements = row_element.find_all("td")
                try:
                    player_name = cell_elements[0].div.span.a["title"].strip()
                except:
                    player_name = "error"
                player_id = int(cell_elements[0].div.span.a["href"].split("/")[-1])
                try:
                    player_age = int(cell_elements[1].font.font.text.strip())
                except:
                    try:
                        player_age = int(cell_elements[1].text.strip())
                    except:
                        player_age = int(cell_elements[1].text.strip()[1:])
                try:
                    player_nationality = cell_elements[2].img["title"].strip()
                except:
                    player_nationality = "0"
                try:
                    player_position = cell_elements[3].font.font.text.strip()
                except:
                    player_position = cell_elements[3].text.strip()
                try:
                    player_market_value = cell_elements[5].font.font.text.strip()
                except:
                    player_market_value = 0
                try:
                    from_club = cell_elements[7].a["title"].strip()
                except: 
                    from_club = "0"
                try:
                    from_club_nationality = cell_elements[7].img["title"].strip()
                except:
                    from_club_nationality = "0"
                try:
                    fee = cell_elements[-1].a.font.font.text.strip()
                except:
                    fee = cell_elements[-1].a.text.strip()
                try:
                    trasnfer_id = int(cell_elements[-1].a["href"].split("/")[-1].strip())
                except:
                    trasnfer_id = 0
                #print(from_club, from_club_nationality, team_name, player_name, player_id, player_age, player_nationality, player_position, player_market_value, fee, trasnfer_id)
                df.loc[len(df)] = {"player_name": player_name, "player_id": player_id, "season_id": season_start_year, "left_team": team_name, "joined_team": from_club, "market_value": player_market_value, "fee_of_transfer": fee}
        return df, team_income_expenditure

    http, headers = reset_user_agent(http, headers)
    try:
        transfers_url = generate_url(league_url, season_start_year)
        soup = load_page_soup(transfers_url, http)

        df, team_income_expenditure = get_transfers(soup)
        return df, team_income_expenditure
    except:
        return scrape_transfers_data(season_start_year, league_url, http, headers)


def get_transfers_df() -> DataFrame:
    headers = {
            "User-Agent": provider.internet.user_agent()
        }
    timeout = Timeout(connect = 10, read = 10)
    http = urllib3.PoolManager(headers=module.headers, timeout= timeout)
    transfers_df = pd.DataFrame(columns = ["player_id", "season_id", "left_team", "joined_team", "fee_of_transfer"])
    team_income_expenditures = pd.DataFrame(columns= ["season", "team_name", "income", "expenditure"])
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    leagues = pd.read_csv(URLS_DIR / "league_urls.csv")
    with db_engine.connect() as connection:
        seasons = connection.execute(text("SELECT season_name FROM seasons")).fetchall()
        for season_tuple in tqdm(seasons, desc= "seasons"):
            season_name = season_tuple[0]
            for league in tqdm(list(leagues.itertuples()), desc= "leagues:"):
                league_name = league[2]
                league_url = league[1]
                if league_name != "UEFA Champions League":
                    df, team_income_expenditure = scrape_transfers_data(int(season_name[:4]), league_url, http, headers)
                    transfers_df = pd.concat([transfers_df, df], ignore_index= True)
                    team_income_expenditure["season"] = season_name
                    team_income_expenditures = pd.concat([team_income_expenditures, team_income_expenditure], ignore_index= True)


    return transfers_df, team_income_expenditures


def insert_transfers_into_db(df: DataFrame):

    df[0].to_csv("data/transfers.csv")
    df[1].to_csv("data/team_income_expenditures.csv")


insert_transfers_into_db(get_transfers_df())