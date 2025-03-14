# MacのSpotlightを使ったSlackブックマークの活用方法

Chromeにインポートしたブックマークは、MacのSpotlightを使って素早くアクセスすることができます。

## セットアップ

1. 本ツールを使ってSlackチャンネルやDMのブックマークをChromeにインポートします
2. Chromeでブックマークをよく使う項目に追加しておくとSpotlight検索で見つけやすくなります

## 使い方

### Spotlightでの検索

1. `⌘ + Space` を押してSpotlightを起動
2. チャンネル名やユーザー名の一部を入力（例: `#general` や `@username`）
3. 「Bookmarks」カテゴリに表示されるブックマークを選択

### ヒント

- 日本語名のチャンネルやユーザー名は日本語のまま検索できます
- ブックマークに特定のプレフィックス（例: `sl-`）を付けておくと検索しやすくなります
- Spotlightの検索結果から直接Slackアプリが起動されます

## トラブルシューティング

- Spotlightでブックマークが検索結果に表示されない場合:
  - System Settings > Spotlight > Search Results で「Bookmarks & History」にチェックが入っているか確認してください
  - Spotlight インデックスを再構築: `sudo mdutil -E /`

## 高度な使い方: Alfred との連携

[Alfred](https://www.alfredapp.com/) を使用している場合は、より高度なワークフローを設定できます:

1. Alfred の Preferences を開く
2. Features > Web Bookmarks を有効にする
3. Chrome のブックマークを含めるよう設定

これにより、`sl` などのキーワードを入力してからチャンネル名を入力するだけで、対象のSlackチャンネルに直接ジャンプできるようになります。
