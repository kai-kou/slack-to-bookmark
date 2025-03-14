#!/usr/bin/env python3
"""
セキュリティチェックスクリプト

このスクリプトはプロジェクト内の潜在的なセキュリティリスクをスキャンします。
環境情報や機密データが誤って含まれていないかを検出します。
"""

import os
import re
import sys
import glob


def print_header(title):
    """ヘッダーを出力する"""
    width = len(title) + 4
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_result(status, message):
    """結果を出力する"""
    if status == "OK":
        print(f"✓ {message}")
    elif status == "WARNING":
        print(f"⚠ {message}")
    elif status == "ERROR":
        print(f"✗ {message}")
    else:
        print(f"  {message}")


def scan_for_tokens(file_path):
    """ファイル内のAPIトークンパターンをスキャンする"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

            # Slackトークンのパターン
            slack_token_pattern = r"xoxp-[0-9A-Za-z]{12,}"
            slack_tokens = re.findall(slack_token_pattern, content)

            # その他のAPIキーパターン (例: 16-64文字の英数字)
            api_key_pattern = r'[\'"][a-zA-Z0-9]{16,64}[\'"]'
            api_keys = re.findall(api_key_pattern, content)

            return slack_tokens, api_keys
    except Exception as e:
        return [], []


def scan_for_workspace_info(file_path):
    """ファイル内のワークスペース情報をスキャンする"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

            # ワークスペースIDのパターン
            workspace_id_pattern = r"T[A-Z0-9]{8,10}"
            workspace_ids = re.findall(workspace_id_pattern, content)

            return workspace_ids
    except Exception as e:
        return []


def check_env_file():
    """環境変数ファイルのチェック"""
    print_header("環境変数ファイルのチェック")

    if os.path.exists(".env"):
        print_result(
            "WARNING",
            ".envファイルが存在します。これには機密情報が含まれている可能性があります。",
        )
        print_result(
            "INFO",
            "  .envファイルはgitignoreされていますが、プロジェクトを共有する際には注意してください。",
        )

        # .envファイル内の内容を確認
        try:
            with open(".env", "r", encoding="utf-8") as f:
                env_content = f.read()

                if "SLACK_TOKEN=" in env_content:
                    print_result(
                        "WARNING", "  .envファイルにSLACK_TOKENが設定されています。"
                    )

                if "WORKSPACE_NAME=" in env_content:
                    print_result(
                        "WARNING", "  .envファイルにWORKSPACE_NAMEが設定されています。"
                    )

                if "WORKSPACE_ID=" in env_content:
                    print_result(
                        "WARNING", "  .envファイルにWORKSPACE_IDが設定されています。"
                    )
        except Exception as e:
            print_result(
                "ERROR", f"  .envファイルの読み込み中にエラーが発生しました: {e}"
            )
    else:
        print_result("OK", ".envファイルが存在しません。")

    if os.path.exists(".env.sample"):
        print_result("INFO", ".env.sampleファイルが存在します。これは問題ありません。")

        # サンプルファイル内の実際のデータがないか確認
        try:
            with open(".env.sample", "r", encoding="utf-8") as f:
                sample_content = f.read()

                if re.search(
                    r"SLACK_TOKEN=(?!.*DUMMY)(?!.*YOUR)(?!.*XXXX)(?!.*example).*",
                    sample_content,
                    re.IGNORECASE,
                ):
                    print_result(
                        "WARNING",
                        "  .env.sampleファイルに実際のSLACK_TOKENが設定されている可能性があります。",
                    )

                if re.search(
                    r"WORKSPACE_NAME=(?!.*DUMMY)(?!.*YOUR)(?!.*XXXX)(?!.*example).*",
                    sample_content,
                    re.IGNORECASE,
                ):
                    print_result(
                        "WARNING",
                        "  .env.sampleファイルに実際のWORKSPACE_NAMEが設定されている可能性があります。",
                    )

                if re.search(
                    r"WORKSPACE_ID=(?!.*DUMMY)(?!.*YOUR)(?!.*XXXX)(?!.*example).*",
                    sample_content,
                    re.IGNORECASE,
                ):
                    print_result(
                        "WARNING",
                        "  .env.sampleファイルに実際のWORKSPACE_IDが設定されている可能性があります。",
                    )
        except Exception as e:
            print_result(
                "ERROR", f"  .env.sampleファイルの読み込み中にエラーが発生しました: {e}"
            )


def check_generated_files():
    """生成されたファイルのチェック"""
    print_header("生成されたファイルのチェック")

    generated_patterns = ["slack_*.html", "bookmark_guide*.html"]

    found_files = []
    for pattern in generated_patterns:
        found_files.extend(glob.glob(pattern))

    if found_files:
        print_result(
            "WARNING",
            f"{len(found_files)}個の生成されたファイルが見つかりました。これらには組織の情報が含まれている可能性があります。",
        )
        for file in found_files:
            print_result("INFO", f"  - {file}")
        print_result(
            "INFO",
            "  これらのファイルは.gitignoreされていますが、共有する際には注意してください。",
        )
    else:
        print_result("OK", "生成されたHTMLファイルは見つかりませんでした。")


