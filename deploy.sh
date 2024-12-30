#!/bin/bash

# 現在のディレクトリに存在するZIPファイルを削除
echo "Deleting existing ZIP files in the current directory..."
find . -maxdepth 1 -name "*.zip" -exec rm -v {} \;

# 新しいZIPファイル名を設定
ZIP_FILE="margiela-price-info_20241230_1.zip"

# 新しいZIPファイルを作成
echo "Creating new ZIP file: $ZIP_FILE"
zip -r $ZIP_FILE . \
    -x "env/*" \
    -x ".git/*" \
    -x ".mypy_cache/*" \
    -x "src/__pycache__/*" \
    -x "tests/__pycache__/*" \
    -x "data/.DS_Store" \
    -x "*/.ipynb_checkpoints/*"

# 関数コードの取得（オプション）
echo "Getting Lambda function code location..."
aws lambda get-function \
    --function-name margiela-price-info \
    --query 'Code.Location' \
    --output text

# Lambda 関数コードの更新
echo "Updating Lambda function code..."
aws lambda update-function-code \
    --function-name margiela-price-info \
    --zip-file fileb://$ZIP_FILE
