# Changelog

このファイルでは、プロジェクトの変更履歴を管理します。

形式は「日付ごとの変更点（追加/変更/修正/ドキュメント）」で簡潔にまとめています。

## [Unreleased]
- 新しいデータソース対応や可視化の拡充を予定。

## [2025-08-09]

### 追加（Added）
- KML/KMZ の正式対応。
  - KMZで `doc.kml` が無い場合も、最初に見つかった `.kml` を読み込むフォールバックを実装。
- KMLの時刻抽出を強化（TimeStamp, TimeSpan, gx:Track に対応）。
- KML/KMZのエッジケース向けテストを追加。
- DataFrame結合の回帰テストを追加（全NA列の扱い）。

### 変更（Changed）
- KML抽出の粒度改善に伴い、テストの期待値を「2→5」に更新。
  - 仕様の明確化：より多くのポイントを正しく抽出するのが意図です。
- READMEを更新（KML/KMZ対応、タイムゾーンの扱い、処理順を明記）。

### 修正（Fixed）
- pandasのFutureWarning（concat時の全NA列）を解消。
  - 各DataFrameで全NA列を一時的に削除してから結合する方式に変更。
- `main_unified.py` の進捗/サマリに KML/KMZ を反映。

### ドキュメント（Documentation）
- タイムゾーン方針を明記：
  - naiveは `INPUT_TIMEZONE` で解釈 → `OUTPUT_TIMEZONE` に変換 → tz情報を外して保存（ソート/CSVの一貫性のため）。
- CONTRIBUTINGを更新：
  - 仕様に影響する変更はPRとCHANGELOGに必ず記載。
  - 回帰テストの追加指針を追記。
