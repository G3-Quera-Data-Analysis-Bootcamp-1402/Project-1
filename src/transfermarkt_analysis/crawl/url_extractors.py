import os
import urllib3
from bs4 import BeautifulSoup
import pandas as pd

from transfermarkt_analysis.crawl.consts import BASE_URL, LEAGUE_URLS, HEADERS, URLS_DIR, SEASONS_RANGE


http = urllib3.PoolManager(headers=HEADERS)


def player_urls_extractor():
    """
    get player column href attr (url of players profiles) for each season
    """
    for league_url in LEAGUE_URLS.values():
        for season in SEASONS_RANGE:
            resp = http.request(
                "GET", league_url + "/plus/", fields={"saison_id": season}
            )
            soup = BeautifulSoup(resp.data, "html.parser")
            selector = (
                "table > tbody > tr > td:nth-child(1) > div > span.show-for-small > a"
            )
            for result in soup.select(selector, href=True):
                yield {"url": BASE_URL + result["href"]}


def team_urls_extractor():
    """
    get url for each team exist in specific season
    """
    for league_url in LEAGUE_URLS.values():
        for season in SEASONS_RANGE:
            resp = http.request(
                "GET", league_url + "/plus/", fields={"saison_id": season}
            )
            soup = BeautifulSoup(resp.data, "html.parser")
            selector = "h2.content-box-headline.content-box-headline--inverted.content-box-headline--logo > a:nth-child(2)"
            for result in soup.select(selector, href=True):
                yield {"url": BASE_URL + result["href"]}


def store_player_urls():
    """
    call player_urls_extractor and store result as pandas.DataFrame
    and drop duplicates because we can have multiple profiles for same player
    then use .to_csv method to store it as csv file in crawl/data/urls dir
    """
    df = pd.DataFrame(player_urls_extractor())
    df.drop_duplicates().to_csv(URLS_DIR / "player_urls.csv")


def store_team_urls():
    """
    call player_urls_extractor and store result as pandas.DataFrame
    and drop duplicates because we can have multiple profiles for same player
    then use .to_csv method to store it as csv file in crawl/data/urls dir
    """
    df = pd.DataFrame(team_urls_extractor())
    df.drop_duplicates().to_csv(URLS_DIR / "team_urls.csv")


def store_all_urls():
    """
         call all store functions (if .csv file exist in data/urls ignores related store functions)
    """
    store_funcs = {
        "player_urls.csv": store_player_urls,
        "team_urls.csv": store_team_urls,
    }
    
    for csv_file in store_funcs.keys():
        if csv_file in os.listdir(URLS_DIR):
            print(f"already {csv_file} exists in {URLS_DIR}")
        else:
            store_funcs[csv_file]()
