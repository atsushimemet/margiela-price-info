from src.local_config import CLIENT_ME, TwitterAPI  # noqa
from pathlib import Path

REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
MAX_PAGE = 1
HITS_PER_PAGE = 30


req_params = {
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

path_output_dir = Path("./data/output/")
