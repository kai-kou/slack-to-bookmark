# WindowsのランチャーツールでSlackブックマークを活用する方法

Chromeにインポートしたブックマークは、Windowsの各種ランチャーツールと連携して素早くアクセスできます。

## Windows検索を使用した方法

### セットアップ

1. 本ツールを使ってSlackチャンネルやDMのブックマークをChromeにインポートします
2. Chromeでブックマークをお気に入りに追加しておくと検索で見つけやすくなります

### 使い方

1. `Windows + S` または画面左下の検索ボックスをクリック
2. チャンネル名やユーザー名の一部を入力（例: `#general` や `@username`）
3. 「Chrome」カテゴリに表示されるブックマークを選択

### 注意点

- Windows検索はブックマークの検索に対応していますが、インデックスの更新に時間がかかる場合があります
- 検索結果が表示されない場合は、`設定 > 検索 > 検索するコンテンツ` で「ウェブ」にチェックが入っているか確認してください

## PowerToys Runを使用した方法（おすすめ）

[PowerToys Run](https://learn.microsoft.com/ja-jp/windows/powertoys/run) はMicrosoftが提供する高機能なランチャーツールです。

### セットアップ

1. [PowerToys](https://github.com/microsoft/PowerToys/releases/) をインストール
2. PowerToys Runの設定を開き、「Browser Bookmarks」プラグインが有効になっていることを確認

### 使い方

1. `Alt + Space`（デフォルト）でPowerToys Runを起動
2. `b:` の後にチャンネル名やユーザー名を入力（例: `b:general` や `b:@username`）
3. 表示されるブックマークを選択

### ヒント

- `b:` プレフィックスを使うとブックマーク検索に絞り込めます
- 日本語名のチャンネルやユーザー名も検索可能です
- 頻繁に使用するブックマークには、わかりやすいプレフィックス（例: `sl-`）を付けておくと検索しやすくなります

## Wox/Everything を使用した方法

[Wox](http://www.wox.one/) と [Everything](https://www.voidtools.com/) の組み合わせも強力なランチャーとして機能します。

### セットアップ

1. Everything と Wox をインストール
2. Wox の設定で「Chrome Bookmarks」プラグインを有効化

### 使い方

1. `Alt + Space`（デフォルト）で Wox を起動
2. チャンネル名やユーザー名を入力
3. Chrome ブックマークカテゴリの結果を選択

これらのツールを活用することで、Windowsでも素早くSlackチャンネルにアクセスできるようになります。
