import datetime
import os
from pathlib import Path
from time import sleep

import pandas as pd
import requests
import tweepy
from logzero import logfile, logger

from src.config import DAILY_FREE_TWEET_LIMIT, PATH_OUTPUT_DIR, REQ_PARAMS, TwitterAPI

# 環境変数
MAX_PAGE = int(os.environ.get("MAX_PAGE", 5))
REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
BASE_DIR = "./"
WANT_ITEMS = [
    "itemName",
    "itemPrice",
    "itemUrl",
]
TWITTER_API_URL = "https://api.twitter.com/2/tweets"
client = tweepy.Client(
    bearer_token=TwitterAPI.BearerToken,
    consumer_key=TwitterAPI.Key,
    consumer_secret=TwitterAPI.KeySecret,
    access_token=TwitterAPI.AccessToken,
    access_token_secret=TwitterAPI.AccessTokenSecret,
)


# Lambda ハンドラ
def lambda_handler(event, context):
    # ログ設定
    log_file = f"{BASE_DIR}/log.txt"
    logfile(log_file)

    # ブランドと商品情報の設定
    brand = "カルティエ"
    item = "腕時計 サントスLM"
    logger.info(f"Processing item: {brand}, {item}")

    try:
        # 商品情報の取得
        df = fetch_products(brand, item)
        if df.empty:
            logger.warning("No products found.")
            return {"status": "No products found"}

        # ツイート用テキストの保存
        save_tweet_texts(brand, df, PATH_OUTPUT_DIR)

        # 自動投稿処理
        today = datetime.datetime.today().strftime("%Y%m%d")
        auto_post_margiela(today, brand)
        logger.info("Processing completed successfully.")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"status": "error", "message": str(e)}


# 商品情報を取得する関数
def fetch_products(brand, item):
    keyword = f"{brand} {item}"
    logger.info(f"Keyword: {keyword}")
    df = pd.DataFrame(columns=WANT_ITEMS)
    for page in range(1, MAX_PAGE + 1):
        REQ_PARAMS.update({"page": page, "keyword": keyword})
        response = requests.get(REQ_URL, params=REQ_PARAMS)
        if response.status_code != 200:
            logger.error(f"Error: {response.status_code} on page {page}")
            continue
        data = response.json()
        if data["hits"] == 0:
            logger.info("No more products found.")
            break
        tmp_df = pd.DataFrame(data["Items"])[WANT_ITEMS]
        df = pd.concat([df, tmp_df], ignore_index=True)
        logger.info(f"Page {page} processed.")
        sleep(1)
    logger.info("Fetch products finished.")
    return df


# ツイート用のテキストを保存する関数
def save_tweet_texts(brand, df, output_dir):
    today = datetime.datetime.today().strftime("%Y%m%d")
    output_dir = Path(output_dir) / brand
    output_dir.mkdir(parents=True, exist_ok=True)

    with open("./data/input/tag.txt") as f:
        tag = f.read()

    for i, row in df.iterrows():
        tweet_text = f"【腕時計】アイテム名: {row['itemName']}\n価格: {row['itemPrice']}\nURL: {row['itemUrl']} {tag}"
        tweet_file_path = output_dir / f"tweet_{today}_{i}.txt"
        with open(tweet_file_path, "w") as file:
            file.write(tweet_text)
        logger.info(f"Saved: {tweet_file_path}")


# 自動投稿する関数
def auto_post_margiela(yyyymmdd, brand):
    start_idx = min(get_id_list(yyyymmdd, brand))
    end_idx = max(get_id_list(yyyymmdd, brand))
    for idx in range(start_idx, end_idx + 1):
        logger.info(f"auto load tweet:{idx}")
        try:
            with open(
                PATH_OUTPUT_DIR / brand / f"tweet_{yyyymmdd}_{idx}.txt", "r"
            ) as f:
                try:
                    client.create_tweet(text=f.read())
                    sleep(1)
                except tweepy.errors.Forbidden as e:
                    logger.info(f"{e}")
                except tweepy.errors.TooManyRequests as e:
                    logger.info(f"Rate limit exceeded: {e}")
                    break
                except tweepy.errors.BadRequest as e:
                    logger.error(
                        f"Bad request, likely too long tweet text: {e}. Text length: {len(f.read())}"
                    )
        except FileNotFoundError:
            logger.info(f"file not found:{idx}")
            continue
        if idx + 1 == DAILY_FREE_TWEET_LIMIT:
            logger.info(f"DAILY_FREE_TWEET_LIMIT:{DAILY_FREE_TWEET_LIMIT} so fin!")
            break
    logger.info("Processing completed")


def get_id_list(yyyymmdd: str, brand: str) -> list:
    return [
        int(f.split("_")[2].split(".txt")[0])
        for f in os.listdir(PATH_OUTPUT_DIR / brand)
        if f.startswith("tweet") and yyyymmdd in f
    ]


if __name__ == "__main__":
    lambda_handler(None, None)
