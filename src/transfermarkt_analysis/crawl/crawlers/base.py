import re
import requests
from typing import Any, Dict

import numpy as np
import pandas as pd
from mimesis import Generic, Locale

from transfermarkt_analysis.consts import DATA_DIR


__all__ = [
    "get_headers",
    "make_request",
    "obj_id",
    "get_matchday_urls_df"
]

provider: Generic = Generic(locale=Locale.EN)


def get_headers() -> Dict[str, Any]:
    headers: Dict[str, Any] = {"User-Agent": provider.internet.user_agent()}
    return headers


def make_request(url: str) -> requests.Response:
    headers: Dict[str, Any] = get_headers()
    try:
        resp: requests.Response = requests.get(
            url=url,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp
    except requests.RequestException:
        return None


def obj_id(url: str) -> str:
    pattern: str = r"\d+"
    mtch: str = re.search(pattern, url).group()
    return mtch


def get_matchday_urls_df(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    output_df: pd.DataFrame = pd.read_csv(DATA_DIR / f"matches/{filename}.csv")
    url_ids = output_df.loc[:, "url_id"].drop_duplicates()
    return df.loc[~np.isin(df.index.values, url_ids)]