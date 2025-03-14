# テスト方法ガイド

このガイドでは、Clineを使用してslack-to-bookmarkプロジェクトをテストする方法について説明します。

## 目次

1. [テストの種類](#テストの種類)
2. [単体テストの作成](#単体テストの作成)
3. [統合テストの作成](#統合テストの作成)
4. [モックの使用](#モックの使用)
5. [手動テスト手順](#手動テスト手順)
6. [一般的なエラーと解決策](#一般的なエラーと解決策)

## テストの種類

slack-to-bookmarkプロジェクトでは、以下の種類のテストが有効です：

1. **単体テスト**: 個別の関数やメソッドが正しく動作することを確認
2. **統合テスト**: Slack APIとの連携や、複数のコンポーネントが連携して動作することを確認
3. **手動テスト**: 実際にアプリケーションを実行して、生成されたブックマークファイルの内容や挙動を確認

## 単体テストの作成

Clineを使用して単体テストを効率的に作成できます。Pythonの標準ライブラリである`unittest`またはサードパーティライブラリの`pytest`を使用します。

### テスト用ディレクトリの作成

```bash
mkdir tests
touch tests/__init__.py
```

### テストファイルの作成

Clineに指示して、テストファイルを作成しましょう。例えば：

```python
# tests/test_bookmark_generation.py
import unittest
import datetime
from unittest.mock import patch, MagicMock
import os
import tempfile
from slack_to_bookmark import generate_bookmarks_file

class TestBookmarkGeneration(unittest.TestCase):
    def setUp(self):
        # テスト用のダミーチャンネルデータを作成
        self.channels = [
            {"name": "general", "id": "C12345", "is_private": False},
            {"name": "random", "id": "C67890", "is_private": False},
            {"name": "private-channel", "id": "C54321", "is_private": True}
        ]
        self.workspace_name = "test-workspace"
        self.workspace_id = "T12345"
        
        # 一時ファイルを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_file = os.path.join(self.temp_dir.name, "test_bookmarks.html")
    
    def tearDown(self):
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()
    
    def test_bookmarks_file_generation(self):
        # ブックマークファイルを生成
        result_file = generate_bookmarks_file(
            self.channels, 
            self.workspace_name, 
            self.workspace_id, 
            self.output_file
        )
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(result_file))
        
        # ファイルの内容を確認
        with open(result_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 基本的なHTMLタグが含まれているか確認
            self.assertIn('<!DOCTYPE NETSCAPE-Bookmark-file-1>', content)
            self.assertIn('<TITLE>Bookmarks</TITLE>', content)
            
            # チャンネル情報が含まれているか確認
            self.assertIn('slack://channel?team=T12345&id=C12345', content)
            self.assertIn('#general', content)
            self.assertIn('slack://channel?team=T12345&id=C67890', content)
            self.assertIn('#random', content)
            
            # プライベートチャンネルには 🔒 マークが付いているか確認
            self.assertIn('🔒 #private-channel', content)
            self.assertIn('slack://channel?team=T12345&id=C54321', content)

# メイン実行部
if __name__ == '__main__':
    unittest.main()
```

### テストの実行

テストを実行するには、以下のコマンドを使用します：

```bash
python -m unittest discover tests
```

または、pytestを使用する場合：

```bash
pytest tests/
```

## 統合テストの作成

Slack APIと連携する部分の統合テストも重要です。ただし、実際のAPIを呼び出すとレート制限に達する可能性があるため、モックを使用することをお勧めします。

```python
# tests/test_slack_api.py
import unittest
from unittest.mock import patch, MagicMock
from slack_to_bookmark import get_all_channels, get_all_users

class TestSlackAPI(unittest.TestCase):
    def setUp(self):
        # テスト用のモックデータ
        self.mock_channels_response = {
            "channels": [
                {"id": "C12345", "name": "general", "is_private": False},
                {"id": "C67890", "name": "random", "is_private": False}
            ],
            "response_metadata": {"next_cursor": ""}
        }
        
        self.mock_users_response = {
            "members": [
                {
                    "id": "U12345",
                    "profile": {"real_name": "Test User 1", "display_name": "testuser1"},
                    "is_bot": False,
                    "deleted": False
                },
                {
                    "id": "U67890",
                    "profile": {"real_name": "Test User 2", "display_name": "testuser2"},
                    "is_bot": False,
                    "deleted": False
                }
            ],
            "response_metadata": {"next_cursor": ""}
        }
    
    @patch('slack_sdk.WebClient')
    def test_get_all_channels(self, mock_client):
        # WebClientのモックを設定
        instance = mock_client.return_value
        instance.conversations_list.return_value = self.mock_channels_response
        
        # 関数を実行
        channels = get_all_channels(instance)
        
        # 結果を検証
        self.assertEqual(len(channels), 2)
        self.assertEqual(channels[0]["name"], "general")
        self.assertEqual(channels[1]["name"], "random")
        
        # conversations_listが正しいパラメータで呼ばれたか確認
        instance.conversations_list.assert_called_with(
            types="public_channel",
            limit=1000,
            cursor=None
        )
    
    @patch('slack_sdk.WebClient')
    def test_get_all_users(self, mock_client):
        # WebClientのモックを設定
        instance = mock_client.return_value
        instance.users_list.return_value = self.mock_users_response
        
        # 関数を実行
        users = get_all_users(instance)
        
        # 結果を検証
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]["profile"]["real_name"], "Test User 1")
        self.assertEqual(users[1]["profile"]["real_name"], "Test User 2")
        
        # users_listが正しいパラメータで呼ばれたか確認
        instance.users_list.assert_called_with(
            limit=1000,
            cursor=None
        )

if __name__ == '__main__':
    unittest.main()
```

## モックの使用

Clineを使用すると、効率的なモックの作成と使用が可能です。APIリクエストやI/O操作などの外部依存を持つコードをテストする際に特に役立ちます。

### モックデータの作成例

```python
# SlackのAPIレスポンスをモックするデータ
mock_conversations_list_response = {
    "ok": True,
    "channels": [
        {
            "id": "C012AB3CD",
            "name": "general",
            "is_channel": True,
            "is_group": False,
            "is_im": False,
            "created": 1449252889,
            "creator": "U012A3CDE",
            "is_archived": False,
            "is_general": True,
            "unlinked": 0,
            "name_normalized": "general",
            "is_shared": False,
            "is_private": False,
            "is_member": True,
            "topic": {
                "value": "Company-wide announcements and work-based matters",
                "creator": "",
                "last_set": 0
            },
            "purpose": {
                "value": "This channel is for team-wide communication and announcements. All team members are in this channel.",
                "creator": "",
                "last_set": 0
            },
            "previous_names": [],
            "num_members": 4
        },
        {
            "id": "C061EG9T2",
            "name": "random",
            "is_channel": True,
            "is_group": False,
            "is_im": False,
            "created": 1449252889,
            "creator": "U061F7AUR",
            "is_archived": False,
            "is_general": False,
            "unlinked": 0,
            "name_normalized": "random",
            "is_shared": False,
            "is_private": False,
            "is_member": True,
            "topic": {
                "value": "Non-work banter and water cooler conversation",
                "creator": "",
                "last_set": 0
            },
            "purpose": {
                "value": "A place for non-work-related flimflam, faffing, hodge-podge or jibber-jabber you'd prefer to keep out of more focused work-related channels.",
                "creator": "",
                "last_set": 0
            },
            "previous_names": [],
            "num_members": 4
        }
    ],
    "response_metadata": {
        "next_cursor": ""
    }
}
```

## 手動テスト手順

Clineを用いた開発後も、手動テストは重要です。以下の手順でアプリケーションの動作を確認します。

### 基本機能のテスト

1. **.envファイルの準備**:
   - `.env.sample`をコピーして`.env`ファイルを作成
   - 有効なSlack APIトークン、ワークスペース名、ワークスペースIDを設定

2. **アプリケーションの実行**:
   ```bash
   python slack_to_bookmark.py
   ```

3. **生成ファイルの確認**:
   - `slack_bookmarks.html` (全チャンネル)
   - `slack_public_bookmarks.html` (公開チャンネルのみ)
   - `slack_user_dms.html` (ユーザーDM)
   - 各種ガイドHTMLファイル

4. **ブックマークのインポートテスト**:
   - Chromeでブックマークマネージャーを開く (Cmd+Option+B または Ctrl+Shift+O)
   - 生成されたHTMLファイルをインポート
   - インポートされたブックマークが期待通りに表示されているか確認

5. **ブックマークの動作確認**:
   - いくつかのブックマークをクリックし、正しいSlackチャンネルまたはDMが開くか確認

### エッジケースのテスト

1. **大量のチャンネルやユーザーがある場合**:
   - 多数のチャンネルやユーザーが存在する大規模ワークスペースでテスト
   - パフォーマンスやメモリ使用量を監視

2. **特殊文字を含むチャンネル名やユーザー名**:
   - 日本語、絵文字、特殊記号などを含むチャンネル名やユーザー名の処理が正しいか確認

3. **権限エラーの処理**:
   - 不十分な権限を持つAPIトークンを使用した場合のエラーメッセージが適切か確認

## 一般的なエラーと解決策

### 1. APIトークン関連の問題

**エラー**: `slack_sdk.errors.SlackApiError: The request to the Slack API failed.`

**解決策**:
- APIトークンが正しく設定されているか確認
- トークンに必要なスコープ（権限）が付与されているか確認
- トークンが有効であるか確認（無効になっていないか）

### 2. ブックマークファイル生成の問題

**エラー**: ブックマークファイルが生成されない、または内容が不正

**解決策**:
- API応答から正しくデータが取得できているか確認（デバッグプリントを追加）
- ファイル書き込み権限があるか確認
- HTMLの構文が正しいか確認

### 3. ブラウザでの表示問題

**エラー**: ブックマークがChromeに正しくインポートされない

**解決策**:
- 生成されたHTMLファイルの構文が標準的なNetscape Bookmark形式に準拠しているか確認
- Chromeを再起動してから再度インポートを試みる
- ブックマークファイルのエンコーディングがUTF-8であることを確認

---

このガイドを参考に、Clineを活用してslack-to-bookmarkプロジェクトの開発とテストを効率的に行ってください。適切なテストを実施することで、アプリケーションの品質と信頼性を向上させることができます。
