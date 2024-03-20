#!/usr/bin/env python
# coding: utf-8
import argparse
import os
from time import sleep

import tweepy
from logzero import logger

from src.config import TwitterAPI, path_output_dir

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
        for f in os.listdir(path_output_dir / brand)
        if f.startswith("tweet") and yyyymmdd in f
    ]


def main(yyyymmdd: str, brand: str):
    start_idx = min(get_id_list(yyyymmdd, brand))
    end_idx = max(get_id_list(yyyymmdd, brand))
    for idx in range(start_idx, end_idx + 1):
        logger.info(f"auto load tweet:{idx}")
        try:
            with open(
                path_output_dir / brand / f"tweet_{yyyymmdd}_{idx}.txt", "r"
            ) as f:
                try:
                    client.create_tweet(text=f.read())
                    sleep(1)
                except tweepy.errors.Forbidden as e:
                    logger.info(f"{e}")
        except FileNotFoundError:
            logger.info(f"file not found:{idx}")
            continue


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("yyyymmdd", type=str)
    parser.add_argument("brand", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    main(args.yyyymmdd, args.brand)
