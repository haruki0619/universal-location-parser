# KML/KMZ ファイル解析機能の追加

## 概要
本プルリクエストでは、フォーク（`haruki0619/universal-location-parser`）から本家リポジトリ（`DK-com2/universal-location-parser`）へKML/KMZファイルの読み込み対応機能を追加します。既存のJSON・GPX解析機能と統合して統一的なCSV出力を実現し、Google Earth等で利用されるKML/KMZファイルを新たにサポートすることで、汎用的な位置情報解析システムを構築します。

### 主要機能
- **KML解析**: `gx:Track`要素（Google拡張）および`Placemark`要素の解析
- **KMZ対応**: ZIP展開による`doc.kml`の自動抽出
- **統一フォーマット**: 既存のGPX・JSON解析と同じスキーマでデータ変換
- **エラー耐性**: 破損ファイルや未知要素への対応

## 🔧 変更ファイル一覧

### 新規作成
- `modules/kml_parser.py`: KML/KMZ解析のメインモジュール
- `tests/test_kml_parser.py`: KML解析機能の単体テスト
- `sample_data/dummy_track.kml`: テスト用KMLサンプル
- `sample_data/dummy_track.kmz`: テスト用KMZサンプル

### 修正
- `modules/file_handler.py`: KMZ（ZIP）ファイルの展開処理を追加
- `modules/data_converter.py`: KMLデータの統一フォーマット変換対応
- `requirements.txt`: `fastkml`および`lxml`依存関係を追加
- `main_unified.py`: KMLファイル処理の統合（想定）

## 📋 技術仕様

### 対応KML要素
- `<gx:Track>`: Google拡張のタイムスタンプ付きトラック
  - `<when>`: タイムスタンプ
  - `<gx:coord>`: 座標（経度 緯度 標高）
- `<Placemark>`: 標準的なプレースマーク
  - `<Point>`: 単一点
  - `<LineString>`: 線分
  - `<MultiGeometry>`: 複合ジオメトリ

### 新規依存関係
```
fastkml>=1.0.0,<2.0  # KML解析ライブラリ
lxml>=4.9,<5.0       # XML解析（既存）
```

### 出力フォーマット
```python
{
    'latitude': 35.681, 
    'longitude': 139.767, 
    'elevation': 25.3,
    'point_time': '2025-07-01T09:00:15Z', 
    'type': 'kml_gx_track',  # または 'kml_placemark'
    'username': 'alice'
}
```

## ✅ テスト戦略

### 単体テスト
- [ ] `gx:Track`要素の正常解析
- [ ] `Placemark`要素の正常解析  
- [ ] KMZファイルの展開・解析
- [ ] 破損ファイルのエラーハンドリング
- [ ] 空ファイル・無効XML への対応

### 統合テスト
- [ ] `main_unified.py`経由でのKML/KMZ処理
- [ ] 複数フォーマット（JSON + GPX + KML）の統合出力
- [ ] 既存機能への影響確認

## 🔍 レビューポイント

### 重点確認箇所
1. **`modules/kml_parser.py`**: 
   - XMLパース処理の安全性（XXE攻撃対策）
   - 名前空間の適切な処理
   - エラーハンドリングの妥当性

2. **`modules/file_handler.py`**:
   - ZIP展開処理のセキュリティ（ZipSlip攻撃対策）
   - ファイル種別判定の正確性

3. **統合処理**:
   - 既存のGPX・JSON解析への影響
   - 統一スキーマの一貫性

### パフォーマンス考慮
- 大容量KMZファイルのメモリ使用量
- XMLパース処理の速度

## 🚫 破壊的変更
**なし** - 既存のAPIやデータ形式に変更はありません。

## 📊 確認事項

### 機能テスト
- [ ] `dummy_track.kml`の正常読み込み・CSV出力
- [ ] `dummy_track.kmz`の正常読み込み・CSV出力  
- [ ] 他フォーマット（JSON・GPX）との混在処理
- [ ] エラーケース（破損ファイル等）の適切な処理

### コード品質
- [ ] 単体テストの全パス
- [ ] リンティングルール準拠
- [ ] 型チェック（`mypy`）のパス
- [ ] セキュリティチェック（`bandit`）のパス

## 🔮 今後の予定

### Phase 2 機能拡張
- ExtendedData要素のサポート
- NetworkLink（外部KMLリンク）の対応
- スタイル情報の保持・活用

### 技術負債解消
- 型アノテーションの充実
- エラーハンドリングの標準化
- パフォーマンス最適化

### ドキュメント整備
- KML/KMZ対応機能の詳細ドキュメント作成
- 使用例・サンプルコードの追加
- 英語版ドキュメントの作成

---

**レビュアー**: @haruki0619
**関連Issue**: #XX（該当する場合）

**参考**: [GitHub公式 - プルリクエストのベストプラクティス](https://docs.github.com/ja/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests)
