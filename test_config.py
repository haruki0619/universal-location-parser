#!/usr/bin/env python3
"""
設定テストスクリプト
config.pyの動作確認
"""

try:
    from config import *
    
    print("🔧 config.py 設定テスト")
    print("=" * 40)
    
    print(f"📁 DATA_DIR: {DATA_DIR}")
    print(f"📄 OUTPUT_FILE: {OUTPUT_FILE}")
    print(f"👤 USERNAME: {USERNAME}")
    print(f"🐛 DEBUG: {DEBUG}")
    print(f"🌍 TIMEZONE: {INPUT_TIMEZONE} → {OUTPUT_TIMEZONE}")
    
    print(f"\n📋 CSV_COLUMNS 数: {len(CSV_COLUMNS)}")
    print("   主要カラム:", CSV_COLUMNS[:5])
    print("   GPXカラム:", [col for col in CSV_COLUMNS if col.startswith('_gpx')])
    
    print(f"\n🏔️ GPX_CONFIG:")
    print(f"   速度しきい値: {GPX_CONFIG['speed_thresholds']}")
    print(f"   標高しきい値: {GPX_CONFIG['elevation_thresholds']}")
    print(f"   データソース数: {len(GPX_CONFIG['data_source_defaults'])}")
    
    print("\n✅ config.py は正常に動作しています！")
    
except ImportError as e:
    print(f"❌ config.py インポートエラー: {e}")
except Exception as e:
    print(f"❌ config.py 設定エラー: {e}")