def check_source_code():
    """ソースコードのチェック"""
    print_header("ソースコードのチェック")

    source_files = []
    for ext in [".py", ".js", ".json", ".md", ".txt"]:
        source_files.extend(glob.glob(f"**/*{ext}", recursive=True))

    token_found = False
    workspace_info_found = False

    for file_path in source_files:
        # .gitやvenv内のファイルはスキップ
        if ".git/" in file_path or "venv/" in file_path or "__pycache__/" in file_path:
            continue

        # APIトークンのスキャン
        slack_tokens, api_keys = scan_for_tokens(file_path)
        if slack_tokens or api_keys:
            if not token_found:
                token_found = True
                print_result(
                    "WARNING", "潜在的なAPIトークンが以下のファイルで見つかりました:"
                )

            if slack_tokens:
                print_result(
                    "ERROR",
                    f"  {file_path}: Slackトークンのパターンが{len(slack_tokens)}個見つかりました",
                )

            if api_keys and file_path != ".env.sample":  # .env.sampleは除外
                print_result(
                    "WARNING",
                    f"  {file_path}: 潜在的なAPIキーのパターンが{len(api_keys)}個見つかりました",
                )

        # ワークスペース情報のスキャン
        workspace_ids = scan_for_workspace_info(file_path)
        if workspace_ids and file_path != ".env.sample":  # .env.sampleは除外
            if not workspace_info_found:
                workspace_info_found = True
                print_result(
                    "WARNING",
                    "潜在的なワークスペース情報が以下のファイルで見つかりました:",
                )

            print_result(
                "WARNING",
                f"  {file_path}: ワークスペースIDのパターンが{len(workspace_ids)}個見つかりました",
            )

    if not token_found and not workspace_info_found:
        print_result("OK", "ソースコード内に機密情報は見つかりませんでした。")


def check_git_hooks():
    """Gitフックのチェック"""
    print_header("Gitフックのチェック")

    if os.path.exists(".git/hooks/pre-commit"):
        try:
            with open(".git/hooks/pre-commit", "r", encoding="utf-8") as f:
                hook_content = f.read()

                if (
                    'git diff --cached --name-only | grep -q "\\.env$"' in hook_content
                    and "exit 1" in hook_content
                ):
                    print_result(
                        "OK",
                        "pre-commitフックが.envファイルのコミットをブロックするよう設定されています。",
                    )
                else:
                    print_result(
                        "WARNING",
                        "pre-commitフックが.envファイルのチェックを行っていない可能性があります。",
                    )

                if "slack_.*\\.html" in hook_content:
                    print_result(
                        "OK",
                        "pre-commitフックが生成されたHTMLファイルのコミットをブロックするよう設定されています。",
                    )
                else:
                    print_result(
                        "WARNING",
                        "pre-commitフックが生成されたHTMLファイルのチェックを行っていない可能性があります。",
                    )

                if "xoxp-[0-9A-Za-z]" in hook_content:
                    print_result(
                        "OK",
                        "pre-commitフックがSlackトークンのパターンをチェックするよう設定されています。",
                    )
                else:
                    print_result(
                        "WARNING",
                        "pre-commitフックがSlackトークンのチェックを行っていない可能性があります。",
                    )

            if not os.access(".git/hooks/pre-commit", os.X_OK):
                print_result(
                    "ERROR",
                    "pre-commitフックに実行権限がありません。chmod +x .git/hooks/pre-commitを実行してください。",
                )
            else:
                print_result("OK", "pre-commitフックに実行権限があります。")
        except Exception as e:
            print_result(
                "ERROR", f"pre-commitフックの読み込み中にエラーが発生しました: {e}"
            )
    else:
        print_result(
            "WARNING",
            "pre-commitフックが見つかりません。これは機密情報を誤ってコミットするリスクを増加させます。",
        )
        print_result(
            "INFO",
            "  pre-commitフックを設定するために、README.mdの指示に従ってください。",
        )


def check_gitignore():
    """gitignoreのチェック"""
    print_header(".gitignoreのチェック")

    if os.path.exists(".gitignore"):
        try:
            with open(".gitignore", "r", encoding="utf-8") as f:
                gitignore_content = f.read()

                # 重要な項目が.gitignoreに含まれているか確認
                checks = {
                    ".env": ".envファイルは.gitignoreに含まれています。",
                    "slack_*.html": "生成されたslack_*.htmlファイルは.gitignoreに含まれています。",
                    "bookmark_guide*.html": "生成されたbookmark_guide*.htmlファイルは.gitignoreに含まれています。",
                    "__pycache__": "Pythonのキャッシュファイルは.gitignoreに含まれています。",
                    "*.py[cod]": "Pythonのコンパイルファイルは.gitignoreに含まれています。",
                    "venv/": "仮想環境ディレクトリは.gitignoreに含まれています。",
                }

                for pattern, message in checks.items():
                    if pattern in gitignore_content:
                        print_result("OK", message)
                    else:
                        print_result(
                            "WARNING", f"{pattern}が.gitignoreに含まれていません。"
                        )
        except Exception as e:
            print_result(
                "ERROR", f".gitignoreファイルの読み込み中にエラーが発生しました: {e}"
            )
    else:
        print_result(
            "ERROR",
            ".gitignoreファイルが見つかりません。機密情報が誤ってコミットされる可能性があります。",
        )


def main():
    """メイン実行関数"""
    # スクリプトが直接実行される場合のみ実行
    if __name__ == "__main__":
        print("\n🔒 Slack-to-Bookmark セキュリティチェック 🔒")
        print(
            "このツールはプロジェクト内の潜在的なセキュリティリスクをスキャンします。"
        )
        print("環境情報や機密データが誤って含まれていないかをチェックします。")

        check_env_file()
        check_generated_files()
        check_source_code()
        check_git_hooks()
        check_gitignore()

        print("\n🔒 セキュリティチェック完了 🔒")
        print("このチェックは基本的なセキュリティリスクのみをカバーしています。")
        print("コード共有前に、手動での最終確認を行うことをお勧めします。")


# スクリプトを実行
main()
