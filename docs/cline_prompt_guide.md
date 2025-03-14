# Slack to Bookmark プロジェクト - Clineプロンプトガイド

このドキュメントでは、まっさらな状態からClineを使用して「Slack to Bookmark」プロジェクトを実装するための手順を説明します。

## 概要

このプロンプトガイドを使用することで、プログラミング知識がなくても、Clineに指示するだけで「Slack to Bookmark」プロジェクトの全ファイルを生成できます。プロンプトをコピー＆ペーストするだけで、Clineが自動的に必要なコードを生成します。

## 使用方法

1. VSCodeで新しいフォルダを作成し、開きます
2. Clineのチャットパネルを開きます（VSCode右下のClineアイコンをクリック）
3. 以下の「プロンプト」セクションからプロンプトをコピー
4. Clineのチャットパネルにペーストし、送信
5. 生成されたコードをそれぞれ指定のファイル名で保存

## プロジェクト構成

現在のプロジェクトは以下のディレクトリ構造になっています：

```
slack-to-bookmark/
├── __init__.py
├── .env.sample               # 環境変数のサンプルファイル
├── .gitignore
├── all_channel_guide.html    # 全チャンネル用ガイドページ
├── check_env.py              # 環境変数チェックスクリプト
├── i18n.py                   # 国際化サポート
├── public_channel_guide.html # 公開チャンネル用ガイドページ
├── README.md                 # プロジェクト説明
├── requirements.txt          # 必要なパッケージリスト
├── security_check.py         # セキュリティチェックスクリプト
├── slack_to_bookmark.py      # メインスクリプト
├── user_dm_guide.html        # DM用ガイドページ
├── demos/                    # デモファイル
│   ├── demo_channel_guide.html
│   ├── demo_slack_channels.html
│   ├── demo_slack_to_bookmark.py
│   ├── demo_slack_users_bookmarks.html
│   ├── demo_slack_users.html
│   └── demo_user_guide.html
├── docs/                     # ドキュメント
│   ├── cline_implementation_guide.md
│   ├── cline_prompt_guide.md
│   ├── mac_launcher_guide.md
│   ├── quickstart.md
│   ├── README.md
│   ├── security_guidelines.md
│   ├── slack_api_setup.md
│   ├── testing_guide.md
│   ├── windows_launcher_guide.md
│   ├── setup/
│   │   └── slack_app_permissions.md
│   └── troubleshooting/
│       └── invalid_auth_resolution.md
├── src/                      # ソースコード
│   ├── __init__.py
│   ├── bookmark_generator.py
│   ├── check_env.py
│   ├── guide_generator.py
│   ├── i18n.py
│   ├── security_check.py
│   ├── slack_client.py
│   ├── slack_to_bookmark.py
│   ├── locales/
│   │   ├── en/
│   │   │   └── messages.json
│   │   └── ja/
│   │       └── messages.json
│   └── templates/
│       └── guide.html
└── tests/                    # テスト
    ├── test_slack_to_bookmark.py
    └── test_slack_token.py
```

## プロンプト

プロジェクトを構築するためのプロンプトは、モジュール別に分けて実行します。各プロンプトを順番に実行してください。

### ステップ1: メインスクリプトとソースモジュール

```
SlackチャンネルやDMをChromeブックマークに変換するPythonプロジェクトを作成してください。
以下の機能を実装してください：

1. Slack APIを使用してワークスペース内のチャンネル情報を取得（公開・非公開両方）
2. Slack APIを使用してユーザー情報を取得
3. Chrome用のHTMLブックマークファイルを生成（Netscape Bookmark File Format）
   a. 全チャンネル用ブックマークファイル
   b. 公開チャンネルのみのブックマークファイル
   c. ユーザーDM用のブックマークファイル
4. ブックマークのインポート手順を説明するHTMLガイドページを生成
5. 生成したガイドページを自動的にブラウザで開く
6. 多言語サポート（日本語と英語）

以下の要件に従って実装してください：
- 適切なディレクトリ構造で、モジュール分割された形式にする
- src/ディレクトリ内に各機能ごとに分けたモジュールを作成
- 環境変数から設定を読み込む（.envファイル）
- エラーハンドリングとロギングを適切に実装
- 詳細なコメントを日本語で記述
- SlackのチャンネルやDMのURLはSlackアプリで直接開くリンク形式にする（slack://channel?team=...）
- テンプレートを使用してHTMLを生成する

以下のファイルを作成してください：
1. src/slack_client.py - Slack APIと通信するモジュール
2. src/bookmark_generator.py - ブックマークを生成するモジュール
3. src/guide_generator.py - ガイドページを生成するモジュール
4. src/i18n.py - 国際化サポートモジュール
5. src/slack_to_bookmark.py - メインスクリプト
6. src/check_env.py - 環境変数チェックモジュール
```

### ステップ2: 必要なパッケージリスト

```
先ほど作成したSlackチャンネルとDMをブックマークに変換するプロジェクトに必要なPythonパッケージを、requirements.txtファイルとして作成してください。
必要なパッケージには以下を含めてください：
- slack_sdk
- python-dotenv
- jinja2
- pytest (テスト用)
- colorama (カラー出力用)
```

### ステップ3: 環境変数テンプレート

```
先ほど作成したSlack to Bookmarkプロジェクト用の.env.sampleファイルを作成してください。
このファイルには以下の環境変数を含め、詳細な説明とサンプル値（ダミー値）を記載してください：

1. SLACK_TOKEN - Slack API トークン
2. WORKSPACE_NAME - ワークスペース名
3. WORKSPACE_ID - ワークスペースID
4. LANGUAGE - 使用言語（ja または en）
5. LOG_LEVEL - ログレベル（INFO, DEBUG, WARNING, ERROR）

各環境変数にはコメントで詳細な説明を付け、ユーザーがどこでこれらの値を取得できるかも明記してください。
```

