# コントリビューションガイド

Slack to Bookmarkプロジェクトへの貢献をご検討いただきありがとうございます！このガイドでは、プロジェクトへの貢献方法について説明します。

## コントリビューションの方法

以下のような様々な方法でプロジェクトに貢献できます：

- バグレポート
- 機能リクエスト
- コードの改善
- ドキュメントの改善
- テストの追加

## 開発環境のセットアップ

1. リポジトリをフォークしてクローンします：

```bash
git clone https://github.com/YOUR_USERNAME/slack-to-bookmark.git
cd slack-to-bookmark
```

2. 開発用の依存関係をインストールします：

```bash
pip install -r requirements.txt
pip install -e .
pip install pytest pytest-cov flake8 mypy black isort pre-commit
```

3. pre-commitフックをインストールします：

```bash
pre-commit install
```

## コードスタイル

このプロジェクトでは、次のコードスタイルガイドラインを採用しています：

- [PEP 8](https://www.python.org/dev/peps/pep-0008/) - Pythonコードスタイルガイド
- [Google Pythonスタイルガイド](https://google.github.io/styleguide/pyguide.html)に準拠したドキュメンテーション形式
- 行の最大長は100文字
- コード整形には[Black](https://black.readthedocs.io/)を使用
- インポートの整理には[isort](https://pycqa.github.io/isort/)を使用

pre-commitフックが設定されているため、コミット時に自動的にこれらのスタイルガイドラインがチェックされます。

## テスト

変更を加える際は、以下を確認してください：

1. 既存のテストがすべて通過すること
2. 新しい機能や修正には適切なテストが追加されていること

テストを実行するには：

```bash
pytest --cov=. tests/
```

## Pull Requestの提出

1. 新しいブランチを作成して作業します：

```bash
git checkout -b feature/my-new-feature
```

2. 変更を加え、適切なテストを追加します

3. ローカルでテストを実行し、すべてのテストが通過することを確認します

4. pre-commitチェックを実行して、コードスタイルに問題がないことを確認します：

```bash
pre-commit run --all-files
```

5. コミットしてプッシュします：

```bash
git commit -m "機能追加: 新機能の説明"
git push origin feature/my-new-feature
```

6. GitHubでPull Requestを作成します

## 多言語サポート

新しいテキストを追加する場合は、以下の手順に従ってください：

1. `locales/ja/messages.json` と `locales/en/messages.json` の両方に適切なキーと翻訳を追加します
2. コード内で `i18n.t('キー')` を使用して翻訳テキストを取得します

## セキュリティに関する考慮事項

セキュリティに関する問題（特にAPI認証情報の取り扱い）を見つけた場合は、Issue Trackerで公開せず、メンテナに直接連絡してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。プロジェクトに貢献することで、あなたの貢献物もMITライセンスの下で公開されることに同意したものとみなします。
