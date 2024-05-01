from unittest.mock import MagicMock, patch

import pytest

from get_product_info import (
    fetch_products,
)  # スクリプトの名前に応じて変更してください。
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
