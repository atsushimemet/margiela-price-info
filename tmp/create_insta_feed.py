#!/usr/bin/env python
# coding: utf-8
import os
from pathlib import Path
import argparse
from logzero import logger


def main(yyyymmdd: str, brand: str):
    file_list = [f for f in os.listdir(f"./data/output/{brand}") if yyyymmdd in f]
    price_list = []
    for file in file_list:
        with open(Path(f"data/output/{brand}") / file, "r") as f:
            price_list.append(int(f.read().split("価格: ")[1].split("\n")[0]))
    logger.info(f"平均値: {round(sum(price_list) / len(price_list))}")
    logger.info(f"最安値: {min(price_list)}")
    logger.info(f"最高値: {max(price_list)}")


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("yyyymmdd", type=str)
    parser.add_argument("brand", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    main(args.yyyymmdd, args.brand)
