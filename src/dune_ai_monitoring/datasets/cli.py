"""Command-line tools for dataset manifests."""

from __future__ import annotations

import argparse
from pathlib import Path

from dune_ai_monitoring.datasets.manifest import DatasetRecord, add_record_to_manifest, compute_sha256


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dune-manifest-add",
        description="Add one downloaded image or tile to a Dune AI Monitoring dataset manifest.",
    )
    parser.add_argument("--manifest", default="data/metadata/manifest.csv", help="Manifest CSV path to create or update.")
    parser.add_argument("--image-path", required=True, help="Local image path to record.")
    parser.add_argument("--source-name", required=True, help="Dataset or provider name.")
    parser.add_argument("--source-url", required=True, help="Dataset source URL or catalogue link.")
    parser.add_argument("--capture-date", help="Capture date in YYYY-MM-DD format.")
    parser.add_argument("--location-name", help="Human-readable site name.")
    parser.add_argument("--latitude", type=float, help="Approximate image or tile centre latitude.")
    parser.add_argument("--longitude", type=float, help="Approximate image or tile centre longitude.")
    parser.add_argument("--sensor", help="Sensor or platform name.")
    parser.add_argument("--bands", help="Semicolon-separated band list, for example 'B2;B3;B4;B8'.")
    parser.add_argument("--stage", help="Optional psammosere stage label.")
    parser.add_argument("--label-source", help="How the label was created, such as manual_review or field_survey.")
    parser.add_argument("--label-confidence", type=float, help="Label confidence from 0.0 to 1.0.")
    parser.add_argument("--license", help="Dataset licence or access terms.")
    parser.add_argument("--notes", help="Short free-text context.")
    parser.add_argument(
        "--allow-missing-file",
        action="store_true",
        help="Create the manifest row without computing sha256 when the image is not present locally.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    image_path = Path(args.image_path)
    if image_path.exists():
        sha256 = compute_sha256(image_path)
    elif args.allow_missing_file:
        sha256 = None
    else:
        raise SystemExit(f"Image file does not exist: {image_path}")

    record = DatasetRecord(
        image_path=image_path,
        source_name=args.source_name,
        source_url=args.source_url,
        capture_date=args.capture_date,
        location_name=args.location_name,
        latitude=args.latitude,
        longitude=args.longitude,
        sensor=args.sensor,
        bands=tuple(args.bands.split(";")) if args.bands else (),
        stage=args.stage,
        label_source=args.label_source,
        label_confidence=args.label_confidence,
        sha256=sha256,
        license=args.license,
        notes=args.notes,
    )
    add_record_to_manifest(args.manifest, record)
    print(f"Added manifest row for {record.image_path} -> {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

