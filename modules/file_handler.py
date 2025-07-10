"""
ファイル操作モジュール
JSONファイルの検索、読み込み、エラーハンドリング
"""

import os
import json
import glob
from typing import List, Union, Dict, Any
from config import DATA_DIR, SUPPORTED_EXTENSIONS, DEBUG, USERNAME


def find_json_files() -> List[str]:
    """データディレクトリ内のJSONファイルを検索する"""
    if not os.path.exists(DATA_DIR):
        print(f"❌ データディレクトリが存在しません: {DATA_DIR}")
        return []
    
    json_files = []
    for ext in SUPPORTED_EXTENSIONS:
        pattern = os.path.join(DATA_DIR, f"*{ext}")
        json_files.extend(glob.glob(pattern))
    
    if DEBUG:
        print(f"📁 {len(json_files)}個のJSONファイルを発見:")
        for file in json_files:
            print(f"   - {os.path.basename(file)}")
    
    return json_files


def find_gpx_files() -> List[str]:
    """データディレクトリ内のGPXファイルを検索する"""
    if not os.path.exists(DATA_DIR):
        print(f"❌ データディレクトリが存在しません: {DATA_DIR}")
        return []
    
    gpx_files = []
    gpx_extensions = ['.gpx', '.GPX']
    
    for ext in gpx_extensions:
        pattern = os.path.join(DATA_DIR, f"*{ext}")
        gpx_files.extend(glob.glob(pattern))
    
    if DEBUG:
        print(f"🏔️ {len(gpx_files)}個のGPXファイルを発見:")
        for file in gpx_files:
            print(f"   - {os.path.basename(file)}")
    
    return gpx_files


def find_kml_files() -> List[str]:
    """データディレクトリ内のKML/KMZファイルを検索する"""
    if not os.path.exists(DATA_DIR):
        print(f"❌ データディレクトリが存在しません: {DATA_DIR}")
        return []
    
    kml_exts = ['.kml', '.kmz', '.KML', '.KMZ']
    files = []
    for ext in kml_exts:
        files.extend(glob.glob(os.path.join(DATA_DIR, f"*{ext}")))
    
    if DEBUG:
        print(f"🗺️ {len(files)}個のKML/KMZファイルを発見:")
        for file in files:
            print(f"   - {os.path.basename(file)}")
    
    return files


def find_all_files() -> Dict[str, List[str]]:
    """すべてのサポートされているファイルを検索する（KML/KMZも含む）"""
    return {
        'json': find_json_files(),
        'gpx': find_gpx_files(),
        'kml': find_kml_files(),  # KML/KMZを追加
    }


def load_json_file(filepath: str) -> Union[Dict, List, None]:
    """ファイルを安全に読み込む"""
    if DEBUG:
        print(f"📖 読み込み中: {os.path.basename(filepath)}")
    
    try:
        # ファイルサイズチェック
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            if DEBUG:
                print("   ❌ ファイルが空です")
            return None
        
        # 複数エンコーディングで試行
        encodings = ['utf-8', 'utf-8-sig', 'shift_jis', 'cp932']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read().strip()
                
                if not content:
                    if DEBUG:
                        print("   ❌ ファイル内容が空です")
                    return None
                
                data = json.loads(content)
                if DEBUG:
                    print(f"   ✅ 読み込み成功 ({encoding})")
                return data
                
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                if DEBUG:
                    print(f"   ❌ JSON解析エラー ({encoding}): {e}")
                continue
        
        if DEBUG:
            print("   ❌ 全エンコーディングで失敗")
        return None
        
    except Exception as e:
        if DEBUG:
            print(f"   ❌ ファイル読み込みエラー: {e}")
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
