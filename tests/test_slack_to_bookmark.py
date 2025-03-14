#!/usr/bin/env python3
"""
Slack to Bookmarkのテストモジュール

このモジュールはSlack to Bookmarkの機能をテストするためのテストケースを提供します。
テストはPytestフレームワークを使用して実装されています。
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# 親ディレクトリをパスに追加してインポートできるようにする
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.slack_to_bookmark import SlackClient, BookmarkGenerator, GuideGenerator, SlackToBookmark


class TestSlackClient:
    """SlackClientクラスのテスト"""
    
    @patch('src.slack_to_bookmark.WebClient')
    def test_init_with_valid_token(self, mock_webclient):
        """有効なトークンで初期化できることをテスト"""
        # テストデータ
        token = "xoxp-valid-token"
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        
        # テスト実行
        client = SlackClient(token, workspace_name, workspace_id)
        
        # 検証
        assert client.workspace_name == workspace_name
        assert client.workspace_id == workspace_id
        mock_webclient.assert_called_once_with(token=token)
    
    def test_init_with_empty_token(self):
        """空トークンでの初期化でValueErrorが発生することをテスト"""
        # テストデータ
        token = ""
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        
        # テスト実行と検証
        with pytest.raises(ValueError, match="Slack APIトークンが指定されていません"):
            SlackClient(token, workspace_name, workspace_id)
    
    @patch('src.slack_to_bookmark.WebClient')
    def test_get_channels_by_type_invalid_type(self, mock_webclient):
        """無効なチャンネルタイプでValueErrorが発生することをテスト"""
        # テストデータ
        token = "xoxp-valid-token"
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        invalid_type = "invalid_channel_type"
        
        # セットアップ
        client = SlackClient(token, workspace_name, workspace_id)
        
        # テスト実行と検証
        with pytest.raises(ValueError, match="チャンネルタイプは 'public_channel' または 'private_channel' である必要があります"):
            client.get_channels_by_type(invalid_type)
    
    @patch('src.slack_to_bookmark.WebClient')
    def test_get_public_channels(self, mock_webclient):
        """公開チャンネル取得メソッドが正しく呼び出されることをテスト"""
        # テストデータ
        token = "xoxp-valid-token"
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        
        # モックの設定
        mock_client = MagicMock()
        mock_webclient.return_value = mock_client
        
        # レスポンスデータの設定
        mock_channels = [{"id": "C123", "name": "general", "is_private": False}]
        mock_client.conversations_list.return_value = {"channels": mock_channels, "response_metadata": {}}
        
        # テスト実行
        client = SlackClient(token, workspace_name, workspace_id)
        with patch.object(client, 'get_channels_by_type') as mock_get_channels:
            mock_get_channels.return_value = mock_channels
            channels = client.get_public_channels()
        
        # 検証
        mock_get_channels.assert_called_once_with("public_channel")
        assert channels == mock_channels


class TestBookmarkGenerator:
    """BookmarkGeneratorクラスのテスト"""
    
    def test_init(self):
        """BookmarkGeneratorが正しく初期化されることをテスト"""
        # テストデータ
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        
        # テスト実行
        generator = BookmarkGenerator(workspace_name, workspace_id)
        
        # 検証
        assert generator.workspace_name == workspace_name
        assert generator.workspace_id == workspace_id
        assert generator.timestamp is not None
    
    @patch('builtins.open', new_callable=MagicMock)
    def test_generate_channel_bookmarks(self, mock_open):
        """チャンネルブックマーク生成が正しく動作することをテスト"""
        # テストデータ
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        channels = [
            {"id": "C123", "name": "general", "is_private": False},
            {"id": "C456", "name": "random", "is_private": False},
            {"id": "C789", "name": "private-channel", "is_private": True}
        ]
        output_file = "test_bookmarks.html"
        
        # テストファイルハンドラの設定
        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle
        
        # テスト実行
        generator = BookmarkGenerator(workspace_name, workspace_id)
        result = generator.generate_channel_bookmarks(channels, output_file)
        
        # 検証
        mock_open.assert_called_once_with(output_file, "w", encoding="utf-8")
        assert mock_file_handle.write.call_count == 1
        assert "#general" in str(mock_file_handle.write.call_args[0][0])
        assert "#random" in str(mock_file_handle.write.call_args[0][0])
        assert "🔒 #private-channel" in str(mock_file_handle.write.call_args[0][0])
        assert result == output_file


class TestGuideGenerator:
    """GuideGeneratorクラスのテスト"""
    
    def test_init(self):
        """GuideGeneratorが正しく初期化されることをテスト"""
        # テスト実行
        generator = GuideGenerator()
        
        # 検証
        assert hasattr(generator, 'is_mac')
        assert hasattr(generator, 'is_windows')
    
    @patch('builtins.open', new_callable=MagicMock)
    def test_create_guide(self, mock_open):
        """ガイドページ生成が正しく動作することをテスト"""
        # テストデータ
        html_file_path = "test_bookmarks.html"
        output_file = "test_guide.html"
        
        # テストファイルハンドラの設定
        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle
        
        # テスト実行
        generator = GuideGenerator()
        result = generator.create_guide(html_file_path, output_file)
        
        # 検証
        mock_open.assert_called_once_with(output_file, "w", encoding="utf-8")
        assert mock_file_handle.write.call_count == 1
        assert html_file_path in str(mock_file_handle.write.call_args[0][0])
        assert result == output_file


class TestSlackToBookmark:
    """SlackToBookmarkクラスのテスト"""
    
    @patch('src.slack_to_bookmark.load_dotenv')
    @patch('os.getenv')
    @patch('src.slack_to_bookmark.SlackClient')
    @patch('src.slack_to_bookmark.BookmarkGenerator')
    @patch('src.slack_to_bookmark.GuideGenerator')
    def test_init_with_token(self, mock_guide_gen, mock_bookmark_gen, mock_slack_client, 
                            mock_getenv, mock_load_dotenv):
        """環境変数があるときに正しく初期化されることをテスト"""
        # テストデータ
        token = "xoxp-valid-token"
        workspace_name = "test-workspace"
        workspace_id = "T12345678"
        
        # モックの設定
        mock_getenv.side_effect = lambda key, default=None: {
            "SLACK_TOKEN": token,
            "WORKSPACE_NAME": workspace_name,
            "WORKSPACE_ID": workspace_id
        }.get(key, default)
        
        # テスト実行
        app = SlackToBookmark()
        
        # 検証
        mock_load_dotenv.assert_called_once()
        assert app.token == token
        assert app.workspace_name == workspace_name
        assert app.workspace_id == workspace_id
        mock_slack_client.assert_called_once_with(token, workspace_name, workspace_id)
        mock_bookmark_gen.assert_called_once_with(workspace_name, workspace_id)
        mock_guide_gen.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
