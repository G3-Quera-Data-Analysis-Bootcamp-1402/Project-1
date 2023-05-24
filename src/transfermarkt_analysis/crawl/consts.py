import pathlib

BASE_URL = "https://transfermarkt.com"

LEAGUE_TRANSFERS_URLS = {
    "england": "https://transfermarkt.com/premier-league/transfers/wettbewerb/GB1",
    "spain": "https://transfermarkt.com/laliga/transfers/wettbewerb/ES1",
    "germany": "https://transfermarkt.com/bundesliga/transfers/wettbewerb/L1",
    "italy": "https://transfermarkt.com/serie-a/transfers/wettbewerb/IT1",
    "france": "https://transfermarkt.com/ligue-1/transfers/wettbewerb/FR1",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

SEASONS_RANGE = range(2015, 2022)

# for get easy access to data/urls directory and by adding / you can add path
# example for accessing to player_urls.csv URLS_DIR / "player_urls.csv" -> data/urls/player_urls.csv
URLS_DIR = pathlib.Path("data/urls")