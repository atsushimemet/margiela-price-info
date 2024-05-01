import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from get_product_info import (
    fetch_products,  # スクリプトの名前に応じて変更してください。
    save_tweet_texts,
)
from src.config import MAX_PAGE


# fetch_productsのテスト
@pytest.mark.parametrize(
    "status_code, expected_call_count",
    [(200, MAX_PAGE), (404, 0)],  # 正常なレスポンス  # エラーコードの場合
)
def test_fetch_products__df_len_expected(status_code, expected_call_count):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {
            "hits": 1,
            "Items": [
                {
                    "itemName": "テスト商品",
                    "itemPrice": "1000",
                    "itemUrl": "http://example.com",
                }
            ],
        }
        mock_get.return_value = mock_response
        df = fetch_products("テストブランド", "テストアイテム")
        assert len(df) == expected_call_count


@pytest.fixture
def mock_env(tmp_path):
    # 環境変数やパスを一時パスに設定する
    from src.config import path_output_dir

    original_path = path_output_dir
    path_output_dir = tmp_path  # 一時ディレクトリを設定
    yield tmp_path
    path_output_dir = original_path  # テスト後に元に戻す


def test_save_tweet_texts(mock_env):
    df = pd.DataFrame(
        {
            "itemName": ["商品A"],
            "itemPrice": ["1000"],
            "itemUrl": ["http://example.com"],
        }
    )
    brand = "テストブランド"
    today = datetime.datetime.today().strftime("%Y%m%d")
    expected_file_path = mock_env / brand / f"tweet_{today}_0.txt"
    expected_content = "アイテム名: 商品A\n価格: 1000\nURL: http://example.com PR"

    with patch("builtins.open", mock_open()) as mock_file, patch(
        "pathlib.Path.mkdir"
    ) as mock_mkdir:
        save_tweet_texts(brand, df, mock_env)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_file.assert_called_once_with(expected_file_path, "w")
        handle = mock_file()
        handle.write.assert_called_once_with(expected_content)
