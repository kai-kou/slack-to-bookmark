"""
国際化 (i18n) サポートモジュール
(互換性のために再エクスポート)
"""

from src.i18n import *

if __name__ == "__main__":
    # 既存のCLI呼び出しのためにスクリプトをそのまま実行
    import sys
    import os
    script_path = os.path.join(os.path.dirname(__file__), "src", "i18n.py")
    os.system(f"{sys.executable} {script_path}")
