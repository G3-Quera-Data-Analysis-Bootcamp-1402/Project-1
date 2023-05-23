import pathlib
import urllib3
from bs4 import BeautifulSoup
import pandas as pd

http = urllib3.PoolManager()

headers = {
    "User-Agent": "	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

league_urls = {
    "england": "https://transfermarkt.com/premier-league/transfers/wettbewerb/GB1/plus/",
    "spain": "https://transfermarkt.com/laliga/transfers/wettbewerb/ES1/plus/plus/",
    "germany": "https://transfermarkt.com/bundesliga/transfers/wettbewerb/L1/plus/",
    "italy": "https://transfermarkt.com/serie-a/transfers/wettbewerb/IT1/plus/",
    "france": "https://transfermarkt.com/ligue-1/transfers/wettbewerb/FR1/plus/",
}

urls_dir = pathlib.Path(__file__).resolve().parent / "data/urls"

def player_urls_extractor():
    """
    get player column href attr (url of players profiles) for each season
    """
    for season in range(2015, 2022):
        for league_url in league_urls.values():
            resp = http.request(
                "GET", league_url, headers=headers, fields={"saison_id": season}
            )
            soup = BeautifulSoup(resp.data, "html.parser")
            selectors = (
                "table > tbody > tr > td:nth-child(1) > div > span.show-for-small > a"
            )
            for result in soup.select(selectors, href=True):
                yield {"url": result["href"]}


def store_player_urls():
    """
    call player_urls_extractor and store result as pandas.DataFrame
    and drop duplicates because we can have multiple profiles for same player
    then use .to_csv method to store it as csv file in crawl/data/urls dir
    """
    df = pd.DataFrame(player_urls_extractor())
    df.drop_duplicates().to_csv(urls_dir / "players_url.csv")


def store_all():
    """
         call all store functions
    """
    store_player_urls()
