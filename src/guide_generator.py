#!/usr/bin/env python3
"""
Guide Generator Module - ブックマークインポート手順のガイドページ生成を担当するモジュール

このモジュールは、生成されたブックマークファイルをChromeブラウザに
インポートする手順を説明するHTMLガイドページを生成します。
ユーザーのOS（WindowsまたはMac）を自動検出し、適切なショートカットキーを
表示します。
"""

import platform
import logging

# ロギング設定
logger = logging.getLogger("slack_to_bookmark")


class GuideGenerator:
    """ブックマークインポート手順のガイドページ生成を担当するクラス

    このクラスは、生成されたブックマークファイルをChromeブラウザに
    インポートする手順を説明するHTMLガイドページを生成します。
    ユーザーのOS（WindowsまたはMac）を自動検出し、適切なショートカットキーを
    表示します。
    """

    def __init__(self):
        """
        GuideGeneratorの初期化

        ユーザーの実行環境（OS）を自動検出し、適切なキーボードショートカットなどを
        設定します。
        """
        self.is_mac = platform.system() == "Darwin"
        self.is_windows = platform.system() == "Windows"
        logger.info(f"GuideGenerator initialized for {platform.system()}")

    def create_guide(
        self,
        html_file_path: str,
        output_file: str,
        is_public_only: bool = False,
        is_user_dm: bool = False,
    ) -> str:
        """
        ブックマークインポート手順ページを生成

        生成されたブックマークファイルをChromeブラウザにインポートする手順を
        説明するHTMLガイドページを生成します。ブックマークの種類（全チャンネル、
        公開チャンネルのみ、ユーザーDM）に応じて内容を調整します。

        Args:
            html_file_path: 参照するHTMLファイルのパス
            output_file: 出力ファイル名（例: 'bookmark_guide.html'）
            is_public_only: Trueの場合、公開チャンネルのみのガイドを生成
            is_user_dm: Trueの場合、ユーザーDM用のガイドを生成

        Returns:
            str: 生成されたガイドファイルのパス、エラー時は空文字列

        Raises:
            IOError: ファイル書き込みに失敗した場合
        """
        # タイトル設定
        if is_user_dm:
            title = "Slackユーザー DMブックマークインポート手順"
        else:
            title = (
                "Slackパブリックチャンネル ブックマークインポート手順"
                if is_public_only
                else "Slackチャンネル ブックマークインポート手順"
            )

        # 注意書きの内容
        if is_user_dm:
            note_content = "インポート後、「Slack Users」フォルダにユーザーDMのブックマークが追加されます。"
        else:
            note_content = (
                "インポート後、「Slack」フォルダに全チャンネルが追加されます。"
            )

        # キーボードショートカット（OS別）
        shortcut = "Ctrl+Shift+O" if self.is_windows else "Cmd+Option+B"

        # HTMLコードを生成
        html = f"""<!DOCTYPE html>
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
"""

        # ファイルに保存
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"ガイドページを生成しました: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"ガイドページ生成エラー: {e}")
            return ""
