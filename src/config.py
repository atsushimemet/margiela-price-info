from pathlib import Path
from typing import Dict, Union

import tweepy

from src.local_config import CLIENT_ME, TwitterAPI  # noqa

# 楽天
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

# Twitter
DAILY_FREE_TWEET_LIMIT = 50
client = tweepy.Client(
    bearer_token=TwitterAPI.BearerToken,
    consumer_key=TwitterAPI.Key,
    consumer_secret=TwitterAPI.KeySecret,
    access_token=TwitterAPI.AccessToken,
    access_token_secret=TwitterAPI.AccessTokenSecret,
)

# その他
BASE_DIR = "./"
PATH_OUTPUT_DIR = Path("./data/output/")
