import pathlib

HEADERS = {
    "User-Agent": "	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# for get easy access to data/urls directory and by adding / you can add path
# example for accessing to player_urls.csv URLS_DIR / "player_urls.csv" -> src/.../data/urls/player_urls.csv
URLS_DIR = pathlib.Path(__file__).resolve().parent / "data/urls"
