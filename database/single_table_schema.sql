-- Timeline Data - シンプルな単一テーブルスキーマ
-- このSQLスクリプトは現在のCSV出力と同じ構造の単一テーブルを作成します

-- PostGISエクステンションを有効化（地理空間データ処理のため）
CREATE EXTENSION IF NOT EXISTS postgis;

-- タイムラインデータ用のシンプルな単一テーブル
CREATE TABLE timeline_data (
    -- 主キー（自動採番）
    id BIGSERIAL PRIMARY KEY,
    
    -- データの種類（timelinePath, visit, activity_start, activity_end）
    type VARCHAR(50) NOT NULL,
    
    -- 時間情報
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    point_time TIMESTAMPTZ,
    
    -- 位置情報
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    
    -- 地理空間データ（PostGIS）- 緯度経度から自動生成
    location GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS 
        (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography) STORED,
    
    -- 訪問データ関連
    visit_probability FLOAT,
    visit_placeId VARCHAR(255),
    visit_semanticType VARCHAR(50),
    
    -- 活動データ関連
    activity_distanceMeters FLOAT,
    activity_type VARCHAR(50),
    activity_probability FLOAT,
    
    -- ユーザー情報
    username VARCHAR(255) NOT NULL,
    
    -- メタデータ
    source VARCHAR(50),  -- データソース（google_timeline_android, google_timeline_ios, yamap, garmin, etc.）
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP  -- レコード作成日時
);

-- インデックス - パフォーマンス最適化用
-- 時間検索のためのインデックス
CREATE INDEX timeline_time_idx ON timeline_data (start_time, end_time);
CREATE INDEX timeline_point_time_idx ON timeline_data (point_time);

-- ユーザー検索のためのインデックス
CREATE INDEX timeline_username_idx ON timeline_data (username);

-- データタイプ検索のためのインデックス
CREATE INDEX timeline_type_idx ON timeline_data (type);

-- 位置情報検索のための空間インデックス
CREATE INDEX timeline_location_idx ON timeline_data USING GIST (location);

-- 複合インデックス - よく使われる検索パターン用
CREATE INDEX timeline_user_time_type_idx ON timeline_data (username, start_time, type);

-- コメント
COMMENT ON TABLE timeline_data IS 'タイムラインデータ統合テーブル - Google Timeline, YAMAP, Garminなどの位置情報を保存';
COMMENT ON COLUMN timeline_data.type IS 'データタイプ: timelinePath, visit, activity_start, activity_end など';
COMMENT ON COLUMN timeline_data.source IS 'データソース: google_timeline_android, google_timeline_ios, yamap, garmin など';
COMMENT ON COLUMN timeline_data.location IS 'PostGIS地理空間データ型 - 緯度経度から自動生成された位置情報';

-- サンプルSQLクエリ

-- 1. 特定ユーザーの特定日の位置情報取得
-- SELECT * FROM timeline_data 
-- WHERE username = 'testuser' 
-- AND start_time >= '2025-05-01'::date 
-- AND start_time < '2025-05-02'::date
-- ORDER BY COALESCE(point_time, start_time);

-- 2. 特定範囲内の位置情報取得
-- SELECT * FROM timeline_data
-- WHERE ST_DWithin(
--     location, 
--     ST_SetSRID(ST_MakePoint(139.7, 35.6), 4326)::geography,
--     1000  -- 1km以内
-- );

-- 3. ユーザーごとの活動タイプ集計
-- SELECT username, activity_type, COUNT(*), SUM(activity_distanceMeters)
-- FROM timeline_data
-- WHERE activity_type IS NOT NULL
-- GROUP BY username, activity_type;

-- 4. CSVデータのインポート例（COPY文）
-- COPY timeline_data(type, start_time, end_time, point_time, latitude, longitude, 
--                  visit_probability, visit_placeId, visit_semanticType,
--                  activity_distanceMeters, activity_type, activity_probability, username)
-- FROM 'path/to/timeline_output.csv' 
-- DELIMITER ',' 
-- CSV HEADER;
