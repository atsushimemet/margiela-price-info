from unittest.mock import MagicMock, patch

import pytest

from auto_post_margiela import get_id_list, logger, main


@pytest.fixture
def setup_test_files(tmp_path):
    # テスト用のディレクトリとファイルを作成する
    test_dir = tmp_path / "test_brand"
    test_dir.mkdir()
    for i in range(1, 4):
        with open(test_dir / f"tweet_20240101_{i}.txt", "w") as f:
            f.write(f"Test tweet {i}")
    return test_dir


def test_get_id_list(setup_test_files, tmp_path):
    # 適切なIDリストを取得できることを確認する
    id_list = get_id_list("20240101", tmp_path / "test_brand")
    assert id_list == [1, 2, 3]


def test_main(setup_test_files, monkeypatch):
    # PATH_OUTPUT_DIRをモックして、setup_test_filesのパスを指定
    monkeypatch.setattr("auto_post_margiela.PATH_OUTPUT_DIR", setup_test_files.parent)

    # tweepy.Clientのモック
    mock_tweepy_client = MagicMock()
    monkeypatch.setattr("auto_post_margiela.client", mock_tweepy_client)

    # loggerのモック
    with patch.object(logger, "info") as mock_logger_info, patch.object(
        logger, "error"
    ) as mock_logger_error:
        main("20240101", "test_brand")
        # ログの呼び出しを検証
        mock_logger_info.assert_any_call("auto load tweet:1")
        mock_logger_info.assert_any_call("auto load tweet:2")
        mock_logger_info.assert_any_call("auto load tweet:3")
        mock_logger_info.assert_any_call("Processing completed")

        # エラーログが呼ばれていないことを確認
        mock_logger_error.assert_not_called()
