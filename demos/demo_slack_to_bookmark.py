#!/usr/bin/env python3
"""
Slack to Bookmark - デモバージョン

有効なSlackトークンがなくても機能をテストするためのデモスクリプトです。
APIレスポンスをモックして、HTMLブックマークファイルの生成を行います。
"""

import os
import sys
import platform
import datetime
import time
import logging
import webbrowser
from typing import List, Dict, Any

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("demo_slack_to_bookmark")

class BookmarkGenerator:
    def __init__(self, workspace_name: str, workspace_id: str):
        self.workspace_name = workspace_name
        self.workspace_id = workspace_id
        self.timestamp = str(int(datetime.datetime.now().timestamp()))
        logger.info("BookmarkGenerator initialized")
    
    def generate_channel_bookmarks(self, channels: List[Dict[str, Any]], output_file: str) -> str:
        # 標準的なNetscape Bookmark File Format
        html = f'''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="{self.timestamp}" LAST_MODIFIED="{self.timestamp}">Slack</H3>
    <DL><p>
'''
        
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
        
        html += '''    </DL><p>
</DL><p>
'''
        
        # ファイルに保存
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"ブックマークファイルを生成しました: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"ブックマークファイル生成エラー: {e}")
            return ""
    
    def generate_user_dm_bookmarks(self, users: List[Dict[str, Any]], output_file: str) -> str:
        # 標準的なNetscape Bookmark File Format
        html = f'''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="{self.timestamp}" LAST_MODIFIED="{self.timestamp}">Slack Users</H3>
    <DL><p>
'''
        
        # ユーザーのDMリンクを追加
        for user in users:
            user_id = user["id"]
            real_name = user.get("real_name", "")
            display_name = user.get("display_name", "")
            
            # 表示名がない場合は実名を使用
            if not display_name:
                display_name = real_name
            
            # 表示形式: 実名 (@表示名)
            bookmark_name = f"{real_name} (@{display_name})" if display_name != real_name else real_name
            
            # Slackアプリが直接開くURL形式
            url = f"slack://user?team={self.workspace_id}&id={user_id}"
            
            # ブックマークエントリを追加
            html += f'            <DT><A HREF="{url}" ADD_DATE="{self.timestamp}">{bookmark_name}</A>\n'
        
        html += '''    </DL><p>
</DL><p>
'''
        
        # ファイルに保存
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"ユーザーDMのブックマークファイルを生成しました: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"ユーザーDMブックマークファイル生成エラー: {e}")
            return ""

