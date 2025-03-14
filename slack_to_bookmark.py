"""
Slack to Bookmark - SlackチャンネルとDMリンクをChromeブックマークに変換するツール

このモジュールは、src/slack_to_bookmark.py モジュールからクラスをインポートし、
後方互換性のために再エクスポートします。
"""

from src import (
    SlackClient, 
    BookmarkGenerator, 
    GuideGenerator, 
    SlackToBookmark,
    main,
    create_parser,
    __version__
)

if __name__ == "__main__":
    main()
