#!/usr/bin/env python
# coding: utf-8
import argparse
import os
from time import sleep

import tweepy
from logzero import logger

from src.config import DAILY_FREE_TWEET_LIMIT, PATH_OUTPUT_DIR, TwitterAPI

client = tweepy.Client(
    bearer_token=TwitterAPI.BearerToken,
    consumer_key=TwitterAPI.Key,
    consumer_secret=TwitterAPI.KeySecret,
    access_token=TwitterAPI.AccessToken,
    access_token_secret=TwitterAPI.AccessTokenSecret,
)


def get_id_list(yyyymmdd: str, brand: str) -> list:
    return [
        int(f.split("_")[2].split(".txt")[0])
        for f in os.listdir(PATH_OUTPUT_DIR / brand)
        if f.startswith("tweet") and yyyymmdd in f
    ]


def main(yyyymmdd: str, brand: str):
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


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("yyyymmdd", type=str)
    parser.add_argument("brand", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    main(args.yyyymmdd, args.brand)
