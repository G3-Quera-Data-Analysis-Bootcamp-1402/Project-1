import threading
from dataclasses import asdict
from time import sleep
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from transfermarkt_analysis.consts import DATA_DIR, URLS_DIR
from transfermarkt_analysis.crawl.crawlers.base import *
from transfermarkt_analysis.crawl.structs import MatchAppearance, MatchAppearances


def appearances_extractor(resp: requests.Response) -> List[MatchAppearance]:
    def appearance_extractor(
        match_id: str, team_id: str, player: Tag, postion: Tag
    ) -> MatchAppearance:
        return MatchAppearance(
            match_id=match_id,
            team_id=team_id,
            player_id=obj_id(player["href"]),
            position_name=postion.get_text().split(",")[0],
        )

    soup: BeautifulSoup = BeautifulSoup(markup=resp.text, features="html.parser")
    match_id: str = obj_id(resp.url)
    selectors: Dict[str, str] = {
        "home_team": "div.box.sb-spielbericht-head div.box-content div.sb-team.sb-heim a.sb-vereinslink",
        "away_team": "div.box.sb-spielbericht-head div.box-content div.sb-team.sb-gast a.sb-vereinslink",
        "home_players": "div.row:nth-child(9) > div:nth-child(1) > div.box > div.responsive-table > table.items > tr > td > table.inline-table > tr > td > a.wichtig",
        "home_positions": "div.row:nth-child(9) > div:nth-child(1) > div.box > div.responsive-table > table.items > tr > td > table.inline-table > tr:nth-child(2) > td",
        "away_players": "div.row:nth-child(9) > div:nth-child(2) > div.box > div.responsive-table > table.items > tr > td > table.inline-table > tr > td > a.wichtig",
        "away_positions": "div.row:nth-child(9) > div:nth-child(2) > div.box > div.responsive-table > table.items > tr > td > table.inline-table > tr:nth-child(2) > td",
    }

    home_team: Tag = soup.select_one(selectors["home_team"], href=True)
    away_team: Tag = soup.select_one(selectors["away_team"], href=True)
    home_team_id: str = None
    away_team_id: str = None

    try:
        home_team_id = obj_id(home_team["href"])
        away_team_id = obj_id(away_team["href"])
    except Exception:
        pass

    home_appearances: List[MatchAppearance] = [
        appearance_extractor(match_id, home_team_id, player, position)
        for player, position in zip(
            soup.select(selectors["home_players"]),
            soup.select(selectors["home_positions"]),
        )
    ]

    away_appearances: List[MatchAppearance] = [
        appearance_extractor(match_id, away_team_id, player, position)
        for player, position in zip(
            soup.select(selectors["away_players"]),
            soup.select(selectors["away_positions"]),
        )
    ]

    appearances: List[MatchAppearance] = home_appearances + away_appearances

    for appearance in appearances:
        yield appearance


def appearance_writer(url_id: int, resp: requests.Response, filename: str):
    appearance_df: pd.DataFrame = pd.DataFrame(
        list(map(lambda a: {"url_id": url_id, **asdict(a)}, appearances_extractor(resp)))
    )
    appearance_df.to_csv(
        DATA_DIR / f"matches/{filename}.csv", mode="a", index=False, header=False
    )


def appearance_crawler(df: pd.DataFrame, filename: str):
    counter: int = 0
    index_list: Iterable = iter(df.index.values.tolist())
    url_list: Iterable = iter(df["url"].tolist())
    for url_id, url in zip(index_list, url_list):
        print(f"getting {url_id} {url}")

        resp: requests.Response = make_request(url)

        while resp is None or resp.status_code != 200:
            url_id = next(index_list)
            url = next(url_list)
            print(f"getting instead {url_id} {url}")
            resp = make_request(url)

        if resp is not None:
            if resp.status_code == 200:
                appearance_writer(url_id, resp, filename)
                print(f"{resp.status_code} got {url_id} {url}")
                counter += 1

        if counter % 50 == 0:
            counter = 0
            sleep(30)


def appearance_partion_crawler(filename: str, start: int, end: int) -> None:
    df: pd.DataFrame = pd.read_csv(URLS_DIR / "appearance_urls.csv").iloc[start:end,]
    appearance_crawler(get_matchday_urls_df(df, filename), filename)


def multi_appearances_partion_crawler(
    filename: str, start: int, end: int, step: int = 100
) -> None:
    limits: List[int] = list(range(start, end + 1, step))
    partions: List[Tuple[int, int]] = [
        (limits[i], limits[i + 1]) for i in range(len(limits) - 1)
    ]
    threads: List[threading.Thread] = []
    for partion in partions:
        thread = threading.Thread(
            target=appearance_partion_crawler,
            args=(filename, partion[0], partion[1]),
        )
        threads.append(thread)
        thread.start()

    for thrd in threads:
        thrd.join()
