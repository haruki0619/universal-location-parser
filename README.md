# Universal Timeline Parser

複数のGISデータソースからタイムラインデータを統合する汎用的なパーサーです。

## プロジェクトの目標

このプロジェクトは、あらゆるGISデータ（タイムラインデータ、GPSログなど）を単一の統合テーブルに保管することを目指しています。これは、今後 [Pathfinder](https://pathfinder.dk-core.com/) の開発に役立てるための、汎用的かつ包括的なDBの作成を目的としています。

現在は、AndroidおよびiPhoneの端末に保存されているGoogle Timelineデータのみに対応していますが、今後はGPX形式やその他の位置情報データ形式にも拡張していく予定です。

## 構造

```
timeline/
├── main.py                 # メイン実行スクリプト
├── config.py               # 設定ファイル
├── modules/                # 機能別モジュール
│   ├── __init__.py
│   ├── file_handler.py     # ファイル操作
│   ├── json_parser.py      # JSON解析
│   ├── data_converter.py   # データ変換
│   └── csv_exporter.py     # CSV出力
├── data/                   # 入力フォルダ（Git管理外）
└── timeline_output.csv     # 出力ファイル
```

## 使用方法

### 1. ファイル配置
```bash
# Google TimelineのJSONファイルをdataディレクトリに配置
cp your_timeline.json data/
```

### 2. 実行
```bash
# 仮想環境を有効化（初回のみ）
python -m venv venv
source venv/bin/activate  # Linuxの場合
venv\Scripts\activate     # Windowsの場合

# 依存パッケージのインストール（初回のみ）
pip install -r requirements.txt

# 実行
python main.py
```

### 3. 結果確認
- `timeline_output.csv` が生成されます
- 時間順にソートされた統合データが出力されます

## サポートされているデータ形式

現在、以下のデータ形式をサポートしています：

1. **Google Timeline（Android）** - AndroidデバイスからエクスポートされたJSON形式
2. **Google Timeline（iPhone）** - iPhoneデバイスからエクスポートされたJSON形式

今後対応予定の形式：
- GPX（GPS Exchange Format）
- KML/KMZ（Google Earth形式）
- その他のGPSトラッカーアプリのデータ形式

## 各モジュールの役割

### config.py
- ディレクトリパス設定
- 出力ファイル名設定
- CSVカラム定義
- デバッグモード設定

### file_handler.py
- 様々な形式のファイルの検索と読み込み
- ファイル読み込み（複数エンコーディング対応）
- エラーハンドリング
- ユーザー名生成

### json_parser.py
- Android/iPhone形式の自動判別
- データ構造の解析
- visit/activity/timelinePathの抽出
- 座標データの抽出

### data_converter.py
- 時間変換（現地時間→UTC）
- 数値データの正規化
- DataFrameの結合
- 時間順ソート

### csv_exporter.py
- CSVファイル出力
- データ検証
- 結果サマリー表示

## 特徴

### モジュール設計
- **単一責任原則**: 各モジュールが明確な役割を持ち、独立して機能
- **拡張性**: 新しいデータ形式の追加が容易
- **再利用性**: 各モジュールを他のプロジェクトで再利用可能

### 柔軟な設定
- `config.py`で一元管理
- カラム定義の集中管理
- デバッグモード切り替え

### 強力なエラーハンドリング
- 複数エンコーディング対応
- 無効なファイルの検出
- 詳細なエラーメッセージ

## 新しいデータ形式の追加方法

このパーサーは、簡単に新しいデータ形式に対応できるように設計されています：

1. `config.py`の`SUPPORTED_EXTENSIONS`に新しい拡張子を追加
2. `json_parser.py`（または新しいパーサーモジュール）に解析関数を追加
3. `detect_format()`関数を拡張して新しい形式を検出
4. 新しい形式のデータを共通形式に変換する関数を実装

例えば、GPXファイル形式をサポートするには：

```python
# config.py
SUPPORTED_EXTENSIONS = [".json", ".gpx"]

# modules/gpx_parser.py（新規作成）
def parse_gpx_data(data, username):
    records = []
    # GPXデータ解析ロジックを実装
    return records

# json_parser.py を拡張
def detect_format(data):
    if isinstance(data, list) and len(data) > 0 and 'startTime' in data[0]:
        return "iphone"
    elif isinstance(data, dict) and 'semanticSegments' in data:
        return "android"
    elif isinstance(data, str) and '<?xml' in data and '<gpx' in data:
        return "gpx"
    else:
        raise ValueError("不明なデータ形式")

def parse_json_data(data, username):
    try:
        data_format = detect_format(data)
        
        if data_format == "android":
            return parse_android_data(data, username)
        elif data_format == "iphone":
            return parse_iphone_data(data, username)
        elif data_format == "gpx":
            from modules.gpx_parser import parse_gpx_data
            return parse_gpx_data(data, username)
        else:
            raise ValueError(f"未対応の形式: {data_format}")
    except Exception as e:
        # エラーハンドリング
        return []
```

## カラム定義

出力CSVファイルのカラムは`config.py`の`CSV_COLUMNS`で定義されています：

```python
CSV_COLUMNS = [
    "type",
    "start_time", 
    "end_time",
    "point_time",
    "latitude",
    "longitude",
    "visit_probability",
    "visit_placeId", 
    "visit_semanticType",
    "activity_distanceMeters",
    "activity_type", 
    "activity_probability",
    "username"
]
```

新しいカラムを追加または不要なカラムを削除する場合は、このリストを編集するだけです。

## 将来の拡張計画

1. **新しいデータ形式対応**
   - GPX、KML形式のサポート
   - Strava、Garminなどのサービスからのデータインポート
   
2. **データ可視化**
   - 基本的な地図ビューアーの統合
   - 時間ベースのアニメーション

3. **データエンリッチメント**
   - 天気データとの統合
   - 逆ジオコーディング（座標→住所/場所名）

4. **分析機能**
   - 移動パターンの抽出
   - 統計レポート生成

## ライセンス

このプロジェクトのライセンス情報については、プロジェクト管理者にお問い合わせください。
