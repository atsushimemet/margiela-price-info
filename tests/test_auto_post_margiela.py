import os
from io import StringIO
from unittest.mock import patch

import pytest

from auto_post_margiela import get_id_list, main


@pytest.fixture
def setup_test_files(tmp_path):
    # テスト用のディレクトリとファイルを作成する
    test_dir = tmp_path / "test_brand"
    test_dir.mkdir()
    with open(test_dir / "tweet_20240101_1.txt", "w") as f:
        f.write("Test tweet 1")
    with open(test_dir / "tweet_20240101_2.txt", "w") as f:
        f.write("Test tweet 2")
    with open(test_dir / "tweet_20240101_3.txt", "w") as f:
        f.write("Test tweet 3")


def test_get_id_list(setup_test_files, tmp_path):
    # 適切なIDリストを取得できることを確認する
    id_list = get_id_list("20240101", tmp_path / "test_brand")
    assert id_list == [1, 2, 3]


# @patch("sys.stdout", new_callable=StringIO)
# def test_main(setup_test_files, mock_stdout):
#     # main関数が正常に動作し、期待どおりのログが出力されることを確認する
#     main("20240101", "test_brand")
#     expected_output = """auto load tweet:1
# auto load tweet:2
# auto load tweet:3
# Processing completed
# """
#     assert mock_stdout.getvalue() == expected_output


# @patch("sys.stdout", new_callable=StringIO)
# def test_main_file_not_found(setup_test_files, mock_stdout):
#     # ファイルが存在しない場合に、該当するログが出力されることを確認する
#     main("20240101", "non_existing_brand")
#     expected_output = (
#         "file not found:1\nfile not found:2\nfile not found:3\nProcessing completed\n"
#     )
#     assert mock_stdout.getvalue() == expected_output
