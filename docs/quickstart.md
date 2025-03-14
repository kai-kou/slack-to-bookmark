# クイックスタートガイド

このガイドでは、Slack-to-Bookmarkツールを最短で設定して使用する方法を説明します。初めてPythonを使う方やGitに不慣れな方でも理解できるように手順を解説しています。セットアップ完了までの所要時間は約5〜10分です。

## このガイドの目的

このガイドでは、以下の手順を順番に説明します：
1. 必要な環境の確認とインストール
2. リポジトリの取得とセットアップ
3. Slack APIの設定と認証情報の取得
4. 環境設定ファイルの作成
5. スクリプトの実行とブックマークの生成
6. ブックマークのインポート方法

各ステップで詳細な説明を提供します。

## 前提条件

### 必要なソフトウェア
- Python 3.6以上がインストールされていること
- Chromeブラウザがインストールされていること
- Slackワークスペースへの管理者アクセス権限があること（もしくはAPIアプリを作成する権限）

### Pythonがインストールされているか確認する方法

1. コマンドプロンプト（Windows）またはターミナル（Mac）を開きます
2. 以下のコマンドを入力してEnterキーを押します：

```bash
python --version
```

3. バージョン情報（例：`Python 3.9.5`）が表示されれば、Pythonはすでにインストールされています
4. 「コマンドが見つかりません」というエラーが表示される場合は、Pythonをインストールする必要があります

### Pythonをインストールする方法

