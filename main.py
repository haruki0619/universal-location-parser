#!/usr/bin/env python3
"""
Google Timeline Parser - メインスクリプト
dataディレクトリ内の全JSONファイルを処理して統合CSVを出力
"""

import sys
import os
from datetime import datetime

# モジュールのインポート
from modules.file_handler import find_json_files, load_json_file, get_username_from_filename, validate_json_data
from modules.json_parser import parse_json_data
from modules.data_converter import convert_records_to_dataframe, sort_dataframe_by_time, combine_dataframes
from modules.csv_exporter import export_to_csv, print_summary, validate_output_data
from config import OUTPUT_FILE, DEBUG


def main():
    """メイン処理"""
    print("🌐 Google Timeline Parser")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # 1. JSONファイルの検索
    print("\n📁 JSONファイルを検索中...")
    json_files = find_json_files()
    
    if not json_files:
        print("❌ 処理するJSONファイルが見つかりません")
        print(f"   dataディレクトリ({os.path.abspath('data')})にJSONファイルを配置してください")
        return
    
    # 2. 各ファイルを処理
    print(f"\n🔄 {len(json_files)}個のファイルを処理中...")
    all_dataframes = []
    processed_files = 0
    
    for i, json_file in enumerate(json_files, 1):
        print(f"\n[{i}/{len(json_files)}] {os.path.basename(json_file)}")
        
        # ファイル読み込み
        data = load_json_file(json_file)
        if data is None:
            continue
        
        # データ妥当性チェック
        if not validate_json_data(data):
            if DEBUG:
                print("   ❌ 無効なデータ形式")
            continue
        
        # ユーザー名生成
        username = get_username_from_filename(json_file)
        
        # JSON解析
        records = parse_json_data(data, username)
        if not records:
            continue
        
        # DataFrame変換
        df = convert_records_to_dataframe(records)
        if df.empty:
            continue
        
        all_dataframes.append(df)
        processed_files += 1
        
        if DEBUG:
            print(f"   ✅ {len(df)} レコード抽出完了")
    
    # 3. データ統合
    if not all_dataframes:
        print("\n❌ 有効なデータが見つかりませんでした")
        return
    
    print(f"\n🔗 {processed_files}個のファイルからデータを統合中...")
    combined_df = combine_dataframes(all_dataframes)
    
    if combined_df.empty:
        print("❌ 統合後のデータが空です")
        return
    
    # 4. 時間ソート
    print("\n⏰ 時間順ソート中...")
    sorted_df = sort_dataframe_by_time(combined_df)
    
    # 5. 出力データ検証
    if not validate_output_data(sorted_df):
        print("❌ 出力データの検証に失敗しました")
        return
    
    # 6. CSV出力
    print(f"\n💾 CSV出力中...")
    output_file = export_to_csv(sorted_df, OUTPUT_FILE)
    
    if output_file:
        # 7. 結果サマリー表示
        end_time = datetime.now()
        processing_time = end_time - start_time
        
        print_summary(sorted_df, output_file)
        print(f"\n⏱️ 処理時間: {processing_time.total_seconds():.2f}秒")
        print("🎉 処理完了!")
    else:
        print("❌ CSV出力に失敗しました")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 処理が中断されました")
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)
