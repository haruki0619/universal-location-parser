"""
基本的なテストケース
"""

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.file_handler import get_username_from_filename
from config import USERNAME


class TestFileHandler(unittest.TestCase):
    """ファイルハンドラーモジュールのテスト"""

    def test_get_username_from_filename(self):
        """ファイル名からユーザー名を抽出するテスト"""
        # 基本ケース
        self.assertEqual(get_username_from_filename("username-test.json"), "test")
        self.assertEqual(get_username_from_filename("user-john.json"), "john")
        
        # アンダースコアのケース
        self.assertEqual(get_username_from_filename("john_data.json"), "john")
        
        # パターンなしの場合はデフォルト値
        self.assertEqual(get_username_from_filename("nopattern.json"), USERNAME)
        
        # パスを含む場合
        self.assertEqual(get_username_from_filename("/path/to/username-test.json"), "test")
        self.assertEqual(get_username_from_filename("C:\\path\\to\\user-john.json"), "john")


if __name__ == "__main__":
    unittest.main()
