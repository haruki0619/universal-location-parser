# 単一テーブルデータベース設計

このディレクトリには、現在のCSV形式から直接移行可能な単一テーブルのPostgreSQLデータベース設計が含まれています。

## ファイル

- `single_table_schema.sql` - 現在のCSV構造に基づく単一テーブルのPostgreSQLスキーマ定義

## 設計概要

この設計は、現在のCSV出力と同じ構造を保ちながら、PostgreSQLの機能を活用してパフォーマンスと分析機能を強化しています。

### 特徴

1. **単一テーブル構造**
   - 現在のCSVと同じフラットな構造
   - すべてのデータが一つのテーブルに格納される
   - カラム名はCSVと一致

2. **PostgreSQL最適化**
   - 適切なデータ型の使用（TIMESTAMPTZ, FLOAT, VARCHAR等）
   - パフォーマンス向上のためのインデックス
   - PostGISによる地理空間データのサポート

3. **拡張性**
   - 新しいデータソースのための'source'カラム
   - レコード作成日時の自動記録

## 使用方法

### データベース作成

```bash
# PostgreSQLでデータベースを作成
createdb timeline_db

# スキーマの適用
psql -d timeline_db -f single_table_schema.sql
```

### CSVデータのインポート

```bash
# CSVデータのインポート
psql -d timeline_db -c "\COPY timeline_data(type, start_time, end_time, point_time, latitude, longitude, visit_probability, visit_placeId, visit_semanticType, activity_distanceMeters, activity_type, activity_probability, username) FROM 'path/to/timeline_output.csv' DELIMITER ',' CSV HEADER;"
```

## サンプルクエリ

```sql
-- 特定ユーザーの特定日の位置情報取得
SELECT * FROM timeline_data 
WHERE username = 'testuser' 
AND start_time >= '2025-05-01'::date 
AND start_time < '2025-05-02'::date
ORDER BY COALESCE(point_time, start_time);

-- 特定範囲内の位置情報取得
SELECT * FROM timeline_data
WHERE ST_DWithin(
    location, 
    ST_SetSRID(ST_MakePoint(139.7, 35.6), 4326)::geography,
    1000  -- 1km以内
);

-- ユーザーごとの活動タイプ集計
SELECT username, activity_type, COUNT(*), SUM(activity_distanceMeters)
FROM timeline_data
WHERE activity_type IS NOT NULL
GROUP BY username, activity_type;
```

## 将来の拡張

現在は単一テーブルの設計ですが、データ量が増加したり、複雑なクエリパターンが必要になった場合は、より正規化された設計への移行を検討する予定があります。単一テーブルの利点は、シンプルさと現在のCSV構造との互換性です。
