#!/usr/bin/env python3
"""
Slackトークンのテスト用スクリプト（詳細診断版）
"""

import os
import sys
import inspect
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import requests

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("slack_token_test")

def validate_token_format(token):
    """トークンの形式を検証"""
    if not token:
        print("❌ トークンが空です")
        return False
    
    if not token.startswith("xoxp-"):
        print(f"⚠️ トークンが xoxp- で始まっていません: {token[:5]}...")
        return False
    
    if len(token) < 20:  # 適当な長さチェック
        print(f"⚠️ トークンが短すぎます（{len(token)}文字）")
        return False
    
    print("✅ トークン形式は有効です")
    return True

def test_token_with_requests():
    """requestsライブラリを使用してトークンをテスト"""
    token = os.getenv("SLACK_TOKEN")
    if not token:
        print("エラー: SLACK_TOKENが設定されていません。")
        return False
    
    print("\n----- requests ライブラリによるテスト -----")
    try:
        url = "https://slack.com/api/auth.test"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, headers=headers)
        result = response.json()
        
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {result}")
        
        if result.get("ok"):
            print("✅ requestsによる認証テスト: 成功")
            return True
        else:
            print(f"❌ requestsによる認証テスト: 失敗 - {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ requestsによるテスト中にエラー: {e}")
        return False

def test_token_with_webclient():
    """WebClientを使用してトークンをテスト"""
    token = os.getenv("SLACK_TOKEN")
    if not token:
        print("エラー: SLACK_TOKENが設定されていません。")
        return False
    
    print("\n----- WebClient ライブラリによるテスト -----")
    print(f"トークン: {token[:10]}...（安全のため一部のみ表示）")
    
    # WebClientの初期化
    client = WebClient(token=token)
    
    try:
        # auth.testエンドポイントを使用してトークンの有効性をテスト
        response = client.auth_test()
        print("✅ WebClient認証: 成功!")
        print(f"ユーザー: {response['user']}")
        print(f"チーム: {response['team']}")
        print(f"チームID: {response['team_id']}")
        print(f"ユーザーID: {response['user_id']}")
        return True
    except SlackApiError as e:
        print(f"❌ WebClient認証エラー: {e}")
        print(f"エラーレスポンス: {e.response}")
        
        if "invalid_auth" in str(e):
            print("トークンが無効または期限切れです。")
        elif "not_allowed_token_type" in str(e):
            print("このトークンタイプでは許可されていない操作です。")
        elif "missing_scope" in str(e):
            print("トークンに必要なスコープがありません。")
        
        # エラー発生場所の詳細情報
        frame = inspect.currentframe()
        stack_trace = inspect.getframeinfo(frame)
        print(f"エラー発生場所: {stack_trace.filename}:{stack_trace.lineno}")
        
        return False

def check_env_loading():
    """環境変数の読み込みをチェック"""
    print("\n----- 環境変数の検証 -----")
    # 環境変数の読み込み前のトークン
    token_before = os.getenv("SLACK_TOKEN")
    print(f"load_dotenv()前のトークン存在: {'あり' if token_before else 'なし'}")
    
    # 環境変数を明示的に再読み込み
    load_dotenv(override=True)
    
    # 環境変数の読み込み後のトークン
    token_after = os.getenv("SLACK_TOKEN")
    print(f"load_dotenv()後のトークン存在: {'あり' if token_after else 'なし'}")
    
    if token_after:
        print(f"トークン長: {len(token_after)}文字")
        print(f"トークン先頭: {token_after[:10]}...")
        print(f"トークン末尾: ...{token_after[-10:]}")
        
        # 余分な空白や改行のチェック
        stripped_token = token_after.strip()
        if stripped_token != token_after:
            print("⚠️ トークンに余分な空白または改行が含まれています")
            diff = len(token_after) - len(stripped_token)
            print(f"  余分な文字数: {diff}")
            return stripped_token
        else:
            print("✅ トークンにはフォーマットの問題はありません")
            return token_after
    else:
        print("❌ .envからトークンを読み込めませんでした")
        return None

if __name__ == "__main__":
    print("=====================================================")
    print("Slack APIトークン詳細診断ツール")
    print("=====================================================")
    
    print(f"Python: {sys.version.split()[0]}")
    print(f"Slackツール診断を開始します...\n")
    
    token = check_env_loading()
    if token:
        validate_token_format(token)
        
        # 両方のメソッドでテスト
        requests_result = test_token_with_requests()
        webclient_result = test_token_with_webclient()
        
        print("\n----- 診断結果サマリー -----")
        print(f"requests テスト: {'✅ 成功' if requests_result else '❌ 失敗'}")
        print(f"WebClient テスト: {'✅ 成功' if webclient_result else '❌ 失敗'}")
        
        if requests_result and not webclient_result:
            print("\n⚠️ 注意: requestsでは成功しましたが、WebClientでは失敗しました。")
            print("これはslack_sdkの設定または問題の可能性があります。")
        
        if not requests_result and not webclient_result:
            print("\n❌ 両方のテストが失敗しました。トークンの有効性を確認してください。")
        
        print("\n=====================================================")
    else:
        print("\n❌ トークンの検証に失敗しました。.envファイルを確認してください。")
