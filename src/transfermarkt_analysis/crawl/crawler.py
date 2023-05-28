from transfermarkt_analysis.crawl.url_extractors import *
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

def reset_user_agent():
    module.headers = {
        "User-Agent": provider.internet.user_agent()
    }
    timeout = Timeout(connect = 5, read = 5)
    module.http = urllib3.PoolManager(headers=module.headers, timeout= timeout)


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


def read_player_urls() -> Series:
    """
    Reads and retrns urls from file: data/player_urls.csv
    """
    return pd.read_csv(URLS_DIR / "player_urls.csv")["url"]


def scrape_team_data(team_url: str) -> tuple:
    """
    Gets team id, team name and stadium name for a team url
    """
    
    def generate_team_id(team_url: str) -> int:
        """
        Finds the team_id from extracted url in data/team_urls.csv
        """
        team_id = int(team_url.split("/")[6])
        return team_id
    
    def load_page_soup(team_url: str) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the team page
        """
        resp = module.http.request(
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

    reset_user_agent()
    try:
        soup = load_page_soup(team_url)
        team_id = generate_team_id(team_url)
        team_name = get_team_name(soup)
        return (team_id, team_name)
    except:
        return scrape_team_data(team_url)
    

def scrape_player_data(player_url: str) -> tuple:
    """
    gets player data
    """
    def generate_player_id(player_url: str) -> int:
        """
        Finds the player_id from extracted url in data/player_urls.csv
        """
        team_id = int(player_url.split("/")[6])
        return team_id
    
    def load_page_soup(player_url: str) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the player page
        """
        resp = module.http.request(
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

    reset_user_agent()
    try:
        soup = load_page_soup(player_url)
        player_id = generate_player_id(player_url)
        player_name = get_player_name(soup)
        date_of_birth = get_dob(soup)
        height = get_height(soup)
        citizenship = get_citizenship(soup)
        foot = get_foot(soup)
        return (player_id, player_name, date_of_birth, height, citizenship, foot)
    except:
        return scrape_player_data(player_url)
    

def scrape_transfers_data(season_start_year: int, league_url: str) -> DataFrame:
    
    def generate_url(league_url, season_start_year: int):
        """
        generates transfers_url
        """
        url_parts = league_url.split("/")
        
        transfers_url = url_parts[0] + "/" + url_parts[1] + "/" + url_parts[2] + "/" + url_parts[3] + "/transfers/" + url_parts[5] + "/" + url_parts[6] + f"/plus/?saison_id={str(season_start_year)}&s_w=&leihe=1&intern=0&intern=1"

        return transfers_url
    

    def load_page_soup(transfers_url: str) -> BeautifulSoup:
        """
        Makes a BeautifulSoup object of the league transfers page
        """
        resp = module.http.request(
            "GET",
            transfers_url
        )
        soup = BeautifulSoup(resp.data, "html.parser")
        return soup
    
    def get_transfers(soup: BeautifulSoup) -> DataFrame:
        df = pd.DataFrame(columns = ["player_id", "season_id", "left_team", "joined_team", "fee_of_transfer"])
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

        team_tables = soup.find_all("div", attrs= {"class": "box"})
        for team_table in team_tables[3:-2]:
            try:
                team_name = team_table.h2.a["title"]
                transfer_tables = team_table.find_all("div", attrs= {"class": "responsive-table"})
            except:
                pass
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
                    player_market_value = cell_elements[5].font.font.text.strip()
                    player_market_value = decode_market_value(player_market_value)
                except:
                    try:
                        player_market_value = cell_elements[5].text.strip()
                        player_market_value = decode_market_value(player_market_value)
                    except:
                        print(cell_elements[5].text)
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
                df.loc[len(df)] = {"player_id": player_id, "season_id": season_start_year, "left_team": from_club, "joined_team": team_name, "fee_of_transfer": fee}
            
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
                    player_market_value = decode_market_value(player_market_value)
                except:
                    try:
                        player_market_value = cell_elements[5].text.strip()
                        player_market_value = decode_market_value(player_market_value)
                    except:
                        print(cell_elements[5].text)
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
                df.loc[len(df)] = {"player_id": player_id, "season_id": season_start_year, "left_team": team_name, "joined_team": from_club, "fee_of_transfer": fee}
        return df

    reset_user_agent()
    try:
        transfers_url = generate_url(league_url, season_start_year)
        soup = load_page_soup(transfers_url)

        df = get_transfers(soup)
        return df
    except:
        return scrape_transfers_data(season_start_year, league_url)



def get_teams_df():
    reset_user_agent()
    teams = pd.DataFrame(columns= ["team_id", "team_name"])
    team_urls = read_team_urls()
    for team_url in tqdm(team_urls, desc= "Scraping teams"):
        (team_id, team_name) = scrape_team_data(team_url)
        teams.loc[len(teams)] = {"team_id": team_id, "team_name": team_name}
    teams.set_index("team_id", drop= True, inplace= True)
    return teams



def get_transfers_df() -> DataFrame:
    transfers_df = pd.DataFrame(columns = ["player_id", "season_id", "left_team", "joined_team", "fee_of_transfer"])
    db_conf, db_url = load_db_config()
    db_engine = create_engine(db_url)
    leagues = pd.read_csv(URLS_DIR / "league_urls.csv")
    with db_engine.connect() as connection:
        seasons = connection.execute(text("SELECT season_name FROM seasons")).fetchall()
        for season_tuple in tqdm(seasons, desc= "seasons"):
            season_name = season_tuple[0]
            for league in tqdm(leagues.itertuples(), desc= "leagues:"):
                league_name = league[2]
                league_url = league[1]
                if league_name != "UEFA Champions League":
                    df = scrape_transfers_data(int(season_name[:4]), league_url)
                    transfers_df = pd.concat([transfers_df, df], ignore_index= True)
    return transfers_df


def get_players_df():
    reset_user_agent()
    players = pd.DataFrame(columns= ["player_id", "player_name", "date_of_birth", "height", "citizenship", "foot"])
    player_urls = read_player_urls()
    for player_url in tqdm(player_urls, desc= "Scraping players"):
        (player_id, player_name, date_of_birth, height, citizenship, foot) = scrape_player_data(player_url)
        players.loc[len(players)] = {"player_id": player_id, "player_name": player_name, "date_of_birth": date_of_birth,\
                                     "height": height, "citizenship": citizenship, "foot": foot}
    players.set_index("player_id", drop= True, inplace= True)
    return players


def insert_players_into_db(players: DataFrame) -> None:
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
                if len(connection.execute(text(f"SELECT * FROM player WHERE player_name = '{player_name}'")).fetchall()) == 0:
                    connection.execute(text(f"INSERT INTO player (player_name,date_of_birth,height,citizenship,foot) VALUES ('{player_name}',{date_of_birth},{height},'{citizenship}',{foot})"))
            except:
                pass
            connection.commit()


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


def insert_transfers_into_db(df: DataFrame):
    """ "player_id", "season_id", "left_team", "joined_team", "fee_of_transfer" """
    df.to_csv("data/transfers.csv")


#insert_seasons_into_db()
#insert_leagues_into_db()
#insert_transfers_into_db(get_transfers_df())
#insert_teams_into_db(get_teams_df())
#insert_players_into_db(get_players_df())