class GuideGenerator:
    def __init__(self):
        self.is_mac = platform.system() == "Darwin"
        self.is_windows = platform.system() == "Windows"
        logger.info(f"GuideGenerator initialized for {platform.system()}")
    
    def create_guide(self, html_file_path: str, output_file: str, is_public_only: bool = False, is_user_dm: bool = False) -> str:
        # タイトル設定
        if is_user_dm:
            title = "Slackユーザー DMブックマークインポート手順"
        else:
            title = "Slackパブリックチャンネル ブックマークインポート手順" if is_public_only else "Slackチャンネル ブックマークインポート手順"
        
        # 注意書きの内容
        if is_user_dm:
            note_content = "インポート後、「Slack Users」フォルダにユーザーDMのブックマークが追加されます。"
        else:
            note_content = "インポート後、「Slack」フォルダに全チャンネルが追加されます。"
        
        # キーボードショートカット（OS別）
        shortcut = "Ctrl+Shift+O" if self.is_windows else "Cmd+Option+B"
        
        # HTMLコードを生成
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h1 {{ color: #1264A3; }}
        .steps {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .step {{ margin: 10px 0; }}
        .file-path {{ background: #eee; padding: 5px; font-family: monospace; word-break: break-all; border-radius: 3px; }}
        .note {{ background: #fffde7; padding: 10px; margin-top: 20px; border-radius: 5px; }}
        button {{ background: #1264A3; color: white; border: none; padding: 8px 16px; 
                 margin-top: 20px; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background: #0b4f85; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    
    <div class="steps">
        <div class="step">1. Chromeでブックマークマネージャーを開く: <strong>{shortcut}</strong></div>
        <div class="step">2. 右上の「...」をクリックし、「ブックマークをインポート」を選択</div>
        <div class="step">3. 「HTMLファイルから」を選択し、ファイルを選択する</div>
        <div class="step">4. 以下のファイルを選択:</div>
        <div class="file-path">{html_file_path}</div>
        <div class="step">5. 「開く」をクリックしてインポート</div>
    </div>
    
    <div class="note">
        <p><strong>注意:</strong> {note_content}</p>
        <p>インポートに問題がある場合は、一度Chromeを再起動してから再度インポートを試みてください。</p>
    </div>
    
    <button onclick="window.open('chrome://bookmarks/')">ブックマークマネージャーを開く</button>
</body>
</html>
'''
        
        # ファイルに保存
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"ガイドページを生成しました: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"ガイドページ生成エラー: {e}")
            return ""

def main():
    """デモの実行"""
    # 設定
    workspace_name = "demo-workspace"
    workspace_id = "T00000000"
    
    # デモ用のモックデータを作成
    mock_channels = [
        {"id": "C01", "name": "general", "is_private": False},
        {"id": "C02", "name": "random", "is_private": False},
        {"id": "C03", "name": "project-x", "is_private": False},
        {"id": "C04", "name": "team-dev", "is_private": True},
        {"id": "C05", "name": "secret-project", "is_private": True},
    ]
    
    mock_users = [
        {"id": "U01", "real_name": "田中 太郎", "display_name": "tanaka"},
        {"id": "U02", "real_name": "佐藤 花子", "display_name": "sato-hanako"},
        {"id": "U03", "real_name": "鈴木 一郎", "display_name": "suzuki"},
        {"id": "U04", "real_name": "John Smith", "display_name": "john"},
        {"id": "U05", "real_name": "Mike Johnson", "display_name": "mike"},
    ]
    
    logger.info("SlackToBookmarkデモの実行を開始します...")
    
    # ジェネレーター初期化
    bookmark_generator = BookmarkGenerator(workspace_name, workspace_id)
    guide_generator = GuideGenerator()
    
    # チャンネルブックマークの生成
    output_file = "demo_slack_channels.html"
    html_file_path = bookmark_generator.generate_channel_bookmarks(mock_channels, output_file)
    
    # ガイドページの生成
    guide_file = "demo_channel_guide.html"
    guide_path = guide_generator.create_guide(html_file_path, guide_file)
    
    # ユーザーDM用ブックマークの生成
    user_dm_output_file = "demo_slack_users.html"
    user_dm_html_file_path = bookmark_generator.generate_user_dm_bookmarks(mock_users, user_dm_output_file)
    
    # ユーザーDM用ガイドページの生成
    user_guide_file = "demo_user_guide.html"
    user_guide_path = guide_generator.create_guide(user_dm_html_file_path, user_guide_file, is_user_dm=True)
    
    # ブラウザでガイドページを開く（任意）
    try:
        guide_abs_path = os.path.abspath(user_guide_path)
        webbrowser.open(f"file://{guide_abs_path}")
        logger.info("ユーザーDMガイドページを開きました")
    except Exception as e:
        logger.error(f"ブラウザでファイルを開く際にエラーが発生しました: {e}")
    
    logger.info("デモ処理が完了しました。以下のファイルが生成されました:")
    logger.info(f"チャンネルブックマーク: {output_file}")
    logger.info(f"チャンネルガイド: {guide_file}")
    logger.info(f"ユーザーDMブックマーク: {user_dm_output_file}")
    logger.info(f"ユーザーDMガイド: {user_guide_file}")

if __name__ == "__main__":
    main()
