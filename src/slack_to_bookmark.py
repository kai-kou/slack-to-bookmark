#!/usr/bin/env python3
"""
Slack to Bookmark - SlackチャンネルとDMリンクをChromeブックマークに変換するツール

このスクリプトはSlack APIを使用して、ワークスペース内のチャンネルとユーザー情報を取得し、
Chromeのブックマークとして利用できるHTMLファイルを生成します。

機能:
- すべてのSlackチャンネル（公開・非公開）のブックマークを生成
- 公開チャンネルのみのブックマークを生成
- 特定のチャンネルのみのブックマークを生成（フィルタリング機能）
- ユーザーとのダイレクトメッセージ用のブックマークを生成
- ブックマークのインポート手順を記載したガイドページを自動生成
"""

import os
import sys
import json
import datetime
import time
import logging
import webbrowser
import argparse
from typing import List, Dict, Any, Optional, Tuple, Set
from pathlib import Path
from dotenv import load_dotenv

# 独自モジュールをインポート
from .slack_client import SlackClient
from .bookmark_generator import BookmarkGenerator
from .guide_generator import GuideGenerator
from .data_anonymizer import DataAnonymizer

# バージョン情報
__version__ = "1.0.0"

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("slack_to_bookmark")


class SlackToBookmark:
    """Slack to Bookmarkメインクラス

    このクラスはアプリケーションのメインクラスとして機能し、次の役割を担います：
    1. 環境変数の読み込みと設定の検証
    2. 各コンポーネント（SlackClient、BookmarkGenerator、GuideGenerator）の連携
    3. エラーハンドリングとロギング
    4. ブラウザでの結果表示
    """

    def __init__(self):
        """
        SlackToBookmarkクラスの初期化

        .envファイルから環境変数を読み込み、SlackClient、BookmarkGenerator、
        GuideGeneratorのインスタンスを初期化します。必要な環境変数（SLACK_TOKEN）が
        存在しない場合はエラーメッセージを表示してプログラムを終了します。

        Raises:
            SystemExit: SLACK_TOKENが見つからない場合
        """
        # 環境変数の読み込み - 強制的に設定ファイルから読み込む
        load_dotenv(override=True)

        # Slack API設定
        self.token = os.getenv("SLACK_TOKEN")
        self.workspace_name = os.getenv("WORKSPACE_NAME", "your-workspace")
        self.workspace_id = os.getenv("WORKSPACE_ID", "T00000000")

        # コンソール出力でワークスペース情報を確認
        logger.info(
            f"設定値: WORKSPACE_NAME={self.workspace_name}, WORKSPACE_ID={self.workspace_id}"
        )

        # トークンの有効性を直接テスト
        try:
            import requests

            url = "https://slack.com/api/auth.test"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(url, headers=headers)
            result = response.json()

            if result.get("ok"):
                logger.info(
                    f"API認証テスト成功: ユーザー={result.get('user')}, チーム={result.get('team')}"
                )
                logger.info(
                    f"APIレスポンスのワークスペース情報: team_id={result.get('team_id')}"
                )

                # .envのワークスペースIDと異なる場合は警告
                if result.get("team_id") != self.workspace_id:
                    logger.warning(
                        f"注意: .envのワークスペースID({self.workspace_id})とAPI認証のチームID({result.get('team_id')})が一致しません"
                    )
                    logger.warning(
                        "修正: .envのWORKSPACE_IDを更新することをお勧めします"
                    )
                    # APIレスポンスからの値を使用
                    self.workspace_id = result.get("team_id")
                    logger.info(
                        f"ワークスペースIDを{self.workspace_id}に自動更新しました"
                    )
            else:
                logger.error(f"API認証テスト失敗: {result.get('error')}")
        except Exception as e:
            logger.error(f"API認証テスト実行中にエラー: {e}")

        # 設定チェック
        if not self.token:
            logger.error(
                "SLACK_TOKEN環境変数が設定されていません。"
                "\n解決策: "
                "\n1. .envファイルが存在することを確認してください"
                "\n2. .env.sampleを.envにコピーして編集:"
                "\n   cp .env.sample .env"
                "\n3. .envファイルを編集し、有効なSlack APIトークンを設定してください"
                "\n   詳しくは docs/slack_api_setup.md を参照してください"
            )
            sys.exit(1)

        # 各クラスの初期化
        self.slack_client = SlackClient(
            self.token, self.workspace_name, self.workspace_id
        )
        self.bookmark_generator = BookmarkGenerator(
            self.workspace_name, self.workspace_id
        )
        self.guide_generator = GuideGenerator()

        logger.info("SlackToBookmark initialized")

    def run(
        self,
        channel_filter: Optional[List[str]] = None,
        public_only: bool = False,
        include_dm: bool = True,
        anonymize: bool = False,
    ) -> bool:
        """
        メイン処理を実行

        次の処理を順番に実行します：
        1. Slack APIからチャンネルとユーザー情報を取得
        2. 指定されたフィルター条件に基づきブックマークファイルを生成
        3. 各ブックマークファイルに対応するインポート手順ガイドを生成
        4. ブラウザでガイドページを表示（任意）

        Args:
            channel_filter: 特定のチャンネル名のリスト（指定した場合はこれらのみを含む）
            public_only: Trueの場合、公開チャンネルのみを対象とする
            include_dm: Trueの場合、ユーザーDMブックマークも生成する

        Returns:
            bool: 処理が成功した場合はTrue、失敗した場合はFalse
        """
        success = True
        generated_files = []
        try:
            logger.info(
                f"Processing with options: channel_filter={channel_filter}, public_only={public_only}, include_dm={include_dm}"
            )

            # チャンネルの取得と出力
            if public_only:
                logger.info("公開チャンネルのみを処理します")
                channels = self.slack_client.get_public_channels()
                output_file = "slack_public_channels.html"
                guide_file = "public_channel_guide.html"
                is_public_only = True
            else:
                logger.info("すべてのチャンネル（公開・非公開）を処理します")
                channels = self.slack_client.get_all_channels()
                output_file = "slack_all_channels.html"
                guide_file = "all_channel_guide.html"
                is_public_only = False

            # フィルタリング（指定があれば）
            if channel_filter:
                logger.info(f"チャンネルフィルター適用: {', '.join(channel_filter)}")
                channels = [ch for ch in channels if ch["name"] in channel_filter]
                if not channels:
                    logger.warning(
                        "フィルターに一致するチャンネルが見つかりませんでした"
                    )

            # チャンネルブックマークの生成
            if channels:
                html_file_path = self.bookmark_generator.generate_channel_bookmarks(
                    channels, output_file
                )
                if html_file_path:
                    generated_files.append(html_file_path)
                    # ガイドページの生成
                    guide_path = self.guide_generator.create_guide(
                        html_file_path, guide_file, is_public_only=is_public_only
                    )
                    if guide_path:
                        generated_files.append(guide_path)
                        # ブラウザでガイドページを開く
                        try:
                            guide_abs_path = os.path.abspath(guide_path)
                            webbrowser.open(f"file://{guide_abs_path}")
                            logger.info(
                                f"チャンネルガイドページを開きました: {guide_path}"
                            )
                        except Exception as e:
                            logger.error(
                                f"ブラウザでファイルを開く際にエラーが発生しました: {e}"
                            )
                    else:
                        logger.error("チャンネルガイドページの生成に失敗しました")
                        success = False
                else:
                    logger.error("チャンネルブックマークの生成に失敗しました")
                    success = False
            else:
                logger.warning("処理対象のチャンネルがありませんでした")

            # ユーザーDM用ブックマークの生成（オプション）
            if include_dm:
                logger.info("ユーザーDM用ブックマークを生成します")
                users = self.slack_client.get_all_users()
                if users:
                    user_dm_output_file = "slack_user_dms.html"
                    user_dm_html_file_path = (
                        self.bookmark_generator.generate_user_dm_bookmarks(
                            users, user_dm_output_file
                        )
                    )
                    if user_dm_html_file_path:
                        generated_files.append(user_dm_html_file_path)
                        # ユーザーDM用ガイドページの生成
                        user_guide_file = "user_dm_guide.html"
                        user_guide_path = self.guide_generator.create_guide(
                            user_dm_html_file_path, user_guide_file, is_user_dm=True
                        )
                        if user_guide_path:
                            generated_files.append(user_guide_path)
                            # ブラウザでユーザーDMガイドページを開く
                            try:
                                guide_abs_path = os.path.abspath(user_guide_path)
                                # webbrowser.open(f"file://{guide_abs_path}")  # チャンネルガイドを開いたので、こちらはコメントアウト
                                logger.info(
                                    f"ユーザーDMガイドページを生成しました: {user_guide_path}"
                                )
                            except Exception as e:
                                logger.error(
                                    f"ブラウザでファイルを開く際にエラーが発生しました: {e}"
                                )
                        else:
                            logger.error("ユーザーDMガイドページの生成に失敗しました")
                            success = False
                    else:
                        logger.error("ユーザーDMブックマークの生成に失敗しました")
                        success = False
                else:
                    logger.warning("処理対象のユーザーが見つかりませんでした")

            # 結果のサマリーを表示
            if generated_files:
                logger.info("処理が完了しました。以下のファイルが生成されました:")
                for f in generated_files:
                    logger.info(f"- {f}")

                # 匿名化処理（オプション）
                if anonymize and generated_files:
                    try:
                        logger.info("生成されたファイルを匿名化しています...")
                        anonymizer = DataAnonymizer()
                        for file_path in generated_files:
                            anonymizer.anonymize_file(file_path)
                        logger.info("すべてのファイルの匿名化が完了しました")
                    except Exception as e:
                        logger.error(f"匿名化処理中にエラーが発生しました: {e}")
                        # 匿名化が失敗してもメインプロセスは成功扱い
            else:
                logger.warning("生成されたファイルはありません")
                success = False

        except Exception as e:
            logger.error(f"実行中にエラーが発生しました: {e}")
            success = False

        return success


