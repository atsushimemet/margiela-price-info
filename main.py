import datetime
import os
import shutil
from pathlib import Path
from time import sleep

import pandas as pd
import requests
import tweepy
from logzero import logfile, logger

from src.config import (
    BASE_DIR,
    DAILY_FREE_TWEET_LIMIT,
    MAX_PAGE,
    PATH_OUTPUT_DIR,
    REQ_PARAMS,
    REQ_URL,
    WANT_ITEMS,
    client,
    s3_client,
)


# Lambda ハンドラ
def lambda_handler(event, context):
    # ログ設定
    log_file = f"{BASE_DIR}/log.txt"
    logfile(log_file)

    # CSVからブランドと商品情報を取得
    csv_path = f"./data/input/brand_item_model.csv"
    brand_item_df = load_brand_item_model(csv_path)

    # 前回実行したアイテムIDを取得
    last_executed_id = get_last_executed_item_id()

    # 次に実行するアイテムを選択
    next_item_data = brand_item_df[brand_item_df["ID"] == last_executed_id + 1]
    if next_item_data.empty:
        return {"status": "error", "message": "No more items to process"}

    # ブランド、商品情報を設定
    brand = next_item_data["Brand"].values[0]
    item = f"{next_item_data['Item'].values[0]}"
    model = f"{next_item_data['Model'].values[0]}"
    tags = f"#PR #{brand} #{item} #{model}"
    if "腕時計" in item:
        tweet_title = "高級腕時計"
    else:
        tweet_title = "ハイブラ"

    item = " ".join([item, model])

    logger.info(f"Processing item: {brand}, {item}")
    try:
        # 商品情報の取得
        df = fetch_products(brand, item)
        if df.empty:
            logger.warning("No products found.")
            return {"status": "No products found"}

        # ツイート用テキストの保存
        save_tweet_texts(brand, df, PATH_OUTPUT_DIR, tweet_title, tags)

        # 自動投稿処理
        today = datetime.datetime.today().strftime("%Y%m%d")
        auto_post_margiela(today, brand)
        logger.info("Processing completed successfully.")
        # 実行後、IDを1増やして保存
        save_last_executed_item_id(last_executed_id + 1)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"status": "error", "message": str(e)}


# CSVの読み込み処理
def load_brand_item_model(csv_path):
    # CSVファイルをDataFrameとして読み込み
    df = pd.read_csv(csv_path, header=None, names=["ID", "Brand", "Item", "Model"])
    return df


# 前回実行したアイテムIDを取得する関数
def get_last_executed_item_id():
    last_executed_file_key = "last_executed_item.txt"
    bucket_name = "margiela-price-info"
    try:
        # S3からファイルを取得
        response = s3_client.get_object(Bucket=bucket_name, Key=last_executed_file_key)
        last_id = int(response["Body"].read().decode("utf-8").strip())
        return last_id
    except s3_client.exceptions.NoSuchKey:
        # ファイルが存在しない場合はID=0を返す
        return 0
    except Exception as e:
        logger.error(f"Error fetching last executed item ID from S3: {e}")
        raise


# 前回実行したアイテムIDを記録する関数
def save_last_executed_item_id(item_id):
    last_executed_file_key = "last_executed_item.txt"
    bucket_name = "margiela-price-info"
    try:
        # ファイルをS3にアップロード
        s3_client.put_object(
            Bucket=bucket_name, Key=last_executed_file_key, Body=str(item_id)
        )
        logger.info(f"Successfully saved last executed item ID: {item_id}")
    except Exception as e:
        logger.error(f"Error saving last executed item ID to S3: {e}")
        raise


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
def save_tweet_texts(brand, df, output_dir, tweet_title, tags):
    today = datetime.datetime.today().strftime("%Y%m%d")
    output_dir = Path(output_dir) / brand
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, row in df.iterrows():
        # タグを生成
        tweet_text = f"【{tweet_title}】アイテム名: {row['itemName']}\n価格: {row['itemPrice']}\nURL: {row['itemUrl']}\n{tags}"
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
            tweet_file_path_brand = PATH_OUTPUT_DIR / brand
            tweet_file_path = tweet_file_path_brand / f"tweet_{yyyymmdd}_{idx}.txt"
            with open(tweet_file_path, "r") as f:
                tweet_text = f.read()
                try:
                    # ツイートの投稿
                    client.create_tweet(text=tweet_text)
                    logger.info(f"Tweet posted: {tweet_text}")
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
    # 投稿処理完了後、テキストファイルを含むbrandディレクトリ削除
    shutil.rmtree(tweet_file_path_brand)
    logger.info(f"Deleted tweet path brand: {tweet_file_path_brand}")


def get_id_list(yyyymmdd: str, brand: str) -> list:
    return [
        int(f.split("_")[2].split(".txt")[0])
        for f in os.listdir(PATH_OUTPUT_DIR / brand)
        if f.startswith("tweet") and yyyymmdd in f
    ]


if __name__ == "__main__":
    lambda_handler(None, None)
