# Google Timeline Parser - 設定ファイル

# ディレクトリパス
DATA_DIR = "data"
OUTPUT_FILE = "timeline_output.csv"

# ユーザー名設定（シンプルに固定）
USERNAME = "testuser"

# CSV出力カラム定義
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

# タイムゾーン設定
INPUT_TIMEZONE = "Asia/Tokyo"
OUTPUT_TIMEZONE = "UTC"

# サポートされるファイル形式
SUPPORTED_EXTENSIONS = [".json"]

# デバッグモード
DEBUG = True
