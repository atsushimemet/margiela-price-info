# プロジェクト概要
このプロジェクトは、指定されたブランドと商品に関する情報を収集し、自動でツイートを投稿する機能を提供します。

# ディレクトリ構造

```
.
├── README.md                       # このファイル
├── auto_post_margiela.py           # 自動ツイート投稿スクリプト
├── data                            # データ格納用ディレクトリ
│   ├── input                       # 入力データ（除外単語リストなど）
│   │   └── del_word_list.txt
│   └── output                      # 出力データ（収集した商品情報など）
│       ├── margiela
│       ├── supreme
│       └── vuitton
├── get_product_info.py             # 商品情報収集スクリプト
├── mypy.ini                        # mypy設定ファイル
├── notebook                        # Jupyter Notebookファイル
│   ├── create_insta_feed.ipynb     # Instagramフィード作成ノートブック
│   └── system_operation_check.ipynb# システム動作状態チェックノートブック
├── requirements.txt                # 依存ライブラリ
├── run.sh                          # スクリプト実行シェルスクリプト
├── setup.sh                        # 環境セットアップシェルスクリプト
├── src                             # ソースコード
│   ├── config.py                   # 設定ファイル
│   └── local_config.py             # ローカル設定ファイル（Git非追跡）
└── tmp                             # 一時ファイル
    ├── create_insta_feed.py
    └── delete_post.py
```
# セットアップ方法
プロジェクトのセットアップには、以下の手順が含まれます。
## 1. Pythonのバージョンを3.10.5に設定
このプロジェクトはPython 3.10.5で動作するよう設計されています。適切なPythonバージョンを使用していることを確認してください。pyenvなどのバージョン管理ツールを使用してPythonのバージョンを管理している場合は、以下のコマンドでバージョンを設定できます。
```
pyenv install 3.10.5
pyenv local 3.10.5
```
## 2. 仮想環境の作成
プロジェクト専用の仮想環境を作成することで、依存関係をプロジェクト内に閉じ込め、他のプロジェクトやシステム全体のPython環境との衝突を避けることができます。以下のコマンドを実行して仮想環境を作成します。
python -m venv env
作成した仮想環境をアクティベートします。
```
source env/bin/activate
```
## 3. 依存ライブラリのインストール
次に、./setup.shを実行して、必要な依存ライブラリをインストールします
## 4. 設定変更
- src/config.pyファイルを編集して、プロジェクトの設定をカスタマイズします。特に、Twitter APIの認証情報を設定する必要があります。
- run.sh内のbrand/itemの更新
## 5. ローカル設定反映
local_config.pyをsrcディレクトリに作成して、ローカル環境専用の設定を追加します（このファイルはGitで追跡されません）。
# 実行方法
## 商品情報の収集と自動ツイート投稿
run.shスクリプトを使用して、商品情報の収集と自動ツイート投稿を行います。例えば、以下のコマンドはvuittonブランドの財布に関する商品情報を収集し、自動的にツイートします。
```
./run.sh
```
# 注意事項
Twitterの自動投稿は、無料枠では1日あたり50回までとなっています。これを超えると投稿が制限されます。
# REF
- https://exactsolutions.co.jp/column/rpa/python-rakutenapi-minitem/
- https://webservice.rakuten.co.jp/documentation/ichiba-product-search
