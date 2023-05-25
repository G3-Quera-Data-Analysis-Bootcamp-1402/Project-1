from transfermarkt_analysis.crawl.url_extractors import *
from pandas import DataFrame, Series
from tqdm import tqdm
from datetime import datetime

store_all_urls()

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
    
    def get_team_stadium(soup: BeautifulSoup) -> str:
        """
        Gets stadium name for team
        """
        selector = "#main > main > header > div.data-header__info-box > div > ul:nth-child(2) > li:nth-child(2) > span > a"
        stadium_name = soup.select_one(selector).text.strip()
        return stadium_name
    
    def get_in_leauge_since(soup: BeautifulSoup) -> str:
        """
        Gets "in league since" field
        """
        selector = "#main > main > header > div.data-header__box--big > div > span:nth-child(4) > span > a"
        in_league_since = soup.select_one(selector).text.strip()
        return in_league_since

    soup = load_page_soup(team_url)
    team_id = generate_team_id(team_url)
    team_name = get_team_name(soup)
    stadium_name = get_team_stadium(soup)
    in_league_since = get_in_leauge_since(soup)
    return (team_id, team_name, stadium_name, in_league_since)
    

def get_teams():
    teams = pd.DataFrame(columns= ["team_id", "team_name", "stadium_name", "in_league_since"])
    team_urls = read_team_urls()
    for team_url in tqdm(team_urls, desc= "Scraping teams"):
        (team_id, team_name, stadium_name, in_league_since) = scrape_team_data(team_url)
        teams.loc[len(teams)] = {"team_id": team_id, "team_name": team_name,\
                                 "stadium_name": stadium_name, "in_league_since": in_league_since}
    teams.set_index("team_id", drop= True, inplace= True)
    return teams

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
        name_string = soup.find("h1", attrs= {"class": "data-header__headline-wrapper"}).text.strip()
        if "\n" in name_string:
            name_string = name_string.split("\n")[1].strip()
        return name_string
    
    def get_dob(soup: BeautifulSoup) -> int:
        """
        returns player's date of birth as POSIX timestamp
        """
        dob = soup.find("span", attrs= {"itemprop": "birthDate"}).text.strip().lower()[:12].strip()
        
        if dob[4] == ' ':
            dob = dob[:4] + "0" + dob[4:]

        datetime_object = datetime.strptime(dob, '%b %d, %Y')
        timestamp = int(datetime.timestamp(datetime_object))
        return timestamp
    
    def get_height(soup: BeautifulSoup) -> int:
        """
        returns player height in cm
        """
        height_string = soup.find("span", attrs= {"itemprop": "height"}).text.strip()
        meters = int(height_string[:4].split(",")[0])
        centimeters = int(height_string[:4].split(",")[1])
        height_in_cm = meters * 100 + centimeters
        return height_in_cm
    
    def get_citizenship(soup: BeautifulSoup) -> str:
        """
        returns player citizenship
        """
        citizenship_string = soup.find("span", attrs= {"itemprop": "nationality"}).text.strip()
        return citizenship_string
    
    def get_foot(soup: BeautifulSoup) -> str:
        """
        returns foot preference for player
        """
        elements = soup.find_all("span", attrs= {"class": "info-table__content info-table__content--bold"})
        for element in elements:
            if element.text in ["right", "left", "both"]:
                foot = element.text
                break
        return foot

    soup = load_page_soup(player_url)
    player_id = generate_player_id(player_url)
    player_name = get_player_name(soup)
    date_of_birth = get_dob(soup)
    height = get_height(soup)
    citizenship = get_citizenship(soup)
    foot = get_foot(soup)
    return (player_id, player_name, date_of_birth, height, citizenship, foot)
    
def get_players():
    players = pd.DataFrame(columns= ["player_id", "player_name", "date_of_birth", "height", "citizenship", "foot"])
    player_urls = read_player_urls()
    for player_url in tqdm(player_urls, desc= "Scraping players"):
        (player_id, player_name, date_of_birth, height, citizenship, foot) = scrape_player_data(player_url)
        players.loc[len(players)] = {"player_id": player_id, "player_name": player_name, "date_of_birth": date_of_birth,\
                                     "height": height, "citizenship": citizenship, "foot": foot}
    players.set_index("player_id", drop= True, inplace= True)
    return players

print(get_teams())
print(get_players())