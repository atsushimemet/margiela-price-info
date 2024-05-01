#!/bin/zsh
# run.sh

# Base directory
BASE_DIR="/Users/ozawaatsushi/Repository/NewBusiness/margiela-price-info"

log_file="$BASE_DIR/log.txt"
csv_file="$BASE_DIR/data/input/arisa_brand_item_model.csv"
counter_file="$BASE_DIR/.counter"

# カウンターを初期化
if [ ! -f "$counter_file" ]; then
    echo "1" > "$counter_file"
    echo "$(date): Counter initialized to 1." >> $log_file
fi

# カウンターを読み込む
counter=$(cat "$counter_file")

# CSVファイルを読み込んで指定された行のデータを取得する関数
get_csv_line() {
    local line_no=$1
    sed -n "${line_no}p" "$csv_file"
}

# カウンターの行のデータを取得
csv_line=$(get_csv_line "$counter")
if [ -z "$csv_line" ]; then
    # カウンターがCSVの行数を超えていた場合は最初の行に戻す
    csv_line=$(get_csv_line "1")
    echo "1" > "$counter_file"
    echo "$(date): Counter exceeded line count, reset to 1." >> $log_file
else
    # カウンターをインクリメント
    counter=$((counter + 1))
    echo "$counter" > "$counter_file"
fi

# CSVのデータからbrand、item、modelを取得
brand=$(echo "$csv_line" | cut -d',' -f2)
item=$(echo "$csv_line" | cut -d',' -f3)
model=$(echo "$csv_line" | cut -d',' -f4)
item="$item $model"
echo "$(date): Processing item: $brand, $item" >> $log_file

# 日付を取得
date=$(date +%Y%m%d)

# Pythonスクリプトを実行
PYTHON="/Users/ozawaatsushi/.pyenv/versions/3.10.5/bin/python"
$PYTHON $BASE_DIR/get_product_info.py "$brand" "$item"
$PYTHON $BASE_DIR/auto_post_margiela.py "$date" "$brand"
