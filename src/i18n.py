#!/usr/bin/env python3
"""
国際化（i18n）モジュール

Slack to Bookmarkの多言語対応を実現するためのモジュールです。
言語リソースファイル（JSON）からメッセージを読み込み、翻訳を提供します。
"""

import os
import json
import locale
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("slack_to_bookmark")


class I18n:
    """多言語対応（国際化）クラス

    このクラスは言語リソースの読み込みと翻訳の取得を担当します。
    指定された言語または環境のデフォルト言語に基づいてメッセージを提供します。
    """

    def __init__(self, lang: Optional[str] = None):
        """
        I18nクラスの初期化

        Args:
            lang: 使用する言語コード（例: 'en', 'ja'）。指定しない場合はシステムのデフォルトを使用
        """
        self.messages: Dict[str, Any] = {}
        self.lang = lang or self._detect_language()
        self.load_messages()

    def _detect_language(self) -> str:
        """
        システムのデフォルト言語を検出

        Returns:
            str: 言語コード（'en'または'ja'）。不明な場合は'en'をデフォルトとする
        """
        try:
            system_lang, _ = locale.getdefaultlocale()
            if system_lang and system_lang.startswith("ja"):
                return "ja"
            return "en"  # デフォルトは英語
        except Exception as e:
            logger.warning(f"言語検出エラー: {e}、デフォルト(en)を使用します")
            return "en"

    def load_messages(self) -> None:
        """
        指定された言語のメッセージリソースを読み込む

        言語リソースファイル (locales/{lang}/messages.json) からメッセージを読み込みます。
        ファイルが存在しない場合はデフォルト言語（英語）にフォールバックします。
        """
        base_dir = os.path.abspath(os.path.dirname(__file__))
        messages_path = os.path.join(base_dir, "locales", self.lang, "messages.json")

        try:
            with open(messages_path, "r", encoding="utf-8") as f:
                self.messages = json.load(f)
            logger.debug(f"言語リソース読み込み: {self.lang}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"{self.lang}の言語リソース読み込みエラー: {e}")

            # デフォルト言語（英語）にフォールバック
            if self.lang != "en":
                self.lang = "en"
                self.load_messages()
            else:
                logger.error("デフォルト言語リソースの読み込みに失敗しました")
                self.messages = {}

    def get(self, key: str, default: str = "") -> str:
        """
        指定されたキーに対応するメッセージを取得

        キーはドット表記で指定します（例: 'error_messages.no_token'）

        Args:
            key: メッセージのキー（ドット区切り）
            default: キーが見つからない場合のデフォルト値

        Returns:
            str: 指定されたキーに対応するメッセージ。キーが見つからない場合はデフォルト値
        """
        parts = key.split(".")
        current = self.messages

        try:
            for part in parts:
                current = current[part]

            if isinstance(current, str):
                return current
            else:
                logger.warning(f"キー '{key}' の値が文字列ではありません")
                return default
        except (KeyError, TypeError):
            logger.debug(f"キー '{key}' が見つかりません")
            return default

    def format(self, key: str, **kwargs) -> str:
        """
        指定されたキーに対応するメッセージを取得し、変数を置換

        Args:
            key: メッセージのキー（ドット区切り）
            **kwargs: 置換する変数とその値

        Returns:
            str: 変数が置換されたメッセージ
        """
        message = self.get(key)
        try:
            return message.format(**kwargs)
        except KeyError as e:
            logger.warning(f"メッセージ形式エラー: {e}")
            return message


# グローバルインスタンス
_instance = None


def get_i18n(lang: Optional[str] = None) -> I18n:
    """
    I18nのシングルトンインスタンスを取得

    Args:
        lang: 使用する言語コード（省略可）

    Returns:
        I18n: I18nクラスのインスタンス
    """
    global _instance
    if _instance is None or (lang is not None and lang != _instance.lang):
        _instance = I18n(lang)
    return _instance


def t(key: str, default: str = "", **kwargs) -> str:
    """
    指定されたキーの翻訳を取得する簡易関数

    Args:
        key: メッセージのキー（ドット区切り）
        default: キーが見つからない場合のデフォルト値
        **kwargs: 置換する変数とその値

    Returns:
        str: 翻訳されたメッセージ
    """
    i18n = get_i18n()
    message = i18n.get(key, default)

    if kwargs:
        try:
            return message.format(**kwargs)
        except KeyError:
            return message

    return message
