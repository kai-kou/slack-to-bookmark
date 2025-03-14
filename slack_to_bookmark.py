"""
Slack to Bookmark - SlackチャンネルとDMリンクをChromeブックマークに変換するツール

このモジュールは、src/slack_to_bookmark.py モジュールからクラスをインポートし、
後方互換性のために再エクスポートします。
"""

# Import directly from the module files to avoid package name references
from src.slack_client import SlackClient
from src.bookmark_generator import BookmarkGenerator
from src.guide_generator import GuideGenerator
from src.slack_to_bookmark import (
    SlackToBookmark,
    main,
    create_parser,
    __version__
)

if __name__ == "__main__":
    main()
