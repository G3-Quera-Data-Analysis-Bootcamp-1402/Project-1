import pathlib


__all__ = [
    "BASE_URL",
    "LEAGUE_TRANSFERS_URLS",
    "LEAGUE_MATCHDAY_URLS",
    "HEADERS",
    "SEASONS_RANGE",
    "MATCHDAY_RANGE",
    "DATA_DIR",
    "URLS_DIR",
    "CLEANIZED_DIR"
]


BASE_URL = "https://transfermarkt.de"

LEAGUE_TRANSFERS_URLS = {
    "england": "https://transfermarkt.de/premier-league/transfers/wettbewerb/GB1",
    "spain": "https://transfermarkt.de/laliga/transfers/wettbewerb/ES1",
    "germany": "https://transfermarkt.de/bundesliga/transfers/wettbewerb/L1",
    "italy": "https://transfermarkt.de/serie-a/transfers/wettbewerb/IT1",
    "france": "https://transfermarkt.de/ligue-1/transfers/wettbewerb/FR1",
}

LEAGUE_MATCHDAY_URLS = {
    "england": "https://www.transfermarkt.de/premier-league/spieltagtabelle/wettbewerb/GB1/",
    "spain": "https://transfermarkt.de/laliga/spieltagtabelle/wettbewerb/ES1",
    "germany": "https://transfermarkt.de/bundesliga/spieltagtabelle/wettbewerb/L1",
    "italy": "https://transfermarkt.de/serie-a/spieltagtabelle/wettbewerb/IT1",
    "france": "https://transfermarkt.de/ligue-1/spieltagtabelle/wettbewerb/FR1",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

SEASONS_RANGE = range(2015, 2022)

MATCHDAY_RANGE = range(1, 39)

# for get easy access to data/urls directory and by adding / you can add path
# example for accessing to player_urls.csv URLS_DIR / "player_urls.csv" -> data/urls/player_urls.csv
DATA_DIR = pathlib.Path("data").resolve()
URLS_DIR = DATA_DIR / "urls"
CLEANIZED_DIR = DATA_DIR / "cleanized"