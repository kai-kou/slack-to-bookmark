#!/usr/bin/env python3
"""
環境変数の読み込みと実際の値をチェックするシンプルなスクリプト
"""

import os
import sys
from dotenv import load_dotenv
import requests

print("========== 環境変数チェック ==========")

# load_dotenv()の前の環境変数を出力
print("load_dotenv()前の環境変数:")
token_before = os.getenv("SLACK_TOKEN")
workspace_before = os.getenv("WORKSPACE_NAME")
workspace_id_before = os.getenv("WORKSPACE_ID")
print(f"SLACK_TOKEN: {'あり' if token_before else 'なし'}")
print(f"WORKSPACE_NAME: {workspace_before or 'なし'}")
print(f"WORKSPACE_ID: {workspace_id_before or 'なし'}")

# .envファイルを読み込む
print("\n.envファイルを読み込みます...")
load_dotenv(override=True)

# load_dotenv()後の環境変数を出力
print("\nload_dotenv()後の環境変数:")
token = os.getenv("SLACK_TOKEN")
workspace = os.getenv("WORKSPACE_NAME")
workspace_id = os.getenv("WORKSPACE_ID")
print(f"SLACK_TOKEN: {'あり' if token else 'なし'}")
if token:
    print(f"  先頭: {token[:10]}...")
    print(f"  長さ: {len(token)}文字")
print(f"WORKSPACE_NAME: {workspace or 'なし'}")
print(f"WORKSPACE_ID: {workspace_id or 'なし'}")

# slack_to_bookmark.pyのデフォルト値をシミュレーション
print("\nslack_to_bookmark.pyでの実際の値:")
final_token = token
final_workspace = workspace or "your-workspace"  # デフォルト値
final_workspace_id = workspace_id or "T00000000"  # デフォルト値
print(f"token: {'あり' if final_token else 'なし'}")
print(f"workspace_name: {final_workspace}")
print(f"workspace_id: {final_workspace_id}")

# APIテスト
print("\nSlack API認証テスト:")
try:
    url = "https://slack.com/api/auth.test"
    headers = {"Authorization": f"Bearer {final_token}"}
    response = requests.post(url, headers=headers)
    result = response.json()

    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {result}")

    if result.get("ok"):
        print("✅ 認証テスト: 成功")
        print(f"ユーザー: {result.get('user')}")
        print(f"チーム: {result.get('team')}")
        print(f"チームID: {result.get('team_id')}")
    else:
        print(f"❌ 認証テスト: 失敗 - {result.get('error')}")
except Exception as e:
    print(f"❌ テスト実行中にエラー: {e}")

print("\n======================================")
