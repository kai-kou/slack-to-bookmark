#!/usr/bin/env python3
"""
Slack to Bookmark - Pythonパッケージ化セットアップスクリプト

このスクリプトはSlack-to-Bookmarkをpipでインストール可能なパッケージとして配布するための
設定を定義します。
"""

import os
from setuptools import setup, find_packages

# バージョン情報を src/slack_to_bookmark.py から取得
about = {}
with open(os.path.join(os.path.dirname(__file__), "src", "slack_to_bookmark.py")) as f:
    for line in f:
        if line.startswith("__version__"):
            exec(line, about)
            break

# READMEファイルの内容を読み込む
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="slack_to_bookmark",
    version=about["__version__"],
    author="Slack-to-Bookmark Authors",
    author_email="your.email@example.com",  # メールアドレスは適宜変更してください
    description="SlackチャンネルやDMをChromeブックマークに変換するツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/slack-to-bookmark",  # GitHubリポジトリURLに変更してください
    py_modules=["security_check"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.6",
    install_requires=[
        "slack_sdk",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "slack-to-bookmark=src.slack_to_bookmark:main",  # コマンド名はハイフン付きで維持（使いやすさのため）
        ],
    },
    include_package_data=True,
    keywords="slack, bookmark, chrome, productivity, utility",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/slack-to-bookmark/issues",
        "Source": "https://github.com/YOUR_USERNAME/slack-to-bookmark",
        "Documentation": "https://github.com/YOUR_USERNAME/slack-to-bookmark/tree/main/docs",
    },
)