#### Windows
1. [Python公式サイト](https://www.python.org/downloads/)にアクセスし、最新バージョンをダウンロード
2. ダウンロードしたインストーラーを実行
3. インストール時に「Add Python to PATH」オプションにチェックを入れる
4. 「Install Now」をクリックしてインストール

#### Mac
1. [Python公式サイト](https://www.python.org/downloads/)にアクセスし、最新バージョンをダウンロード
2. ダウンロードしたパッケージを開き、指示に従ってインストール
3. または、[Homebrew](https://brew.sh/index_ja)がインストールされている場合は、ターミナルで以下を実行：
   ```bash
   brew install python
   ```

## 1. リポジトリを準備する

### GitHubからコードを取得する（2つの方法）

#### A. Gitを使用する方法（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/slack-to-bookmark.git

# ディレクトリに移動
cd slack-to-bookmark

# 必要なパッケージをインストール
pip install -r requirements.txt
```

#### B. ZIPファイルとしてダウンロードする方法

1. ブラウザで[リポジトリページ](https://github.com/YOUR_USERNAME/slack-to-bookmark)にアクセス
2. 緑色の「Code」ボタンをクリック
3. 「Download ZIP」を選択
4. ダウンロードしたZIPファイルを任意の場所に解凍
5. コマンドプロンプト（Windows）またはターミナル（Mac）を開く
6. 解凍したディレクトリに移動（`cd`コマンドを使用）
7. 以下のコマンドを実行して必要なパッケージをインストール：

```bash
pip install -r requirements.txt
```

> **ヒント**: Windows環境では、フォルダを右クリックして「コマンドプロンプトをここで開く」または「PowerShellウィンドウをここで開く」オプションを使うと便利です。

## 2. Slack APIトークンを取得する

### 2.1. Slackアプリを作成

1. [Slack API管理画面](https://api.slack.com/apps)にアクセスし、Slackアカウントでログインします。
2. 「Create New App」ボタンをクリックします。
3. 「From scratch」を選択します。
4. アプリ名（例: 「Slack Bookmarks」）を入力し、使用するワークスペースを選択して「Create App」をクリックします。

> **ヒント**: アプリ名は後でSlackのチャンネルに表示される名前になります。分かりやすい名前を選びましょう。

### 2.2. 必要な権限を設定

1. 左側のメニューから「OAuth & Permissions」を選択します。

2. 「Scopes」セクションまでスクロールし、「Add an OAuth Scope」ボタンをクリックして以下の権限を追加します：
   - `channels:read` - 公開チャンネル情報の読み取り
   - `groups:read` - プライベートチャンネル情報の読み取り
   - `users:read` - ユーザー情報の読み取り
   - `im:read` - ダイレクトメッセージの読み取り

> **重要**: すべての権限を追加してください。不足していると一部の機能が動作しません。

### 2.3. アプリをワークスペースにインストールしてトークンを取得

1. 「OAuth & Permissions」ページで「Install to Workspace」ボタンをクリックします。

2. 確認画面で「許可する」をクリックします。

3. インストール後、**User OAuth Token**（`xoxp-`で始まるトークン）をコピーします。これは非常に重要です！

> **重要**: 必ず**ユーザートークン(xoxp-)**を使用してください。ボットトークン(xoxb-)では機能が制限され、プライベートチャンネルの取得などができません。
> 
> トークンは非常に重要な情報なので、安全に管理し、決して公開しないでください。

## 3. 環境設定ファイルを作成

1. サンプルファイルをコピーして新しい環境設定ファイルを作成します：

```bash
# Windowsの場合
copy .env.sample .env

# MacまたはLinuxの場合
cp .env.sample .env
```

2. `.env`ファイルをテキストエディタで開きます：
   - Windowsの場合：メモ帳やVSCodeなどで開く
   - Macの場合：TextEditやVSCodeなどで開く

3. 以下の情報を入力します：

```
SLACK_TOKEN=xoxp-あなたのAPIトークン
WORKSPACE_NAME=あなたのワークスペース名
WORKSPACE_ID=あなたのワークスペースID
```

例（実際の値に置き換えてください）：
```
SLACK_TOKEN=xoxp-YOUR_SLACK_API_TOKEN_HERE
WORKSPACE_NAME=mycompany
WORKSPACE_ID=T00000000
```

### ワークスペースIDの見つけ方

ワークスペースIDは通常「T」で始まる文字列で、以下の方法で確認できます：

1. **Slack URLから:**
   - ブラウザでSlackにログインし、URLを確認します
   - `https://{ワークスペース名}.slack.com/` の`{ワークスペース名}`部分がワークスペース名です

2. **ブラウザでSlackを開いた状態で:**
   - アドレスバーのURLを確認し、`https://app.slack.com/client/T01234ABCD/` の `T01234ABCD` 部分がワークスペースIDです

3. **Slackアプリの管理画面から:**
   - Slackで左上のワークスペース名をクリック
   - 「設定と管理」→「ワークスペースの設定」を選択
   - 「詳細情報」セクションでワークスペースIDを確認

## 4. アプリを実行

コマンドプロンプト（Windows）またはターミナル（Mac）で、リポジトリのディレクトリに移動し、以下のコマンドを実行します：

```bash
python slack_to_bookmark.py
```

実行すると、以下のファイルが生成されます：
- `slack_bookmarks.html` - 全チャンネル用ブックマーク
- `slack_public_bookmarks.html` - 公開チャンネルのみのブックマーク
- `slack_user_dms.html` - ユーザーDM用ブックマーク
- `bookmark_guide*.html` - 各ブックマークのインポート手順ガイド

自動的にブラウザが開き、インポート手順のガイドが表示されます。

> **注意**: デフォルトブラウザがChromeでない場合は、以下のいずれかの方法でガイドを表示できます：
> - 生成された`bookmark_guide.html`ファイルをChromeで手動で開く
> - または、`slack_bookmarks.html`ファイルを直接Chromeのブックマークマネージャーからインポート

ブラウザが開かない場合は、生成されたHTMLファイルを手動で開いてください。これらのファイルはプロジェクトのルートディレクトリに保存されています。



## 5. ブックマークをインポート

### Chromeでブックマークをインポートする方法

1. Chromeでブックマークマネージャーを開きます：
   - Macの場合: `Cmd+Option+B`
   - Windowsの場合: `Ctrl+Shift+O`

2. ブックマークマネージャーの右上の「...」（三点リーダー）をクリックし、「ブックマークをインポート」を選択します。

3. 「HTMLファイルから」を選択し、生成されたHTMLファイル（例: `slack_bookmarks.html`）を選択します。

4. 「開く」をクリックしてインポートします。

5. ブックマークバーでSlackフォルダを確認します。フォルダをクリックすると、すべてのSlackチャンネルがブックマークとして表示されます。

## よくあるトラブルと解決策

### プライベートチャンネルが表示されない
- **エラーメッセージ例**: `Error retrieving private channels: not_allowed_token_type`
- **原因**: ユーザートークンを使用していない、または権限が不足している
- **解決策**: 
  1. ユーザートークン(xoxp-)を使用していることを確認（ボットトークンxoxb-ではなく）
  2. 必要な権限スコープ `groups:read` が追加されていることを確認
  3. アプリを再インストールして新しいトークンを取得

### エラー「SLACK_TOKEN環境変数が設定されていません」
- **エラーメッセージ例**: `SLACK_TOKEN環境変数が設定されていません。`
- **原因**: .envファイルが正しく設定されていない
- **解決策**: 
  1. .envファイルがプロジェクトルートディレクトリに存在することを確認
  2. ファイル内に`SLACK_TOKEN=xoxp-...`の行があることを確認
  3. トークンが正しくコピーされていることを確認（余分な空白や改行がないか）

### 「not_allowed_token_type」エラー
- **エラーメッセージ例**: `Error: not_allowed_token_type`
- **原因**: ボットトークン(xoxb-)を使用している
- **解決策**: OAuth & Permissionsページで「User OAuth Token」（xoxp-で始まる）を使用する

### 「invalid_auth」エラー
- **エラーメッセージ例**: `Error: invalid_auth`
- **原因**: トークンが無効または期限切れ
- **解決策**: Slack API管理画面でアプリを再インストールし、新しいトークンを取得

### プログラムが実行されない（Pythonエラー）
- **エラーメッセージ例**: `ModuleNotFoundError: No module named 'slack_sdk'`
- **原因**: 必要なPythonパッケージがインストールされていない
- **解決策**: `pip install -r requirements.txt` コマンドを実行して依存パッケージをインストールする

## 次のステップ

### ショートカットの設定（オプション）

ブックマークを使いこなすためのショートカット設定ガイド：

- **Macユーザー向け**: [Mac Launcherガイド](./mac_launcher_guide.md)
  - Alfred、Raycast、SpotlightなどのランチャーツールでSlackブックマークを素早く開く方法

- **Windowsユーザー向け**: [Windows Launcherガイド](./windows_launcher_guide.md)
  - PowerToys Run、Wox、Windows検索などのツールでSlackブックマークを素早く開く方法

### その他の便利な情報

- より詳細なSlack API設定: [Slack API設定ガイド](./slack_api_setup.md)
- セキュリティについて: [セキュリティガイドライン](./security_guidelines.md)
- テスト方法: [テストガイド](./testing_guide.md)
