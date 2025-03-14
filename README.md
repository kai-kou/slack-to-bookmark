# Slack to Bookmark v1.0.0

SlackチャンネルやDMをChromeブックマークに変換し、より簡単にアクセスできるようにするツールです。このツールを使うと、よく使うSlackチャンネルやDMに素早くアクセスできるようになります。

> **📚 初めて使用する方へ**: [クイックスタートガイド](./docs/quickstart.md)でステップバイステップの導入手順を確認できます。セットアップの所要時間は約5〜10分です。

## 対応環境

- **対応OS**: Windows 10/11, macOS 10.15以降, Linux (Ubuntu 20.04以降)
- **必要なブラウザ**: Google Chrome 90以降, Microsoft Edge 90以降
- **必要なPython**: Python 3.6以降（推奨: Python 3.8または3.9）

## 機能

- Chrome用のHTMLブックマークファイルを生成
- すべてのSlackチャンネル（公開・非公開）のブックマークを作成
- 公開チャンネルのみのブックマークを作成
- **特定のチャンネルのみ**をブックマークに含める機能（フィルタリング）
- ユーザーとのダイレクトメッセージ用のブックマークを作成
- ブックマークのインポート手順を記載したガイドページを自動生成
- ブラウザで直接Slackを開くURLスキーム（`slack://`）を使用
- チャンネル名のアルファベット順にソート
- プライベートチャンネルには 🔒 マークを表示
- コマンドラインオプションによる柔軟な設定
- **NEW** 企業名や個人情報の匿名化機能

## ファイル構成

- `slack_to_bookmark.py` - メインPythonスクリプト (src内の実装へのラッパー)
- `setup.py` - パッケージ化のためのセットアップファイル
- `security_check.py` - コミット前にセキュリティリスクをチェックするスクリプト
- `requirements.txt` - 必要なPythonパッケージのリスト
- `.env.sample` - 環境変数設定のサンプルファイル
- `src/` - ソースコードディレクトリ
  - `slack_to_bookmark.py` - メインクラスの実装
  - `slack_client.py` - Slack APIとの通信を担当
  - `bookmark_generator.py` - ブックマークファイル生成を担当
  - `guide_generator.py` - ガイドページ生成を担当
  - `check_env.py` - 環境変数の検証用モジュール
  - `security_check.py` - セキュリティチェック機能の実装
  - `data_anonymizer.py` - 機密情報の匿名化処理を担当
  - `i18n.py` - 国際化対応モジュール
  - `locales/` - 多言語対応用リソース
    - `en/messages.json` - 英語メッセージ
    - `ja/messages.json` - 日本語メッセージ
  - `templates/` - HTMLテンプレート
- `docs/` - ドキュメント
  - `quickstart.md` - クイックスタートガイド（初心者向け）
  - `mac_launcher_guide.md` - MacのランチャーツールでSlackブックマークを活用する方法
  - `windows_launcher_guide.md` - WindowsのランチャーツールでSlackブックマークを活用する方法
  - `cline_implementation_guide.md` - Clineを使ったプロジェクト実装ガイド
  - `cline_prompt_guide.md` - Clineプロンプト作成ガイド
  - `slack_api_setup.md` - Slack API設定に関する詳細ガイド
  - `testing_guide.md` - テスト方法に関するガイド
  - `security_guidelines.md` - セキュリティに関するガイドライン
  - `README.md` - ドキュメント目次
  - `setup/` - セットアップ関連ガイド
  - `troubleshooting/` - トラブルシューティングガイド
- `tests/` - テストコード
  - `test_slack_to_bookmark.py` - メイン機能のテスト
  - `test_slack_token.py` - Slackトークン検証のテスト
- `demos/` - デモ用ファイル

### 自動生成ファイル (実行時に作成)
- `slack_all_channels.html` - 全チャンネル用のブックマークファイル
- `slack_public_channels.html` - 公開チャンネルのみのブックマークファイル
- `slack_user_dms.html` - ユーザーDM用のブックマークファイル
- `all_channel_guide.html` - 全チャンネルブックマークのインポート手順
- `public_channel_guide.html` - 公開チャンネルブックマークのインポート手順
- `user_dm_guide.html` - ユーザーDMブックマークのインポート手順
- `anonymizer_mappings.json` - 匿名化マッピング情報（匿名化機能使用時）

## 必要環境

