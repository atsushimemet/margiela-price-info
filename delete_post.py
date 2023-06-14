#!/usr/bin/env python
# coding: utf-8

import tweepy

from src.config import TwitterAPI

consumer_key = TwitterAPI.Key
consumer_secret = TwitterAPI.KeySecret
access_token = TwitterAPI.AccessToken
access_token_secret = TwitterAPI.AccessTokenSecret

# 認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main():
    for timeline in api.user_timeline():
        print(timeline._json["id"])
        api.destroy_status(timeline._json["id"])


if __name__ == "__main__":
    main()
