"""Download Sentinel-2 assets from Microsoft Planetary Computer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dune_ai_monitoring.datasets.manifest import DatasetRecord, add_record_to_manifest, compute_sha256
from dune_ai_monitoring.datasets.planetary import (
    download_asset,
    item_cloud_cover,
    item_datetime,
    search_sentinel2_items,
    select_least_cloudy,
    signed_asset_href,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dune-pc-download",
        description="Download the least-cloudy Sentinel-2 L2A asset from Microsoft Planetary Computer and register it.",
    )
    parser.add_argument("--bbox", required=True, help="Bounding box as min_lon,min_lat,max_lon,max_lat.")
    parser.add_argument("--date-range", required=True, help="Date range as YYYY-MM-DD/YYYY-MM-DD.")
    parser.add_argument("--output", required=True, help="Local file path for the downloaded asset.")
    parser.add_argument("--manifest", default="data/metadata/manifest.csv", help="Manifest CSV path to create or update.")
    parser.add_argument("--asset", default="visual", help="STAC asset key to download, for example visual, B02, B03, B04, or B08.")
    parser.add_argument("--max-cloud-cover", type=float, default=20.0, help="Maximum cloud cover percentage.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum STAC items to inspect.")
    parser.add_argument("--location-name", help="Human-readable site name.")
    parser.add_argument("--latitude", type=float, help="Approximate image or tile centre latitude.")
    parser.add_argument("--longitude", type=float, help="Approximate image or tile centre longitude.")
    parser.add_argument("--stage", help="Optional psammosere stage label.")
    parser.add_argument("--label-source", help="How the label was created.")
    parser.add_argument("--label-confidence", type=float, help="Label confidence from 0.0 to 1.0.")
    parser.add_argument("--notes", help="Short free-text context.")
    return parser


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = build_parser().parse_args(_normalize_bbox_arg(argv))
    bbox = _parse_bbox(args.bbox)
    items = search_sentinel2_items(
        bbox,
        args.date_range,
        max_cloud_cover=args.max_cloud_cover,
        limit=args.limit,
    )
    item = select_least_cloudy(items)
    href = signed_asset_href(item, args.asset)
    output = download_asset(href, args.output)

    cloud_cover = item_cloud_cover(item)
    item_id = item.get("id", "unknown-item")
    notes = args.notes or ""
    provenance_note = f"Planetary Computer item {item_id}; asset {args.asset}"
    if cloud_cover is not None:
        provenance_note = f"{provenance_note}; cloud cover {cloud_cover:g}%"
    notes = f"{notes}; {provenance_note}" if notes else provenance_note

    record = DatasetRecord(
        image_path=output,
        source_name="Microsoft Planetary Computer Sentinel-2 L2A",
        source_url=f"https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items/{item_id}",
        capture_date=item_datetime(item),
        location_name=args.location_name,
        latitude=args.latitude,
        longitude=args.longitude,
        sensor="Sentinel-2 MSI",
        bands=(args.asset,),
        stage=args.stage,
        label_source=args.label_source,
        label_confidence=args.label_confidence,
        sha256=compute_sha256(output),
        license="Copernicus Sentinel data terms",
        notes=notes,
    )
    add_record_to_manifest(args.manifest, record)
    print(f"Downloaded {args.asset} from {item_id} -> {output}")
    print(f"Added manifest row -> {args.manifest}")
    return 0


def _parse_bbox(value: str) -> tuple[float, float, float, float]:
    parts = [float(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must have four comma-separated values")
    min_lon, min_lat, max_lon, max_lat = parts
    if min_lon >= max_lon or min_lat >= max_lat:
        raise argparse.ArgumentTypeError("bbox must be min_lon,min_lat,max_lon,max_lat")
    return min_lon, min_lat, max_lon, max_lat


def _normalize_bbox_arg(argv: list[str] | None) -> list[str] | None:
    if argv is None:
        return None
    normalized = list(argv)
    for index, value in enumerate(normalized[:-1]):
        if value == "--bbox":
            normalized[index] = f"--bbox={normalized[index + 1]}"
            del normalized[index + 1]
            break
    return normalized


if __name__ == "__main__":
    raise SystemExit(main())
