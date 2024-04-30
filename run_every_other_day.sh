#!/bin/zsh
# run_every_other_day.sh
start_date="2024-05-01"
current_date=$(date +%Y-%m-%d)

# 日付を YYYY-MM-DD 形式で扱い、日数の差を計算 (macOS用)
start_seconds=$(date -j -f "%Y-%m-%d" "$start_date" +%s)
current_seconds=$(date -j -f "%Y-%m-%d" "$current_date" +%s)
days_difference=$(( ($current_seconds - $start_seconds) / 86400 ))

# 経過日数が偶数の場合にスクリプトを実行
if [ $((days_difference % 2)) -eq 0 ]; then
    echo "Script is running on : current_date:$current_date, days_difference:$days_difference"
    # /bin/zsh /path/to/your/script/run.sh
else
    echo "Script is not running on : current_date:$current_date, days_difference:$days_difference"
fi
