"""
Slack to Bookmark - SlackチャンネルとDMリンクをChromeブックマークに変換するツール

このパッケージは、SlackのチャンネルとDMリンクをChromeブックマークとして
利用できるようにするための機能を提供します。
"""

from .slack_client import SlackClient
from .bookmark_generator import BookmarkGenerator
from .guide_generator import GuideGenerator
from .slack_to_bookmark import SlackToBookmark, create_parser, main, __version__
