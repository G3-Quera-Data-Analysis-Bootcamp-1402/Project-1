from transfermarkt_analysis.crawl.url_extractors import *
from pandas import DataFrame

store_all_urls()

def read_team_urls():
    return pd.read_csv(URLS_DIR / "team_urls.csv")["url"]

def scrape_team_data(team_url: str) -> tuple:
    """
    gets team id, team name and stadium name for a team url
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

    soup = load_page_soup(team_url)
    team_id = generate_team_id(team_url)
    team_name = get_team_name(soup)
    stadium_name = get_team_stadium(soup)
    return (team_id, team_name, stadium_name)
    

def get_teams():
    teams = pd.DataFrame(columns= ["team_id", "team_name", "stadium_name"])
    team_urls = read_team_urls()
    for team_url in team_urls:
        (team_id, team_name, stadium_name) = scrape_team_data(team_url)
        teams.loc[len(teams)] = {"team_id": team_id, "team_name": team_name, "stadium_name": stadium_name}
    teams.set_index("team_id", drop= True, inplace= True)
    return teams
