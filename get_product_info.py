import argparse
import datetime
from pathlib import Path
from time import sleep

import pandas as pd
import requests
from logzero import logger

from src.config import MAX_PAGE, PATH_OUTPUT_DIR, REQ_PARAMS, REQ_URL, WANT_ITEMS


def fetch_products(brand, item):
    # keyword = f"{brand} {item} 中古"
    keyword = f"{brand} {item}"  # TODO:05/17 イブサンローランボーテ リップ
    logger.info(f"keyword:{keyword}")
    df = pd.DataFrame(columns=WANT_ITEMS)
    for page in range(1, MAX_PAGE + 1):
        REQ_PARAMS.update({"page": page, "keyword": keyword})
        response = requests.get(REQ_URL, REQ_PARAMS)
        if response.status_code != 200:
            logger.error(f"ErrorCode -> {response.status_code}\nPage -> {page}")
            continue
        data = response.json()
        if data["hits"] == 0:
            logger.info("No more products found.")
            break
        tmp_df = pd.DataFrame(data["Items"])[WANT_ITEMS]
        df = pd.concat([df, tmp_df], ignore_index=True)
        logger.info(f"Page {page} processed.")
        sleep(1)  # Avoid hitting API rate limit
    logger.info("fetch products Finished!!")
    return df


def save_tweet_texts(brand, df, output_dir):
    today = datetime.datetime.today().strftime("%Y%m%d")
    output_dir = Path(output_dir) / brand
    output_dir.mkdir(parents=True, exist_ok=True)

    with open("./data/input/tag.txt") as f:
        tag = f.read()

    for i, row in df.iterrows():
        tweet_text = f"【旅行の相棒】アイテム名: {row['itemName']}\n価格: {row['itemPrice']}\nURL: {row['itemUrl']} {tag}"
        tweet_file_path = output_dir / f"tweet_{today}_{i}.txt"
        with open(tweet_file_path, "w") as file:
            file.write(tweet_text)
        logger.info(f"Saved: {tweet_file_path}")


def main(brand: str, item: str):
    df = fetch_products(brand, item)
    save_tweet_texts(brand, df, PATH_OUTPUT_DIR)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("brand", type=str)
    parser.add_argument("item", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    main(args.brand, args.item)
