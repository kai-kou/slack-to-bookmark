# 📚 Slack to Bookmark ドキュメント

このディレクトリには、Slack to Bookmarkプロジェクトに関する各種ドキュメントが含まれています。ニーズに合わせて必要なドキュメントを参照してください。

## 🚀 ドキュメント一覧

### 📝 初めての方向け

- [**クイックスタートガイド**](./quickstart.md) - 初めての方向けにステップバイステップで解説した導入ガイド
  - Pythonのインストール方法からSlack APIの設定、実行方法まで詳しく解説
  - **対象者**: プログラミング経験の少ない方、Slack APIを初めて使う方

### 🔍 活用ガイド

- [**MacでのSlackブックマーク活用方法**](./mac_launcher_guide.md)
  - MacのSpotlight、Alfred、Raycastなどを使ったSlackブックマークの効率的な活用方法
  - キーボードショートカットでチャンネルに素早くアクセスする設定
  - **対象者**: Macユーザー、ショートカットを活用したい方

- [**WindowsでのSlackブックマーク活用方法**](./windows_launcher_guide.md)
  - Windows検索、PowerToys Run、Woxなどのツールでブックマークを活用する方法
  - ランチャーツールとの連携設定手順
  - **対象者**: Windowsユーザー、キーボード操作を重視する方

### 🔐 セキュリティと設定ガイド

- [**Slack API設定ガイド**](./slack_api_setup.md)
  - Slack APIの詳細な設定手順と権限の管理方法
  - トラブルシューティングとよくあるエラーの解決方法
  - **対象者**: APIの設定に詳しい情報が必要な方、トラブルが発生した方

- [**セキュリティガイドライン**](./security_guidelines.md)
  - APIトークンの安全な管理方法
  - 組織情報を含むファイルの取り扱い方
  - 安全なGit操作と情報漏洩の防止策
  - **対象者**: セキュリティを重視する方、組織での利用を検討している方

### 💻 開発者向けガイド

- [**Cline実装ガイド**](./cline_implementation_guide.md)
  - Clineを使った効率的な開発手法
  - コード補完や静的解析を活用した実装方法
  - **対象者**: 開発者、プロジェクトに貢献したい方

- [**テスト方法ガイド**](./testing_guide.md)
  - Clineを使ったテスト手法の説明
  - ユニットテストと統合テストの実装方法
  - **対象者**: 開発者、QAエンジニア

## 📋 利用の流れ

1. **初めての利用**: [クイックスタートガイド](./quickstart.md)で基本的なセットアップを行う
2. **トラブルシューティング**: 問題が発生した場合は[Slack API設定ガイド](./slack_api_setup.md#トラブルシューティング)を参照
3. **効率化**: セットアップ後は[Mac](./mac_launcher_guide.md)または[Windows](./windows_launcher_guide.md)のランチャーガイドでワークフローを効率化
4. **安全な利用**: [セキュリティガイドライン](./security_guidelines.md)を確認して安全に利用

## 🔎 よくある質問

- **Q: Slackのプライベートチャンネルが表示されません**
  - A: ユーザートークン(xoxp-)を使用していることを確認し、[Slack API設定ガイド](./slack_api_setup.md#トラブルシューティング)を参照してください

- **Q: 生成されたブックマークはどこに保存されますか？**
  - A: プロジェクトのルートディレクトリに`slack_bookmarks.html`などのファイルが生成されます

- **Q: ブックマークの更新はどのくらいの頻度で行うべきですか？**
  - A: チャンネルが追加・削除されたとき、または定期的（月1回程度）に実行することをお勧めします

詳細なFAQは[こちら](../README.md#faqよくある質問と回答)を参照してください。

## 📄 概要

Slack to Bookmarkは、SlackチャンネルやDMをChromeブックマークに変換し、より簡単にアクセスできるようにするツールです。このドキュメントセットでは、ツールの使用方法からClineを使った実装方法、テスト手法まで幅広く解説しています。

## 📝 ドキュメントの更新方法

ドキュメントの更新や追加が必要な場合は、以下の手順に従ってください：

1. 対象のMarkdownファイルを編集
2. 新しいドキュメントを追加する場合は、このREADME.mdにも参照を追加
3. 変更をコミット

## 👥 貢献方法

プロジェクトやドキュメントの改善に貢献したい場合は、プルリクエストを作成してください。ドキュメントの誤りや改善点を見つけた場合は、Issueを作成していただいても構いません。以下の点に注意してください：

- ドキュメントは初心者にも分かりやすい言葉で記述する
- 各ドキュメントの更新日を記載する

## 📆 更新履歴

- 2025/3/14: ドキュメント全体の改善、より詳細な説明の追加
- 2025/3/10: クイックスタートガイドの作成
- 2025/3/5: プロジェクト初期リリース