### ステップ4: セキュリティチェックスクリプト

```
Slack to Bookmarkプロジェクト用のセキュリティチェックスクリプト「security_check.py」を作成してください。
このスクリプトは以下の機能を持つ必要があります：

1. プロジェクトディレクトリ内のファイルをスキャンし、SlackトークンやワークスペースIDなどの機密情報がコード内に直接記述されていないか確認
2. .envファイルが.gitignoreに含まれているか確認
3. .env.sampleと.envの内容を比較し、必要な環境変数が設定されているか確認
4. 問題が見つかった場合は警告を表示し、修正方法を提案
5. 色付きの出力で結果を表示（成功は緑、警告は黄色、エラーは赤）

Pythonで実装し、適切なコメントを日本語で記述してください。
src/security_check.pyモジュールとセキュリティチェック用コマンドラインスクリプトを作成してください。
```

### ステップ5: テンプレートと国際化

```
Slack to Bookmarkプロジェクト用のテンプレートと国際化ファイルを作成してください。

1. src/templates/guide.html - ガイドページのHTMLテンプレート
2. src/locales/ja/messages.json - 日本語メッセージファイル
3. src/locales/en/messages.json - 英語メッセージファイル

ガイドテンプレートは、ブックマークのインポート手順をわかりやすく説明する内容にし、
メッセージファイルには、アプリケーション内で使用されるすべての文字列を定義してください。
```

### ステップ6: テストコード

```
Slack to Bookmarkプロジェクト用のテストコードを作成してください。

1. tests/test_slack_to_bookmark.py - メイン機能のテスト
2. tests/test_slack_token.py - APIトークンの検証テスト

モック（Mock）を使用してSlack APIとの通信をシミュレートし、
主要な機能が正しく動作することを確認するテストを作成してください。
```

### ステップ7: デモファイル

```
Slack to Bookmarkプロジェクトのデモ用ファイルを作成してください。

1. demos/demo_slack_to_bookmark.py - 簡易版のメインスクリプト
2. demos/demo_slack_channels.html - チャンネル一覧のサンプル
3. demos/demo_slack_users.html - ユーザー一覧のサンプル
4. demos/demo_channel_guide.html - チャンネルガイドのサンプル
5. demos/demo_user_guide.html - ユーザーガイドのサンプル

デモファイルはプロジェクトの基本的な機能を示すものにしてください。
```

### ステップ8: ドキュメント

```
Slack to Bookmarkプロジェクト用のドキュメントを作成してください。

1. README.md - プロジェクトの概要と使用方法
2. docs/README.md - ドキュメントの目次
3. docs/quickstart.md - クイックスタートガイド
4. docs/slack_api_setup.md - Slack API設定ガイド
5. docs/testing_guide.md - テストガイド
6. docs/security_guidelines.md - セキュリティガイドライン
7. docs/mac_launcher_guide.md - Macのランチャーガイド
8. docs/windows_launcher_guide.md - Windowsのランチャーガイド
9. docs/setup/slack_app_permissions.md - Slackアプリ権限設定ガイド
10. docs/troubleshooting/invalid_auth_resolution.md - 認証エラー解決ガイド

各ドキュメントは初心者にもわかりやすい日本語で作成し、
必要に応じてスクリーンショットや図を含めてください。
```

### ステップ9: Cline関連ドキュメント

```
Slack to Bookmarkプロジェクト用のCline関連ドキュメントを作成してください。

1. docs/cline_implementation_guide.md - Clineでの実装ガイド
2. docs/cline_prompt_guide.md - Clineプロンプトガイド

これらのドキュメントは、プログラミング知識がなくてもClineを使って
このプロジェクトを実装できるように説明したものにしてください。
```

## ファイル保存ガイド

Clineが生成したコードやドキュメントは、このプロジェクト構成に合わせて適切に保存してください。
特に以下の点に注意してください：

1. ソースコードは `src/` ディレクトリ内に保存
2. テストコードは `tests/` ディレクトリ内に保存
3. デモファイルは `demos/` ディレクトリ内に保存
4. ドキュメントは `docs/` ディレクトリ内に保存
5. ルートディレクトリには最小限のファイルのみ置く

## 次のステップ

すべてのファイルが生成されたら、以下の手順でプロジェクトをセットアップします：

1. 必要なパッケージをインストール:
   ```
   pip install -r requirements.txt
   ```

2. `.env.sample`をコピーして`.env`を作成し、実際の値を設定:
   ```
   cp .env.sample .env
   ```

3. `.env`ファイルを編集して、必要な環境変数を設定

4. セキュリティチェックを実行:
   ```
   python security_check.py
   ```

5. メインスクリプトを実行:
   ```
   python slack_to_bookmark.py
   ```

以上の手順で、Slack to Bookmarkプロジェクトが完全に実装され、機能するようになります。ブラウザが自動的に開き、生成されたガイドページが表示されます。

## トラブルシューティング

問題が発生した場合は、`docs/troubleshooting/`ディレクトリ内のガイドを参照するか、
以下のプロンプトをClineに送信してください：

```
「Slack to Bookmarkプロジェクトを実行しようとしたところ、次のエラーが発生しました：
[エラーメッセージをここに貼り付け]
このエラーを解決する方法を教えてください。」
```

機能追加や改善したい場合も、Clineに自然言語で指示するだけで対応できます。