- Python 3.6以上
  - Pythonのインストール方法は[クイックスタートガイド](./docs/quickstart.md#pythonをインストールする方法)を参照
- 必要なPythonパッケージ（`pip install -r requirements.txt`でインストール）:
  - slack_sdk - Slack APIとの通信
  - python-dotenv - 環境変数の読み込み
- Chromeブラウザ（ブックマークのインポート用）

## セットアップ

### 1. リポジトリを準備する
リポジトリをクローンまたはZIPファイルとしてダウンロードします:

```bash
# Gitを使用する場合
git clone https://github.com/YOUR_USERNAME/slack-to-bookmark.git
cd slack-to-bookmark

# または、ZIPファイルをダウンロードして解凍し、そのディレクトリに移動
```

詳細な手順は[クイックスタートガイド](./docs/quickstart.md#1-リポジトリを準備する)を参照してください。

### 2. 必要なPythonパッケージをインストール:
```bash
pip install -r requirements.txt
```

### 3. SlackのAPIトークンを設定:
プロジェクトディレクトリに`.env`ファイルを作成（提供された`.env.sample`をテンプレートとして使用可能）:
```
SLACK_TOKEN=your_slack_token_here
WORKSPACE_NAME=your-workspace-name
WORKSPACE_ID=your-workspace-id
```


**重要**: このツールには**ユーザートークン(xoxp-)** が必要です。ボットトークン(xoxb-)では一部の機能が動作しません。

### 4. トークンとワークスペース情報の取得:
- [Slack API設定ガイド](./docs/slack_api_setup.md)の手順に従って必要な情報を取得してください
- **ワークスペースID**はSlack URLの「https://[ワークスペース名].slack.com/」の一部、または管理画面のワークスペース設定から確認できます（通常「T」で始まるIDです）


### 5. 必要な権限スコープ:
SlackアプリにはSlack APIにアクセスするための以下の権限が必要です:
- `channels:read` - 公開チャンネル情報
- `groups:read` - プライベートチャンネル情報 
- `users:read` - ユーザー情報
- `im:read` - ダイレクトメッセージ情報


> **注意**: ワークスペースの管理者権限がない場合は、管理者にアプリ作成を依頼するか、管理者に以下を依頼してください:
> 1. Slackアプリを作成し、必要な権限を付与
> 2. ユーザートークンを取得して共有
> 3. アプリをワークスペースにインストール

## セキュリティ注意事項

### APIトークンの管理
- **重要**: SlackのAPIトークンは機密情報であり、絶対にバージョン管理システム（Git）にコミットしないでください
- このプロジェクトは`.env`ファイル（`.gitignore`に含まれています）からトークンを読み込むよう設定されています
- 誤ってトークンをコードに直接記述しないよう注意してください

### 環境情報の保護
- `.env`ファイルには個人や組織の内部情報（ワークスペース名やID）が含まれるため、厳重に管理してください
- プロジェクトコードをスクリーンショットで共有する際や、スクリーンキャストを録画する際には`.env`ファイルが表示されないよう注意してください

### 生成されるデータの取り扱い 
- 生成されるブックマークファイル（`slack_*.html`）には、チャンネル名やユーザー名など組織内の情報が含まれます
- これらのファイルは`.gitignore`で除外されていますが、メールやメッセージアプリなどで誤って共有しないよう注意してください
- 特にユーザーブックマーク（`slack_user_dms.html`）には組織のメンバー情報が含まれるため、取り扱いに注意してください
- 組織外部に共有する必要がある場合は、`--anonymize`オプションを使用して機密情報を匿名化することを強く推奨します

### 匿名化機能の使用
- `--anonymize`オプションを使用すると、生成されたファイル内の機密情報（企業名、個人名、ワークスペースIDなど）が自動的に匿名化されます
- 匿名化されたデータは一貫性を保つため、同じ情報は常に同じダミーデータに置換されます（マッピング情報は`anonymizer_mappings.json`に保存）
- この機能はスクリーンショットの共有やデモ用途に特に有用です

### security_check.pyの使用方法
- このスクリプトは、コミット前に機密情報のチェックを行います
- 実行するには: `python security_check.py` （実行結果に従って対処してください）

より詳細なセキュリティ情報については[セキュリティガイドライン](./docs/security_guidelines.md)を参照してください。

## 使用方法

### 基本的な使い方

Pythonスクリプトを実行:
```bash
python slack_to_bookmark.py
```

スクリプトはHTMLブックマークファイルとガイドページを生成し、ブラウザで自動的に開きます。

### 実行結果

1. ブックマークファイルが生成されます（`slack_all_channels.html`など）
2. インポートガイドページがブラウザで開きます
3. Chrome/Edgeブックマークマネージャーが自動的に開きます
4. ガイドの手順に従ってブックマークをインポートします


## クイックスタートガイド

初めて使用する場合は以下の手順に従ってください:

1. リポジトリをクローンまたはダウンロード:
   ```bash
   git clone https://github.com/YOUR_USERNAME/slack-to-bookmark.git
   cd slack-to-bookmark
   ```

2. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

3. API設定:
   - [Slack API管理画面](https://api.slack.com/apps)で新規アプリを作成
   - 「OAuth & Permissions」で次の権限を追加: `channels:read`, `groups:read`, `users:read`, `im:read`
   - アプリをワークスペースにインストールし、**ユーザートークン(xoxp-...)** を取得

4. 環境設定:
   - `.env.sample` を `.env` にコピー:
     ```bash
     # Windowsの場合
     copy .env.sample .env
     
     # MacまたはLinuxの場合
     cp .env.sample .env
     ```
   - `.env` ファイルを編集し、Slackトークンとワークスペース情報を追加

5. 実行:
   ```bash
   python slack_to_bookmark.py
   ```

6. ブックマークのインポート:
   - 生成されたガイドページの指示に従ってChromeにブックマークをインポート

より詳細な手順については[クイックスタートガイド](./docs/quickstart.md)と[Slack API設定ガイド](./docs/slack_api_setup.md)を参照してください。

## コマンドラインオプション

特定の要件に合わせてブックマークを生成するためのコマンドラインオプションが用意されています：

```bash
# 基本的な使い方
python slack_to_bookmark.py

# 特定のチャンネルのみをブックマークに含める
python slack_to_bookmark.py --channels "general,random,project-a"

# 公開チャンネルのみをブックマークに含める
python slack_to_bookmark.py --public-only

# ユーザーDMブックマークを生成しない
python slack_to_bookmark.py --no-dm

# バージョン情報の表示
python slack_to_bookmark.py --version

# 複数のオプションを組み合わせる
python slack_to_bookmark.py --channels "general,random" --no-dm

# 機密情報（企業名、個人名など）を匿名化する
python slack_to_bookmark.py --anonymize
```

## FAQ（よくある質問と回答）

### Q: このツールは何に役立ちますか？
**A:** SlackのチャンネルやDMに素早くアクセスするためのChromeブックマークを作成します。頻繁に使用するチャンネルへのアクセスが簡単になり、作業効率が向上します。

### Q: どのブラウザに対応していますか？
**A:** 主にChromeを対象としていますが、Firefox、Edge、Safariなど、HTML形式のブックマークをインポートできるブラウザであれば使用可能です。

### Q: プライベートチャンネルもブックマークに追加できますか？
**A:** はい、プライベートチャンネルもブックマークに追加できます。ただし、ユーザートークン(xoxp-)を使用し、適切な権限スコープ(`groups:read`)を設定する必要があります。

### Q: ブックマークをクリックするとどうなりますか？
**A:** `slack://`プロトコルを使用しているため、インストール済みのSlackアプリが直接開きます。ブラウザ版のSlackではなく、デスクトップアプリが起動します。

### Q: ブックマークはどのくらいの頻度で更新すべきですか？
**A:** チャンネルが追加・削除されたとき、またはユーザーが入社・退社したときなど、Slackの構成が変更されたときに実行することをお勧めします。定期的な更新（例：月1回）も良いでしょう。

### Q: 特定のチャンネルだけをブックマークに含めることはできますか？
**A:** はい、`--channels`オプションを使用して、特定のチャンネルだけをブックマークに含めることができます。例: `python slack_to_bookmark.py --channels "general,random,project-a"`

### Q: デフォルトブラウザがChromeではない場合はどうすればいいですか？
**A:** 自動で開かれるブラウザがChromeでない場合は、生成された`bookmark_guide.html`ファイルをChromeで手動で開き、そこからガイドに従ってください。または、生成されたHTMLファイル（`slack_bookmarks.html`など）を直接Chromeの「ブックマークマネージャー」からインポートすることもできます。

### Q: 生成されたブックマークファイルを保存しておくべきですか？
**A:** 毎回新しいブックマークファイルが生成されるため、通常は保存しておく必要はありません。ただし、複数の環境で同じブックマークを使用したい場合は、生成されたHTMLファイルをバックアップしておくと便利です。

### Q: リポジトリが更新されたらどうすればいいですか？
**A:** 以下の手順でアップデートしてください：
1. リポジトリの最新バージョンを取得（`git pull`またはZIPダウンロード）
2. 必要に応じて`pip install -r requirements.txt`を再実行
3. 既存の`.env`ファイルはそのまま使用可能（通常は再設定不要）

### Q: 機密情報を含むブックマークファイルを共有する必要がある場合はどうすればいいですか？
**A:** `--anonymize`オプションを使用して実行すると、生成されたファイル内の機密情報（企業名、個人名、ワークスペースIDなど）が自動的に匿名化されます。これにより、組織外部にファイルを共有しても安全です。

## セキュリティ注意事項

### APIトークンの管理
- **重要**: SlackのAPIトークンは機密情報であり、絶対にバージョン管理システム（Git）にコミットしないでください
- このプロジェクトは`.env`ファイル（`.gitignore`に含まれています）からトークンを読み込むよう設定されています
- 誤ってトークンをコードに直接記述しないよう注意してください

### 環境情報の保護
- `.env`ファイルには個人や組織の内部情報（ワークスペース名やID）が含まれるため、厳重に管理してください
- プロジェクトコードをスクリーンショットで共有する際や、スクリーンキャストを録画する際には`.env`ファイルが表示されないよう注意してください

### 生成されるデータの取り扱い 
- 生成されるブックマークファイル（`slack_*.html`）には、チャンネル名やユーザー名など組織内の情報が含まれます
- これらのファイルは`.gitignore`で除外されていますが、メールやメッセージアプリなどで誤って共有しないよう注意してください
- 特にユーザーブックマーク（`slack_user_dms.html`）には組織のメンバー情報が含まれるため、取り扱いに注意してください

### Publicリポジトリでの共有 
- このプロジェクトをパブリックリポジトリとして共有する場合、以下の点に注意してください：
  - `.env`ファイルが`.gitignore`に含まれていることを確認する
  - `.env.sample`ファイルには必ずダミー値のみを使用する
  - 生成されたHTMLファイルが誤ってコミットされていないことを確認する
  - コミット履歴に機密情報が含まれていないことを確認する

### pre-commitフック
- このプロジェクトには、機密情報を誤ってコミットするのを防ぐための pre-commit フックが含まれています
- インストールするには次のコマンドを実行してください:
  ```bash
  chmod +x .git/hooks/pre-commit
  ```
- このフックは以下をチェックします:
  - `.env`ファイルのコミット防止
  - 生成されたHTML（`slack_*.html`、`bookmark_guide*.html`）ファイルのコミット防止
  - Slackトークンや潜在的なワークスペースIDパターンの検出

## トラブルシューティング

よくある問題と解決策:

### 1. APIエラー「not_allowed_token_type」
- **エラーメッセージ例**:
  ```
  Error: not_allowed_token_type
  ```
- **問題**: ボットトークン(xoxb)を使用している
- **解決策**: ユーザートークン(xoxp)を取得して使用する

### 2. プライベートチャンネルが表示されない
- **問題**: アプリにプライベートチャンネルへのアクセス権がない
- **解決策**: 各プライベートチャンネルでコマンド `/invite @アプリ名` を実行

### 3. 「ワークスペースIDが無効」エラー
- **エラーメッセージ例**:
  ```
  Invalid workspace ID. Check your .env file.
  ```
- **問題**: `.env` ファイルのワークスペースIDが正しくない
- **解決策**: Slack URLから正しいワークスペースIDを確認 (T で始まる文字列)

### 4. チャンネル数が予想より少ない
- **問題**: APIトークンの権限不足
- **解決策**: 
  1. Slack API管理画面で必要な権限が全て付与されているか確認
  2. 特に `channels:read` と `groups:read` が重要

### 5. 「Token revoked」エラー
- **エラーメッセージ例**:
  ```
  Error: token_revoked
  ```
- **問題**: トークンが無効化されている
- **解決策**: 新しいトークンを生成する

### 6. モジュールが見つからないエラー
- **エラーメッセージ例**:
  ```
  ModuleNotFoundError: No module named 'slack_sdk'
  ```
- **問題**: 必要なPythonパッケージがインストールされていない
- **解決策**: `pip install -r requirements.txt` を実行する

詳細なトラブルシューティングは[Slack API設定ガイド](./docs/slack_api_setup.md#トラブルシューティング)を参照してください。

## Clineでの実装

このプロジェクトはClineを使用して実装することもできます。Clineを使用すると、コード補完や静的解析などの機能を活用して、より効率的に開発を進めることができます。

詳細なガイドは以下のドキュメントを参照してください：

- [Cline実装ガイド](./docs/cline_implementation_guide.md) - Clineを使ったプロジェクト実装の詳細手順
- [Slack API設定ガイド](./docs/slack_api_setup.md) - SlackのAPI設定に関する詳細ガイド
- [テスト方法ガイド](./docs/testing_guide.md) - Clineを使ったテスト手法についての説明

## 貢献方法

このプロジェクトへの貢献を歓迎します！以下の方法で貢献できます：

1. バグ報告: Issuesを作成して問題を報告
2. 機能リクエスト: 新機能のアイデアをIssuesで提案
3. コード貢献: Pull Requestsを送信
4. ドキュメント改善: ドキュメントの誤りや不足している情報を修正

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](./LICENSE)ファイルを参照してください。
