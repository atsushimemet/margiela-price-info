#!/bin/zsh
# CSVファイルのパス
csv_file="data/input/arisa_brand_item_model.csv"

# カウンターを初期化
counter_file=".counter"
if [ ! -f "$counter_file" ]; then
    echo "1" > "$counter_file"
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
else
    # カウンターをインクリメント
    counter=$((counter + 1))
    echo "$counter" > "$counter_file"
fi

# CSVのデータからbrand、item、modelを取得
brand=$(echo "$csv_line" | cut -d',' -f2)
item=$(echo "$csv_line" | cut -d',' -f3)
model=$(echo "$csv_line" | cut -d',' -f4)

# item変数にmodelを追加する
item="$item $model"
echo $brand
echo $item

# 日付を取得
date=$(date +%Y%m%d)

# Pythonスクリプトを実行
python get_product_info.py "$brand" "$item"
python auto_post_margiela.py "$date" "$brand"
