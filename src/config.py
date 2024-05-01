from pathlib import Path
from typing import Dict, Union

from src.local_config import CLIENT_ME, TwitterAPI  # noqa

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
MAX_PAGE = 10  # NOTE: auto_postが300ほどしかできない。
HITS_PER_PAGE = 30


REQ_PARAMS: Dict[str, Union[str, int, Dict[str, str]]] = {
    "applicationId": CLIENT_ME["APPLICATION_ID"],
    "affiliateId": CLIENT_ME["AFF_ID"],
    "format": "json",
    "formatVersion": "2",
    "keyword": "",
    "hits": HITS_PER_PAGE,
    "sort": "-itemPrice",
    "page": 0,
    "minPrice": 100,
}
WANT_ITEMS = [
    "itemName",
    "itemPrice",
    "itemUrl",
]

PATH_OUTPUT_DIR = Path("./data/output/")
DAILY_FREE_TWEET_LIMIT = 50
