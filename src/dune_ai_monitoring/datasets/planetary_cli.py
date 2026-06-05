"""Download Sentinel-2 assets from Microsoft Planetary Computer."""

from __future__ import annotations

import argparse
import math
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
    parser.add_argument("--report", help="Optional Markdown report path describing the downloaded image.")
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
    if args.report:
        write_download_report(args.report, record, bbox, args.asset, item)
    print(f"Downloaded {args.asset} from {item_id} -> {output}")
    print(f"Added manifest row -> {args.manifest}")
    if args.report:
        print(f"Wrote image report -> {args.report}")
    return 0


def write_download_report(
    path: str | Path,
    record: DatasetRecord,
    bbox: tuple[float, float, float, float],
    asset: str,
    item: dict,
) -> Path:
    """Write a human-readable Markdown report for a downloaded image."""

    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    bbox_area_m2 = approximate_bbox_area_m2(bbox)
    cloud_cover = item_cloud_cover(item)
    item_id = item.get("id", "unknown-item")
    lines = [
        f"# {record.location_name or 'Downloaded Sentinel-2 Image'}",
        "",
        "## Image Summary",
        "",
        f"- Local file: `{record.image_path.as_posix()}`",
        f"- Manifest source: `{record.source_url}`",
        f"- Planetary Computer item: `{item_id}`",
        f"- Capture date: {record.capture_date.isoformat() if record.capture_date else 'unknown'}",
        f"- Sensor: {record.sensor or 'unknown'}",
        f"- Downloaded asset: `{asset}`",
        f"- Cloud cover: {_format_optional_percent(cloud_cover)}",
        f"- SHA-256: `{record.sha256 or 'not recorded'}`",
        "",
        "## Area Context",
        "",
        f"- Bounding box: `{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}`",
        f"- Approximate bounding-box area: {bbox_area_m2:,.0f} m^2 ({bbox_area_m2 / 1_000_000:,.2f} km^2)",
        f"- Approximate centre point: {record.latitude or 'unknown'}, {record.longitude or 'unknown'}",
        "",
        "This area value is the size of the search box, not the measured area of sand dunes. Measuring dune area needs a later classification or segmentation step that separates sand, vegetation, water, and urban pixels.",
        "",
        "## Label Context",
        "",
        f"- Stage label: `{record.stage or 'unlabelled'}`",
        f"- Label source: `{record.label_source or 'not recorded'}`",
        f"- Label confidence: {_format_optional_confidence(record.label_confidence)}",
        "",
        "This label is a starting research annotation for the downloaded scene, not a verified pixel-level ecological map.",
        "",
        "## Next Analysis Step",
        "",
        "Use this registered image as input for preprocessing: crop or tile the image, then begin separating visible sand, vegetation, water, and built-up areas before estimating dune extent.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def approximate_bbox_area_m2(bbox: tuple[float, float, float, float]) -> float:
    """Approximate a lon/lat bounding-box area in square metres."""

    min_lon, min_lat, max_lon, max_lat = bbox
    mean_lat = math.radians((min_lat + max_lat) / 2)
    metres_per_degree_lat = 111_320
    metres_per_degree_lon = 111_320 * math.cos(mean_lat)
    width = (max_lon - min_lon) * metres_per_degree_lon
    height = (max_lat - min_lat) * metres_per_degree_lat
    return abs(width * height)


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


def _format_optional_percent(value: float | None) -> str:
    return "unknown" if value is None else f"{value:g}%"


def _format_optional_confidence(value: float | None) -> str:
    return "not recorded" if value is None else f"{value:g}"


if __name__ == "__main__":
    raise SystemExit(main())