def create_parser() -> argparse.ArgumentParser:
    """
    コマンドライン引数パーサーを作成

    Returns:
        argparse.ArgumentParser: 設定済みの引数パーサー
    """
    parser = argparse.ArgumentParser(
        description="SlackチャンネルとDMリンクをChromeブックマークに変換するツール"
    )

    parser.add_argument(
        "--version", action="version", version=f"Slack to Bookmark v{__version__}"
    )

    parser.add_argument(
        "--public-only",
        action="store_true",
        help="公開チャンネルのみを処理する（デフォルト: すべてのチャンネル）",
    )

    parser.add_argument(
        "--no-dm",
        action="store_true",
        help="ユーザーDMブックマークを生成しない（デフォルト: 生成する）",
    )

    parser.add_argument(
        "--channels",
        type=str,
        help="処理対象のチャンネル名（カンマ区切り、例: 'general,random'）",
    )

    parser.add_argument(
        "--anonymize",
        action="store_true",
        help="生成されたファイル内の機密情報（企業名、個人名など）を匿名化する",
    )

    return parser


def main():
    """
    メイン関数

    コマンドラインから実行された際のエントリーポイント。引数を解析して
    SlackToBookmarkクラスを初期化し、処理を実行します。
    """
    parser = create_parser()
    args = parser.parse_args()

    # 開始メッセージ
    logger.info(f"Slack to Bookmark v{__version__} を開始します")

    # チャンネルフィルターの解析（指定されている場合）
    channel_filter = None
    if args.channels:
        channel_filter = [ch.strip() for ch in args.channels.split(",") if ch.strip()]

    # メインクラスのインスタンス化と実行
    app = SlackToBookmark()
    success = app.run(
        channel_filter=channel_filter,
        public_only=args.public_only,
        include_dm=not args.no_dm,
        anonymize=args.anonymize,
    )

    # 終了メッセージ
    if success:
        logger.info("処理が正常に完了しました")
    else:
        logger.error("処理中にエラーが発生しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
