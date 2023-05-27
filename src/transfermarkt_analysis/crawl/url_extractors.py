import os

import pandas as pd
import urllib3
from bs4 import BeautifulSoup

from transfermarkt_analysis.crawl.consts import (BASE_URL, HEADERS,
                                                 LEAGUE_MATCHDAY_URLS,
                                                 LEAGUE_TRANSFERS_URLS,
                                                 MATHDAY_RANGE, SEASONS_RANGE,
                                                 URLS_DIR)

http = urllib3.PoolManager(headers=HEADERS)

# extractor functions


def player_urls_extractor():
    """
    get player column href attr (url of players profiles) for each season
    """
    for league_url in LEAGUE_TRANSFERS_URLS.values():
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
    for league_url in LEAGUE_TRANSFERS_URLS.values():
        for season in SEASONS_RANGE:
            resp = http.request(
                "GET", league_url + "/plus/", fields={"saison_id": season}
            )
            soup = BeautifulSoup(resp.data, "html.parser")
            selector = "h2.content-box-headline.content-box-headline--inverted.content-box-headline--logo > a:nth-child(2)"
            for result in soup.select(selector, href=True):
                yield {"url": BASE_URL + result["href"]}


def matchday_urls_extractor():
    """
    get url for each matchday in each season of each league
    """
    for league_name, league_url in LEAGUE_MATCHDAY_URLS.items():
        for season in SEASONS_RANGE:
            for matchday in MATHDAY_RANGE:
                resp = http.request(
                    "GET",
                    league_url,
                    fields={"saison_id": season, "spieltag": matchday},
                )
                soup = BeautifulSoup(resp.data, "html.parser")
                selector = ".responsive-table > table:nth-child(1) > tbody:nth-child(2) > tr > td:nth-child(7) > span > a"
                for result in soup.select(selector, href=True):
                    yield {"url": BASE_URL + result["href"]}


# store functions


def store_player_urls():
    """
    call player_urls_extractor and store result as pandas.DataFrame
    and drop duplicates because we can have multiple profiles for same player
    then use .to_csv method to store it as csv file in crawl/data/urls dir
    """
    df = pd.DataFrame(player_urls_extractor())
    df.drop_duplicates().to_csv(URLS_DIR / "player_urls.csv", index=False)


def store_team_urls():
    """
    call team_urls_extractor and store result as pandas.DataFrame
    then use .to_csv method to store it as csv file in crawl/data/urls dir
    """
    df = pd.DataFrame(team_urls_extractor())
    df.to_csv(URLS_DIR / "team_urls.csv", index=False)


def store_matchday_urls():
    """
    call matchday_urls_extractor and store result as pandas.DataFrame
    then use .to_csv method to store it as csv file in crawl/data/urls dir
    """
    df = pd.DataFrame(matchday_urls_extractor())
    df.to_csv(URLS_DIR / "matchday_urls.csv", index=False)


def store_all_urls():
    """
    call all store functions (if .csv file exist in data/urls ignores related store functions)
    """
    store_funcs = {
        "player_urls.csv": store_player_urls,
        "team_urls.csv": store_team_urls,
        "matchday_urls.csv": store_matchday_urls,
    }

    for csv_file in store_funcs.keys():
        if csv_file in os.listdir(URLS_DIR):
            print(f"already {csv_file} exists in {URLS_DIR}")
        else:
            store_funcs[csv_file]()
