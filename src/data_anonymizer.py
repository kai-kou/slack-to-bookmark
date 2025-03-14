#!/usr/bin/env python3
"""
Data Anonymizer Module - 生成されたファイル内の機密情報を匿名化するモジュール

このモジュールは、Slack to Bookmarkによって生成されたHTMLファイル内の
企業名、個人名、ワークスペースIDなどの機密情報を検出し、
自動的に匿名化（ダミーデータに置換）する機能を提供します。
"""

import os
import re
import random
import string
import sys
import logging
from typing import Dict, List, Tuple, Set, Optional
from pathlib import Path
import json

# ロギング設定
logger = logging.getLogger("slack_to_bookmark")

class DataAnonymizer:
    """生成ファイル内の機密情報を匿名化するクラス
    
    このクラスは、生成されたHTMLファイル内の機密情報（企業名、個人名、
    ワークスペースIDなど）を検出し、自動的に匿名化（ダミーデータに置換）します。
    一貫性を保つため、同じ情報は常に同じダミーデータに置換されます。
    """
    
    def __init__(self):
        """
        DataAnonymizerの初期化
        
        内部的なマッピングテーブルを初期化し、検出・置換パターンを設定します。
        """
        # マッピングデータを保持する辞書
        self.workspace_id_map = {}  # ワークスペースID のマッピング
        self.user_id_map = {}       # ユーザーID のマッピング
        self.channel_id_map = {}    # チャンネルID のマッピング
        self.name_map = {}          # 個人名のマッピング
        self.company_map = {}       # 企業名のマッピング
        
        # 英語名と日本語名の姓名サンプル（ダミーデータ用）
        self.first_names_en = ["John", "Emma", "Michael", "Olivia", "William", "Sophia", "James", "Ava", "Robert", "Mia"]
        self.last_names_en = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Anderson", "Taylor"]
        self.first_names_jp = ["太郎", "花子", "一郎", "美咲", "健太", "さくら", "大輔", "恵子", "裕子", "直樹"]
        self.last_names_jp = ["佐藤", "鈴木", "田中", "高橋", "伊藤", "渡辺", "山本", "中村", "小林", "加藤"]
        
        # 企業名サンプル（ダミーデータ用）
        self.company_names = ["サンプル株式会社", "テスト産業", "デモテクノロジー", "サンプルコーポレーション", 
                              "ABC商事", "XYZ工業", "架空電機", "モデル物産", "サンプルフーズ", "テストメディア"]
        
        # マッピング保存先ファイル
        self.mapping_file = "anonymizer_mappings.json"
        
        # 既存のマッピングがあれば読み込む
        self._load_mappings()
        
        logger.info("DataAnonymizer initialized")
    
    def _load_mappings(self) -> None:
        """
        既存のマッピングファイルがあれば読み込む
        """
        if os.path.exists(self.mapping_file):
            try:
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    mappings = json.load(f)
                    self.workspace_id_map = mappings.get("workspace_id_map", {})
                    self.user_id_map = mappings.get("user_id_map", {})
                    self.channel_id_map = mappings.get("channel_id_map", {})
                    self.name_map = mappings.get("name_map", {})
                    self.company_map = mappings.get("company_map", {})
                    logger.info(f"既存のマッピング情報を読み込みました: {len(self.name_map)}個の名前, {len(self.company_map)}個の企業名")
            except Exception as e:
                logger.error(f"マッピングファイルの読み込み中にエラーが発生しました: {e}")
    
    def _save_mappings(self) -> None:
        """
        現在のマッピングをファイルに保存
        """
        try:
            mappings = {
                "workspace_id_map": self.workspace_id_map,
                "user_id_map": self.user_id_map,
                "channel_id_map": self.channel_id_map,
                "name_map": self.name_map,
                "company_map": self.company_map
            }
            with open(self.mapping_file, 'w', encoding='utf-8') as f:
                json.dump(mappings, f, ensure_ascii=False, indent=2)
            logger.info(f"マッピング情報を保存しました: {self.mapping_file}")
        except Exception as e:
            logger.error(f"マッピング情報の保存中にエラーが発生しました: {e}")
    
    def _generate_dummy_workspace_id(self) -> str:
        """
        ダミーのワークスペースIDを生成
        形式: T + 9文字の英数字

        Returns:
            str: ダミーのワークスペースID
        """
        return "T" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    def _generate_dummy_user_id(self) -> str:
        """
        ダミーのユーザーIDを生成
        形式: U + 9文字の英数字

        Returns:
            str: ダミーのユーザーID
        """
        return "U" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    def _generate_dummy_channel_id(self) -> str:
        """
        ダミーのチャンネルIDを生成
        形式: C + 9文字の英数字

        Returns:
            str: ダミーのチャンネルID
        """
        return "C" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    
    def _generate_dummy_name(self, is_japanese: bool = True) -> str:
        """
        ダミーの人名を生成

        Args:
            is_japanese: 日本語名を生成するか (Trueなら日本語名、Falseなら英語名)

        Returns:
            str: ダミーの人名
        """
        if is_japanese:
            last_name = random.choice(self.last_names_jp)
            first_name = random.choice(self.first_names_jp)
            return f"{last_name} {first_name}"
        else:
            first_name = random.choice(self.first_names_en)
            last_name = random.choice(self.last_names_en)
            return f"{first_name} {last_name}"
    
    def _generate_dummy_company_name(self) -> str:
        """
        ダミーの企業名を生成

        Returns:
            str: ダミーの企業名
        """
        return random.choice(self.company_names)
    
    def _anonymize_workspace_id(self, content: str) -> str:
        """
        ワークスペースIDを匿名化

        Args:
            content: 処理対象の文字列

        Returns:
            str: ワークスペースIDが匿名化された文字列
        """
        # ワークスペースIDのパターン: team=T[A-Z0-9]{8,10}
        pattern = r'team=(T[A-Z0-9]{8,10})'
        
        def replace_workspace_id(match):
            workspace_id = match.group(1)
            if workspace_id not in self.workspace_id_map:
                self.workspace_id_map[workspace_id] = self._generate_dummy_workspace_id()
            return f'team={self.workspace_id_map[workspace_id]}'
        
        return re.sub(pattern, replace_workspace_id, content)
    
    def _anonymize_ids(self, content: str) -> str:
        """
        ユーザーIDとチャンネルIDを匿名化

        Args:
            content: 処理対象の文字列

        Returns:
            str: ユーザーIDとチャンネルIDが匿名化された文字列
        """
        # ユーザーIDのパターン: id=U[A-Z0-9]{8,10}
        user_pattern = r'user\?team=[^&]+&id=(U[A-Z0-9]+)'
        
        def replace_user_id(match):
            user_id = match.group(1)
            if user_id not in self.user_id_map:
                self.user_id_map[user_id] = self._generate_dummy_user_id()
            return f'user?team={next(iter(self.workspace_id_map.values()))}&id={self.user_id_map[user_id]}'
        
        # チャンネルIDのパターン: id=C[A-Z0-9]{8,10}
        channel_pattern = r'channel\?team=[^&]+&id=(C[A-Z0-9]+)'
        
        def replace_channel_id(match):
            channel_id = match.group(1)
            if channel_id not in self.channel_id_map:
                self.channel_id_map[channel_id] = self._generate_dummy_channel_id()
            return f'channel?team={next(iter(self.workspace_id_map.values()))}&id={self.channel_id_map[channel_id]}'
        
        content = re.sub(user_pattern, replace_user_id, content)
        content = re.sub(channel_pattern, replace_channel_id, content)
        return content
    
    def _anonymize_names(self, content: str) -> str:
        """
        個人名を匿名化

        Args:
            content: 処理対象の文字列

        Returns:
            str: 個人名が匿名化された文字列
        """
        # 日本語名のパターン: 漢字またはひらがな/カタカナの連続（括弧内も含む）
        jp_name_pattern = r'>([一-龯ぁ-んァ-ヶ々ー]+\s+[一-龯ぁ-んァ-ヶ々ー]+)(\s+\([^)]+\))?(\s+\(@[^)]+\))?<'
        # 英語名のパターン
        en_name_pattern = r'>([A-Z][a-z]+\s+[A-Z][a-z]+)<'
        
        def replace_jp_name(match):
            full_name = match.group(1)
            parenthesis = match.group(2) if match.group(2) else ""
            display_name = match.group(3) if match.group(3) else ""
            
            if full_name not in self.name_map:
                self.name_map[full_name] = self._generate_dummy_name(is_japanese=True)
            
            # 括弧内の名前も置換が必要な場合は追加処理
            if parenthesis:
                # 括弧内の名前を抽出して置換
                paren_content = parenthesis[2:-1]  # 括弧と空白を除去
                if paren_content not in self.name_map:
                    # 英語名っぽければ英語名のダミーを生成
                    if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+', paren_content):
                        self.name_map[paren_content] = self._generate_dummy_name(is_japanese=False)
                    else:
                        self.name_map[paren_content] = self._generate_dummy_name(is_japanese=True)
                parenthesis = f" ({self.name_map[paren_content]})"
            
            # 表示名の処理
            if display_name:
                display_name_content = display_name[4:-1]  # 「 (@」と「)」を除去
                if display_name_content not in self.name_map:
                    # 表示名をダミーに置換
                    if ")" in display_name_content:  # 休み情報などが括弧内にある場合
                        parts = display_name_content.split("(")
                        base_name = parts[0].strip()
                        rest = "(" + "(".join(parts[1:])
                        if base_name not in self.name_map:
                            self.name_map[base_name] = f"display_{len(self.name_map)}"
                        display_name = f" (@{self.name_map[base_name]}{rest})"
                    else:
                        self.name_map[display_name_content] = f"display_{len(self.name_map)}"
                        display_name = f" (@{self.name_map[display_name_content]})"
            
            return f'>{self.name_map[full_name]}{parenthesis}{display_name}<'
        
        def replace_en_name(match):
            full_name = match.group(1)
            if full_name not in self.name_map:
                self.name_map[full_name] = self._generate_dummy_name(is_japanese=False)
            return f'>{self.name_map[full_name]}<'
        
        content = re.sub(jp_name_pattern, replace_jp_name, content)
        content = re.sub(en_name_pattern, replace_en_name, content)
        return content
    
    def _anonymize_companies(self, content: str) -> str:
        """
        企業名を匿名化

        Args:
            content: 処理対象の文字列

        Returns:
            str: 企業名が匿名化された文字列
        """
        # 企業名のパターン: 〇〇株式会社、〇〇工業、など
        company_patterns = [
            r'([^\s<>]+株式会社)',
            r'([^\s<>]+興業)',
            r'([^\s<>]+工業)',
            r'([^\s<>]+商事)',
            r'([^\s<>]+産業)',
            r'(株式会社[^\s<>]+)'
        ]
        
        for pattern in company_patterns:
            def replace_company(match):
                company_name = match.group(1)
                if company_name not in self.company_map:
                    self.company_map[company_name] = self._generate_dummy_company_name()
                return self.company_map[company_name]
            
            content = re.sub(pattern, replace_company, content)
        
        return content
    
    def _anonymize_channel_names(self, content: str) -> str:
        """
        チャンネル名を匿名化

        Args:
            content: 処理対象の文字列

        Returns:
            str: チャンネル名が匿名化された文字列
        """
        # チャンネル名のパターン: >#project-name や >🔒 #private-channel など
        channel_pattern = r'>(\🔒 )?#([^<]+)<'
        
        def replace_channel_name(match):
            lock = match.group(1) if match.group(1) else ""
            channel_name = match.group(2)
            
            # 企業名などが含まれるチャンネル名は特別処理
            # まず企業名を検出して置換
            for company, dummy in self.company_map.items():
                if company in channel_name:
                    channel_name = channel_name.replace(company, dummy)
            
            # チャンネル名パターンとして保存
            channel_parts = channel_name.split('-')
            if len(channel_parts) > 1:
                # プレフィックスは保持して残りを匿名化
                prefix = channel_parts[0]
                if prefix not in ["general", "random", "announce"]:
                    prefix = f"category{hash(prefix) % 10}"
                channel_name = f"{prefix}-project{hash(channel_name) % 100}"
            else:
                channel_name = f"channel{hash(channel_name) % 100}"
            
            return f'>{lock}#{channel_name}<'
        
        return re.sub(channel_pattern, replace_channel_name, content)
    
    def anonymize_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        ファイル内の機密情報を匿名化して保存

        Args:
            file_path: 処理対象のファイルパス
            output_path: 出力先ファイルパス（Noneの場合は元のファイルを上書き）

        Returns:
            str: 出力されたファイルのパス

        Raises:
            FileNotFoundError: 指定されたファイルが存在しない場合
            IOError: ファイル読み込み/書き込みエラーの場合
        """
        if not os.path.exists(file_path):
            err_msg = f"ファイルが見つかりません: {file_path}"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)
        
        if output_path is None:
            output_path = file_path
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 各種情報を匿名化
            content = self._anonymize_workspace_id(content)
            content = self._anonymize_ids(content)
            content = self._anonymize_names(content)
            content = self._anonymize_companies(content)
            content = self._anonymize_channel_names(content)
            
            # 結果を保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # マッピング情報を保存
            self._save_mappings()
            
            logger.info(f"ファイルを匿名化しました: {file_path} -> {output_path}")
            return output_path
        
        except Exception as e:
            err_msg = f"ファイルの匿名化中にエラーが発生しました: {e}"
            logger.error(err_msg)
            raise IOError(err_msg)
    
    def anonymize_all_html_files(self, directory: str = '.') -> List[str]:
        """
        指定ディレクトリ内のすべてのHTMLファイルを匿名化

        Args:
            directory: 処理対象のディレクトリパス

        Returns:
            List[str]: 処理されたファイルのパスリスト
        """
        processed_files = []
        
        # HTMLファイルのパターン
        html_patterns = [
            "slack_*.html",
            "*_guide.html"
        ]
        
        for pattern in html_patterns:
            for file_path in Path(directory).glob(pattern):
                try:
                    self.anonymize_file(str(file_path))
                    processed_files.append(str(file_path))
                except Exception as e:
                    logger.error(f"ファイル {file_path} の処理中にエラーが発生しました: {e}")
        
        return processed_files


def main():
    """
    コマンドラインから実行された場合のエントリーポイント
    """
    import argparse
    
    # ロギング設定
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    parser = argparse.ArgumentParser(description="生成されたHTMLファイル内の機密情報を匿名化するスクリプト")
    parser.add_argument(
        "-f", "--file",
        help="処理対象の特定ファイル（指定しない場合はすべてのHTMLファイルを処理）"
    )
    parser.add_argument(
        "-o", "--output",
        help="出力先ファイル（指定しない場合は元のファイルを上書き）"
    )
    parser.add_argument(
        "-d", "--directory",
        default=".",
        help="処理対象のディレクトリ（デフォルト: カレントディレクトリ）"
    )
    
    args = parser.parse_args()
    
    # 匿名化処理の実行
    anonymizer = DataAnonymizer()
    
    if args.file:
        # 特定のファイルを処理
        try:
            output_path = anonymizer.anonymize_file(args.file, args.output)
            print(f"ファイルを匿名化しました: {args.file} -> {output_path}")
        except Exception as e:
            print(f"エラー: {e}")
            return 1
    else:
        # ディレクトリ内のすべてのHTMLファイルを処理
        try:
            processed_files = anonymizer.anonymize_all_html_files(args.directory)
            if processed_files:
                print(f"{len(processed_files)}個のファイルを匿名化しました:")
                for file_path in processed_files:
                    print(f"- {file_path}")
            else:
                print("処理対象のファイルが見つかりませんでした")
        except Exception as e:
            print(f"エラー: {e}")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
