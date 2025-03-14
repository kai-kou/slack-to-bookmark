"""
セキュリティチェック モジュール
(互換性のために再エクスポート)
"""

from src.security_check import *

if __name__ == "__main__":
    # 既存のCLI呼び出しのためにスクリプトをそのまま実行
    import sys
    import os
    script_path = os.path.join(os.path.dirname(__file__), "src", "security_check.py")
    os.system(f"{sys.executable} {script_path}")
