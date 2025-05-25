# リポジトリ設定ガイド

このファイルには、GitHubリポジトリの推奨設定が記載されています。リポジトリを作成・設定する際の参考にしてください。

## リポジトリ基本情報

- **名前**: universal-location-parser
- **説明**:
  - 日本語: 複数のGIS/位置情報データ形式を統合して単一のタイムラインに変換するパーサー。Google Timeline（Android/iOS）やGPXなどの形式に対応し、Pathfinderプロジェクトのためのデータベース構築をサポート。
  - 英語: A parser that unifies multiple GIS/location data formats into a single timeline. Compatible with Google Timeline (Android/iOS), GPX, and more, supporting database construction for the Pathfinder project.
- **ウェブサイト**: https://pathfinder.dk-core.com/ (Pathfinderプロジェクトサイト)
- **トピック**: gis, timeline, parser, location-data, python, gpx, google-timeline
- **ライセンス**: MIT

## リポジトリ設定

### 1. ブランチ保護ルール
`main`ブランチに以下の保護ルールを設定することをお勧めします：
- プルリクエストによる変更のみ許可
- マージ前にレビュー必須
- ステータスチェックの通過を必須に

### 2. Issueラベル
以下のラベルを作成すると効果的です：
- `bug`: バグ報告
- `enhancement`: 機能追加・改善
- `documentation`: ドキュメント関連
- `good first issue`: 初めての貢献者向け
- `help wanted`: 協力募集中
- `data-format`: 新しいデータ形式関連

### 3. 自動テスト
以下のGitHub Actionsを設定することをお勧めします：
- Python Lint & Test
- Dependency Security Check

### 4. 貢献者向けバッジ
READMEに以下のバッジを追加すると効果的です：
- GitHub Stars
- GitHub Issues
- License
- Python Version

## コミュニティガイドライン

コミュニティ運営のポイント：
1. 新しいIssueには24時間以内に初期レスポンスを
2. 初めての貢献者には特に丁寧なフィードバックを
3. 定期的に「good first issue」タグの付いたタスクを追加
4. 積極的な貢献者にはコラボレーター権限の付与を検討
