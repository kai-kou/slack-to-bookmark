#!/usr/bin/env python3
"""
Slack Client Module - Slack APIとの通信を担当するモジュール

このモジュールはSlack APIとの通信を行い、チャンネルやユーザー情報を取得します。
すべてのAPIリクエストはページネーション対応で、大規模なワークスペースでも
すべての情報を取得できます。
"""

import logging
from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ロギング設定
logger = logging.getLogger("slack_to_bookmark")

class SlackClient:
    """Slack APIとの通信を担当するクラス
    
    このクラスはSlack APIとの通信を行い、チャンネルやユーザー情報を取得します。
    すべてのAPIリクエストはページネーション対応で、大規模なワークスペースでも
    すべての情報を取得できます。
    """
    
    def __init__(self, token: str, workspace_name: str, workspace_id: str):
        """
        SlackClientの初期化
        
        Args:
            token: Slack API トークン (xoxp-で始まるユーザートークン)
            workspace_name: ワークスペース名 (例: 'mycompany')
            workspace_id: ワークスペースID (例: 'T00000000')
            
        Raises:
            ValueError: トークンが空の場合
        """
        if not token:
            raise ValueError("Slack APIトークンが指定されていません")
        self.client = WebClient(token=token)
        self.workspace_name = workspace_name
        self.workspace_id = workspace_id
        logger.info(f"SlackClient initialized for workspace: {workspace_name}")
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        ワークスペース内の全ユーザーを取得（ボットユーザーを除く、ページネーション対応）
        
        ワークスペース内のすべての一般ユーザー（人間）の情報を取得します。
        ボットユーザーや削除されたユーザーは除外されます。
        大規模なワークスペースでも完全なリストを取得するため、
        ページネーション処理を実装しています。
        
        Returns:
            List[Dict[str, Any]]: ユーザー情報のリスト（表示名でソート済み）
            
        Raises:
            SlackApiError: Slack APIからエラーレスポンスが返された場合
        """
        all_users = []
        regular_user_count = 0
        
        try:
            cursor = None
            while True:
                result = self.client.users_list(
                    limit=1000,
                    cursor=cursor
                )
                
                # 通常ユーザーのみをフィルタリング (is_bot=False, deleted=False)
                users = result["members"]
                regular_users = [user for user in users if not user.get("is_bot", False) and not user.get("deleted", False)]
                
                all_users.extend(regular_users)
                regular_user_count += len(regular_users)
                
                # 次のページがあるかチェック
                cursor = result.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break
            
            logger.info(f"Retrieved {regular_user_count} regular users")
        except SlackApiError as e:
            logger.error(f"ユーザーリスト取得エラー: {e}")
            if "not_allowed_token_type" in str(e):
                logger.error("トークンに必要な権限がありません。"
                            "User token (xoxp-で始まる) を使用していることを確認してください。Bot token (xoxb-) では動作しません。"
                            "\n解決策: Slack API管理画面 (https://api.slack.com/apps) で新しいユーザートークンを取得してください。")
            elif "invalid_auth" in str(e):
                logger.error("認証に失敗しました。トークンが有効で期限切れでないことを確認してください。"
                            "\n解決策: Slack API管理画面で新しいトークンを生成するか、アプリを再インストールしてください。")
            elif "missing_scope" in str(e):
                logger.error("トークンに必要なスコープがありません。トークンに 'users:read' スコープが含まれていることを確認してください。"
                            "\n解決策: Slack API管理画面の「OAuth & Permissions」ページで権限を追加し、アプリを再インストールしてください。")
            else:
                logger.error("APIエラーが発生しました。以下を確認してください:"
                            "\n- インターネット接続が安定していること"
                            "\n- Slackサーバーが正常に動作していること"
                            "\n- .envファイルの設定が正しいこと")
        
        # ユーザーをアルファベット順にソート（表示名または実名を使用）
        all_users.sort(key=lambda x: (x.get("profile", {}).get("display_name") or 
                                      x.get("profile", {}).get("real_name") or "").lower())
        
        return all_users
    
    def get_channels_by_type(self, channel_type: str) -> List[Dict[str, Any]]:
        """
        指定されたタイプのチャンネルを取得する（ページネーション対応）
        
        Slack APIを使用して、指定されたタイプ（公開またはプライベート）の
        チャンネル情報をすべて取得します。大規模なワークスペースでも
        すべてのチャンネルを取得するため、ページネーション処理を実装しています。
        
        Args:
            channel_type: チャンネルタイプ ("public_channel" または "private_channel")
            
        Returns:
            List[Dict[str, Any]]: チャンネル情報のリスト
            
        Raises:
            SlackApiError: Slack APIからエラーレスポンスが返された場合
            ValueError: 不正なチャンネルタイプが指定された場合
        """
        # チャンネルタイプの検証
        if channel_type not in ["public_channel", "private_channel"]:
            raise ValueError("チャンネルタイプは 'public_channel' または 'private_channel' である必要があります")
        channels = []
        channel_count = 0
        type_display = "公開" if channel_type == "public_channel" else "プライベート"
        
        try:
            cursor = None
            while True:
                result = self.client.conversations_list(
                    types=channel_type,
                    limit=1000,
                    cursor=cursor
                )
                
                new_channels = result["channels"]
                channels.extend(new_channels)
                channel_count += len(new_channels)
                
                # 次のページがあるかチェック
                cursor = result.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break
            
            logger.info(f"{type_display}チャンネル: {channel_count}個")
        except SlackApiError as e:
            error_msg = f"{type_display}チャンネル取得エラー: {e}"
            if channel_type == "private_channel" and "not_allowed_token_type" in str(e):
                error_msg += "\n権限が不足しています。User token (xoxp-) が必要です。Bot token (xoxb-) では動作しません。"
                error_msg += "\n解決策: Slack API管理画面 (https://api.slack.com/apps) で新しいユーザートークンを取得してください。"
            elif "missing_scope" in str(e):
                if channel_type == "public_channel":
                    error_msg += "\nトークンに 'channels:read' スコープが必要です。"
                else:
                    error_msg += "\nトークンに 'groups:read' スコープが必要です。"
                error_msg += "\n解決策: Slack API管理画面の「OAuth & Permissions」ページで権限を追加し、アプリを再インストールしてください。"
            logger.error(error_msg)
        
        return channels
    
    def get_all_channels(self) -> List[Dict[str, Any]]:
        """
        公開チャンネルとプライベートチャンネルを取得 (ページネーション対応)
        
        ワークスペース内のすべての公開チャンネルとプライベートチャンネルを
        取得します。この操作には users:read と groups:read の権限が必要です。
        
        Returns:
            List[Dict[str, Any]]: すべてのチャンネル情報のリスト
            
        Raises:
            SlackApiError: Slack APIからエラーレスポンスが返された場合
        """
        # 公開チャンネルを取得
        public_channels = self.get_channels_by_type("public_channel")
        
        # プライベートチャンネルを取得
        private_channels = self.get_channels_by_type("private_channel")
        
        # 両方を結合
        all_channels = public_channels + private_channels
        
        return all_channels
    
    def get_public_channels(self) -> List[Dict[str, Any]]:
        """
        公開チャンネルのみを取得
        
        ワークスペース内の公開チャンネルのみを取得します。
        プライベートチャンネルは含まれません。
        この操作には channels:read 権限が必要です。
        
        Returns:
            List[Dict[str, Any]]: 公開チャンネル情報のリスト
            
        Raises:
            SlackApiError: Slack APIからエラーレスポンスが返された場合
        """
        logger.info("パブリックチャンネルのみのリストを取得します...")
        return self.get_channels_by_type("public_channel")
