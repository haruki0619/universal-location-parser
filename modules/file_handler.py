"""
ファイル操作モジュール
JSONファイルの検索、読み込み、エラーハンドリング
"""

import os
import json
import glob
from typing import List, Union, Dict, Any
from config import DATA_DIR, SUPPORTED_EXTENSIONS, DEBUG, USERNAME, JSON_EXTS, GPX_EXTS, KML_EXTS
from pathlib import Path


def _glob_exts(base_dir: Path, exts: list) -> list:
    files = []
    for ext in exts:
        files.extend(base_dir.glob(f"**/*{ext}"))
    return sorted(set(str(f) for f in files))


def find_json_files(base_dir=DATA_DIR):
    """データディレクトリ内のJSONファイルを検索する"""
    if not base_dir.exists():
        print(f"❌ データディレクトリが存在しません: {base_dir}")
        return []
    files = _glob_exts(base_dir, JSON_EXTS)
    return files


def find_gpx_files(base_dir=DATA_DIR):
    """データディレクトリ内のGPXファイルを検索する"""
    if not base_dir.exists():
        print(f"❌ データディレクトリが存在しません: {base_dir}")
        return []
    files = _glob_exts(base_dir, GPX_EXTS)
    return files


def find_kml_files(base_dir=DATA_DIR):
    """データディレクトリ内のKML/KMZファイルを検索する"""
    if not base_dir.exists():
        print(f"❌ データディレクトリが存在しません: {base_dir}")
        return []
    files = _glob_exts(base_dir, KML_EXTS)
    return files


def find_all_files(base_dir: Path = Path(DATA_DIR)) -> dict:
    """すべてのサポートされているファイルを検索する（KML/KMZも含む）"""
    return {
        "json": find_json_files(base_dir),
        "gpx": find_gpx_files(base_dir),
        "kml": find_kml_files(base_dir),
    }


def load_json_file(filepath) -> Union[Dict, List, None]:
    """ファイルを安全に読み込む"""
    try:
        # ファイルサイズチェック
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            return None
        
        # 複数エンコーディングで試行
        encodings = ['utf-8', 'utf-8-sig', 'shift_jis', 'cp932']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read().strip()
                
                if not content:
                    return None
                
                data = json.loads(content)
                return data
                
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                continue
        
        return None
        
    except Exception as e:
        pass
    return None


def get_username() -> str:
    """固定ユーザー名を返す"""
    return USERNAME


def get_username_from_filename(filepath: str) -> str:
    """ファイル名からユーザー名を抽出する
    
    ファイル名のパターンによってユーザー名を決定します
    見つからない場合は固定ユーザー名を返します
    """
    # ファイル名から基本名を取得（拡張子を除く）
    basename = os.path.basename(filepath)
    filename_without_ext = os.path.splitext(basename)[0]
    
    # ファイル名からユーザー名のパターンを識別
    # ここでは簡単な例を示しています。必要に応じてパターンを追加してください
    
    # 1. ファイル名に「username-」または「user-」プレフィックスがある場合
    if filename_without_ext.lower().startswith("username-"):
        return filename_without_ext[9:]
    elif filename_without_ext.lower().startswith("user-"):
        return filename_without_ext[5:]
    
    # 2. アンダースコアで区切られた場合（例: username_date.json）
    parts = filename_without_ext.split('_')
    if len(parts) > 1:
        return parts[0]
    
    # 3. 特定のパターンが見つからない場合は設定ファイルのユーザー名を使用
    return get_username()


def validate_json_data(data: Union[Dict, List]) -> bool:
    """データの基本的な検証"""
    if data is None:
        return False
    
    if isinstance(data, dict) and 'semanticSegments' in data:
        return True  # Android形式
    
    if isinstance(data, list) and len(data) > 0 and 'startTime' in data[0]:
        return True  # iPhone形式
    
    return False


def validate_gpx_file(filepath: str) -> bool:
    """GPXファイルの基本的な検証"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # 最初の1000文字をチェック
        
        # 基本的なGPXヘッダーの確認
        return '<?xml' in content and ('gpx' in content.lower() or 'GPX' in content)
        
    except Exception:
        return False
