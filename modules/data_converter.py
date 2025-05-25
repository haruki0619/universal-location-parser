"""
データ変換モジュール
時間変換、座標データの統一、データ型の正規化
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from config import INPUT_TIMEZONE, OUTPUT_TIMEZONE, DEBUG


def convert_timestamp_to_utc(timestamp_str: str) -> pd.Timestamp:
    """タイムスタンプ文字列をUTCに変換"""
    if not timestamp_str:
        return None
    
    try:
        # pandas で解析
        dt = pd.to_datetime(timestamp_str, errors='coerce')
        
        if pd.isna(dt):
            return None
        
        # タイムゾーン処理
        if dt.tz is None:
            # タイムゾーン情報がない場合は日本時間として解釈
            dt = dt.tz_localize(INPUT_TIMEZONE)
        else:
            # 既存のタイムゾーンから日本時間に変換
            dt = dt.tz_convert(INPUT_TIMEZONE)
        
        # UTCに変換
        return dt.tz_convert(OUTPUT_TIMEZONE)
        
    except Exception as e:
        if DEBUG:
            print(f"   ⚠️ 時間変換エラー: {timestamp_str} -> {e}")
        return None


def normalize_numeric_value(value) -> float:
    """数値データの正規化"""
    if value is None or value == '':
        return None
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def convert_records_to_dataframe(records: List[Dict]) -> pd.DataFrame:
    """レコードリストをDataFrameに変換して正規化"""
    if not records:
        return pd.DataFrame()
    
    df = pd.DataFrame(records)
    
    if DEBUG:
        print(f"   🔄 {len(df)} レコードを変換中...")
    
    # 時間カラムの変換
    time_columns = ['start_time', 'end_time', 'point_time']
    for col in time_columns:
        if col in df.columns:
            df[col] = df[col].apply(convert_timestamp_to_utc)
    
    # 数値カラムの変換
    numeric_columns = [
        'latitude', 'longitude', 'activity_distanceMeters', 
        'visit_probability', 'activity_probability'
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(normalize_numeric_value)
    
    # NaN を None に置換
    df = df.replace({np.nan: None})
    
    if DEBUG:
        print(f"   ✅ データ変換完了")
    
    return df


def sort_dataframe_by_time(df: pd.DataFrame) -> pd.DataFrame:
    """DataFrameを時間順にソート"""
    if df.empty:
        return df
    
    if DEBUG:
        print("   🔄 時間順ソート中...")
    
    # ソート用の時間列を作成（優先順位: point_time > start_time > end_time）
    sort_time = df['point_time'].fillna(
        df['start_time'].fillna(df['end_time'])
    )
    
    # ソート実行
    if not sort_time.isna().all():
        sorted_indices = sort_time.sort_values().index
        df_sorted = df.loc[sorted_indices].reset_index(drop=True)
        
        if DEBUG:
            print(f"   ✅ 時間順ソート完了")
        
        return df_sorted
    else:
        if DEBUG:
            print("   ⚠️ ソート可能な時間データなし")
        return df


def combine_dataframes(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
    """複数のDataFrameを結合"""
    if not dataframes:
        return pd.DataFrame()
    
    if DEBUG:
        total_records = sum(len(df) for df in dataframes)
        print(f"🔗 {len(dataframes)}個のDataFrameを結合中... (総{total_records}レコード)")
    
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    if DEBUG:
        print(f"✅ 結合完了: {len(combined_df)} レコード")
    
    return combined_df


def get_dataframe_summary(df: pd.DataFrame) -> Dict:
    """DataFrameの要約情報を取得"""
    if df.empty:
        return {"total_records": 0}
    
    summary = {
        "total_records": len(df),
        "data_types": df['type'].value_counts().to_dict() if 'type' in df.columns else {},
        "users": df['username'].value_counts().to_dict() if 'username' in df.columns else {},
        "time_range": {
            "start": df['start_time'].min() if 'start_time' in df.columns else None,
            "end": df['start_time'].max() if 'start_time' in df.columns else None
        },
        "location_records": len(df.dropna(subset=['latitude', 'longitude'])) if all(col in df.columns for col in ['latitude', 'longitude']) else 0
    }
    
    return summary
