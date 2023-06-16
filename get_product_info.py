import json
from time import sleep
import os
import pandas as pd
import requests
from src.config import req_params, WANT_ITEMS, REQ_URL, MAX_PAGE, path_output_dir
import datetime
import argparse
from logzero import logger


def main(brand: str):
    cnt = 1
    keyword = f"{brand} 財布 バッグ 中古"

    req_params["page"] = cnt
    req_params["keyword"] = keyword
    df = pd.DataFrame(columns=WANT_ITEMS)

    # ページループ
    logger.info("loop start!")
    while True:
        req_params["page"] = cnt
        res = requests.get(REQ_URL, req_params)
        res_code = res.status_code
        res = json.loads(res.text)
        if res_code != 200:
            print(
                f"""
            ErrorCode -> {res_code}\n
            Error -> {res['error']}\n
            Page -> {cnt}"""
            )
        else:
            if res["hits"] == 0:
                print("返ってきた商品数の数が0なので、ループ終了")
                break
            tmp_df = pd.DataFrame(res["Items"])[WANT_ITEMS]
            df = pd.concat([df, tmp_df], ignore_index=True)
        if cnt == MAX_PAGE:
            print("MAX PAGEに到達したので、ループ終了")
            break
        logger.info(f"{cnt} end!")
        cnt += 1
        # リクエスト制限回避
        sleep(1)

    print("Finished!!")

    today = datetime.datetime.today().strftime("%Y%m%d")

    # データフレームからリストを作成するための空のリスト
    result_list = []

    # データフレームの各行をループで処理
    for index, row in df.iterrows():
        item_name = row["itemName"]
        price = row["itemPrice"]
        url = row["itemUrl"]
        result_list.append([item_name, price, url])

    # 結果のリストを表示
    for i, data in enumerate(result_list):
        tweet_text = f"アイテム名: {data[0]}\n価格: {data[1]}\nURL: {data[2]}"
        # 本日日付フォルダ作成
        if not os.path.isdir(path_output_dir / brand):
            os.mkdir(path_output_dir / brand)
        # テキストファイルに書き込む
        with open(path_output_dir / brand / f"tweet_{today}_{i}.txt", "w") as file:
            file.write(tweet_text)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("brand", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    main(args.brand)
