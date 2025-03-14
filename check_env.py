"""
環境変数の読み込みと実際の値をチェックするシンプルなスクリプト
(互換性のために再エクスポート)
"""

from src.check_env import *

if __name__ == "__main__":
    # 既存のCLI呼び出しのためにスクリプトをそのまま実行
    import sys
    import os
    script_path = os.path.join(os.path.dirname(__file__), "src", "check_env.py")
    os.system(f"{sys.executable} {script_path}")
