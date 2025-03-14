#!/usr/bin/env python3
"""
Bookmark Generator Module - ブックマークファイル生成を担当するモジュール

このモジュールはSlackのチャンネルとユーザー情報をHTML形式のブックマーク
ファイルに変換する処理を担当します。Chrome/Edgeブラウザでインポート可能な
標準的なNetscape Bookmark File Format形式で出力します。
"""

import datetime
import logging
from typing import List, Dict, Any

# ロギング設定
logger = logging.getLogger("slack_to_bookmark")


class BookmarkGenerator:
    """ブックマークファイル生成を担当するクラス

    このクラスはSlackのチャンネルとユーザー情報をHTML形式のブックマーク
    ファイルに変換する処理を担当します。Chrome/Edgeブラウザでインポート可能な
    標準的なNetscape Bookmark File Format形式で出力します。
    """

    def __init__(self, workspace_name: str, workspace_id: str):
        """
        BookmarkGeneratorの初期化

        Args:
            workspace_name: Slackワークスペース名（例: 'mycompany'）
            workspace_id: SlackワークスペースID（例: 'T00000000'）

        Note:
            タイムスタンプは現在時刻から自動生成されます
        """
        self.workspace_name = workspace_name
        self.workspace_id = workspace_id
        self.timestamp = str(int(datetime.datetime.now().timestamp()))
        logger.info("BookmarkGenerator initialized")

    def generate_channel_bookmarks(
        self, channels: List[Dict[str, Any]], output_file: str
    ) -> str:
        """
        チャンネル用のHTML形式ブックマークファイルを生成

        チャンネル情報のリストを受け取り、Chrome/Edgeでインポート可能な
        HTML形式のブックマークファイルを生成します。
        チャンネルはアルファベット順にソートされ、プライベートチャンネルには
        🔒 マークが付きます。

        Args:
            channels: Slack APIから取得したチャンネル情報のリスト
            output_file: 出力ファイル名（例: 'slack_bookmarks.html'）

        Returns:
            str: 生成されたファイルのパス、エラー時は空文字列

        Raises:
            IOError: ファイル書き込みに失敗した場合
        """
        # 標準的なNetscape Bookmark File Format
        html = f"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="{self.timestamp}" LAST_MODIFIED="{self.timestamp}">Slack</H3>
    <DL><p>
"""

        # チャンネルをアルファベット順に並べ替え
        channels.sort(key=lambda x: x["name"].lower())

        # すべてのチャンネルを追加
        for channel in channels:
            channel_name = channel["name"]
            channel_id = channel["id"]
            is_private = channel.get("is_private", False)

            # Slackアプリが直接開くURL形式
            url = f"slack://channel?team={self.workspace_id}&id={channel_id}"

            # プライベートチャンネルには 🔒 マークを付ける
            display_name = f"🔒 #{channel_name}" if is_private else f"#{channel_name}"

            # ブックマークエントリを追加
            html += f'            <DT><A HREF="{url}" ADD_DATE="{self.timestamp}">{display_name}</A>\n'

        html += """    </DL><p>
</DL><p>
"""

        # ファイルに保存
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"ブックマークファイルを生成しました: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"ブックマークファイル生成エラー: {e}")
            return ""

    def generate_user_dm_bookmarks(
        self, users: List[Dict[str, Any]], output_file: str
    ) -> str:
        """
        ユーザーDM用のHTML形式ブックマークファイルを生成

        ユーザー情報のリストを受け取り、Chrome/Edgeでインポート可能な
        HTML形式のブックマークファイルを生成します。
        各ユーザーの表示形式は「実名 (@表示名)」となります。
        表示名が実名と同じ場合は、実名のみが表示されます。

        Args:
            users: Slack APIから取得したユーザー情報のリスト
            output_file: 出力ファイル名（例: 'slack_user_dms.html'）

        Returns:
            str: 生成されたファイルのパス、エラー時は空文字列

        Raises:
            IOError: ファイル書き込みに失敗した場合
        """
        # 標準的なNetscape Bookmark File Format
        html = f"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="{self.timestamp}" LAST_MODIFIED="{self.timestamp}">Slack Users</H3>
    <DL><p>
"""

        # ユーザーのDMリンクを追加
        for user in users:
            user_id = user["id"]
            real_name = user.get("profile", {}).get("real_name", "")
            display_name = user.get("profile", {}).get("display_name", "")

            # 表示名がない場合は実名を使用
            if not display_name:
                display_name = real_name

            # 表示形式: 実名 (@表示名)
            bookmark_name = (
                f"{real_name} (@{display_name})"
                if display_name != real_name
                else real_name
            )

            # Slackアプリが直接開くURL形式
            url = f"slack://user?team={self.workspace_id}&id={user_id}"

            # ブックマークエントリを追加
            html += f'            <DT><A HREF="{url}" ADD_DATE="{self.timestamp}">{bookmark_name}</A>\n'

        html += """    </DL><p>
</DL><p>
"""

        # ファイルに保存
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(
                f"ユーザーDMのブックマークファイルを生成しました: {output_file}"
            )
            return output_file
        except Exception as e:
            logger.error(f"ユーザーDMブックマークファイル生成エラー: {e}")
            return ""
