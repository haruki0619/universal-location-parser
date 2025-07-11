"""
KML/KMZ 解析モジュール
=========================
Google Earth などでエクスポートされる **KML / KMZ** ファイルから、タイムスタンプ付き
位置情報（緯度・経度・標高）を抽出し、汎用的な dict リスト形式で返します。

既存の ``gpx_parser.py`` や ``json_parser.py`` と同じスキーマを維持することで、
``main_unified.py`` 側に大きな改修を入れずそのまま統合できます。

主要機能
---------
* **gx:Track** ― Google 拡張タグを優先解析（<when> + <gx:coord>）
* **Placemark (Point / LineString / MultiGeometry)** ― fastkml で抽出
* **KMZ** ― ZIP 展開して ``doc.kml`` を自動読込
* **エラー耐性** ― 破損ファイル・未知ジオメトリを警告ログに残しスキップ

依存
----
* fastkml >= 1.0.0
* lxml >= 4.9

使い方例
--------
>>> from kml_parser import parse_kml_file
>>> recs = parse_kml_file("data/track.kmz", username="alice")
>>> print(recs[0])
{'latitude': 35.681, 'longitude': 139.767, 'elevation': 25.3,
 'point_time': '2025-07-01T09:00:15Z', 'type': 'kml_gx_track',
 'username': 'alice'}

"""
from __future__ import annotations

import logging
import os
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

from fastkml import kml as _kml  # type: ignore
from lxml import etree  # nosec B410

_LOGGER = logging.getLogger(__name__)
# KML標準・Google拡張の名前空間定義
_NS = {
    "kml": "http://www.opengis.net/kml/2.2",
    "gx": "http://www.google.com/kml/ext/2.2",
}

__all__ = [
    "parse_kml_file",
]

# ---------------------------------------------------------------------------
# 内部ヘルパー関数群
# ---------------------------------------------------------------------------

def _read_kml_bytes(filepath: str | os.PathLike) -> bytes:
    """KMLまたはKMZファイルからKMLバイト列を取得（KMZはdoc.kmlを展開）"""
    path = Path(filepath)
    if path.suffix.lower() == ".kmz":
        with zipfile.ZipFile(path, "r") as kmz:
            try:
                return kmz.read("doc.kml")
            except KeyError as exc:
                raise FileNotFoundError("KMZ 内に doc.kml が見つかりません") from exc
    if not path.exists():
        raise FileNotFoundError(str(path))
    return path.read_bytes()


def _extract_gx_track(root: etree._Element) -> List[Dict]:  # noqa: WPS110
    """<gx:Track>要素から時刻・座標を抽出し、dictリスト化（Google拡張対応）"""
    records: List[Dict] = []
    for track in root.findall(".//gx:Track", namespaces=_NS):
        whens = [e.text for e in track.findall("kml:when", namespaces=_NS)]
        coords = [e.text for e in track.findall("gx:coord", namespaces=_NS)]
        if len(whens) != len(coords):
            _LOGGER.warning("gx:Track の when と coord の数が不一致: %s vs %s", len(whens), len(coords))
        for when, coord in zip(whens, coords):
            try:
                lon, lat, *ele = map(float, coord.split())
            except ValueError:  # pragma: no cover
                _LOGGER.debug("無効な座標文字列: %s", coord)
                continue
            records.append(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "elevation": ele[0] if ele else None,
                    "point_time": when,
                    "type": "kml_gx_track",
                },
            )
    return records


def _extract_simple_geometries(k: _kml.KML) -> List[Dict]:  # noqa: WPS231
    """Placemark配下のPoint/LineString/MultiGeometryを再帰的に抽出"""
    records: List[Dict] = []

    def _walk(feat):  # noqa: WPS430
        for f in feat.features():
            if hasattr(f, "geometry") and f.geometry is not None:
                _handle_geometry(f.geometry, records)
            if hasattr(f, "features"):
                _walk(f)

    def _handle_geometry(geom, store: List[Dict]):  # noqa: WPS231
        """ジオメトリをflattenし座標列をdict化して追加"""
        geom_type = geom.__class__.__name__.lower()
        if geom.is_empty:  # type: ignore[attr-defined]
            return
        try:
            coords_iter = list(geom.coords)  # type: ignore[attr-defined]
        except AttributeError:
            # MultiGeometryの場合は再帰的に処理
            if hasattr(geom, "geoms"):
                for sub in geom.geoms:  # type: ignore[attr-defined]
                    _handle_geometry(sub, store)
            return
        for lon, lat, *rest in coords_iter:
            store.append(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "elevation": rest[0] if rest else None,
                    "type": f"kml_{geom_type}",
                },
            )

    _walk(k)
    return records

# ---------------------------------------------------------------------------
# Public API（外部公開関数）
# ---------------------------------------------------------------------------

def parse_kml_file(filepath: str | os.PathLike, *, username: str | None = None) -> List[Dict]:
    """
    指定したKML/KMZファイルをパースし、位置情報dictのリストを返す。
    dictのスキーマ例::
        {
            "latitude": float,      # 緯度
            "longitude": float,     # 経度
            "elevation": float | None,  # 標高（なければNone）
            "point_time": str | None,   # ISO8601時刻（gx:Track等のみ）
            "type": str,           # "kml_gx_track"や"kml_point"等
            "username": str | None,
        }
    """
    kml_bytes = _read_kml_bytes(filepath)

    # --- gx:Track (Google 拡張) 優先 ---
    root = etree.fromstring(kml_bytes)  # nosec B314
    records = _extract_gx_track(root)

    # --- fallback: Placemark (Point/LineString etc.) ---
    if not records:
        k = _kml.KML()
        k.from_string(kml_bytes)
        records = _extract_simple_geometries(k)

    # usernameを付与（指定時）
    if username is not None:
        for rec in records:
            rec["username"] = username
    else:
        for rec in records:
            rec.setdefault("username", None)

    return records

# ---------------------------------------------------------------------------
# CLIエントリポイント（オプション）
# ---------------------------------------------------------------------------

if __name__ == "__main__":  # pragma: no cover
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse KML/KMZ file and dump JSON")
    parser.add_argument("filepath", help="path to .kml/.kmz file")
    parser.add_argument("--username", help="username to annotate", default=None)
    parser.add_argument("-o", "--output", help="output json path (default: stdout)")
    args = parser.parse_args()

    result = parse_kml_file(args.filepath, username=args.username)
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
