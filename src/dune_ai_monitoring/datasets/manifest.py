"""CSV dataset manifest helpers with provenance-oriented validation."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

from dune_ai_monitoring.preprocessing.metadata import validate_stage

MANIFEST_FIELDS = (
    "image_path",
    "source_name",
    "source_url",
    "capture_date",
    "location_name",
    "latitude",
    "longitude",
    "sensor",
    "bands",
    "stage",
    "label_source",
    "label_confidence",
    "sha256",
    "license",
    "notes",
)


@dataclass(frozen=True)
class DatasetRecord:
    """One image or tile entry with source, label, and integrity metadata."""

    image_path: Path
    source_name: str
    source_url: str
    capture_date: date | None = None
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    sensor: str | None = None
    bands: tuple[str, ...] = field(default_factory=tuple)
    stage: str | None = None
    label_source: str | None = None
    label_confidence: float | None = None
    sha256: str | None = None
    license: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "image_path", Path(self.image_path))
        object.__setattr__(self, "source_name", _require_text("source_name", self.source_name))
        object.__setattr__(self, "source_url", _require_text("source_url", self.source_url))

        if self.stage:
            object.__setattr__(self, "stage", validate_stage(self.stage))
        if self.capture_date and not isinstance(self.capture_date, date):
            object.__setattr__(self, "capture_date", date.fromisoformat(str(self.capture_date)))
        if self.label_confidence is not None:
            confidence = float(self.label_confidence)
            if confidence < 0.0 or confidence > 1.0:
                raise ValueError("label_confidence must be between 0.0 and 1.0")
            object.__setattr__(self, "label_confidence", confidence)
        if self.latitude is not None:
            latitude = float(self.latitude)
            if latitude < -90.0 or latitude > 90.0:
                raise ValueError("latitude must be between -90 and 90")
            object.__setattr__(self, "latitude", latitude)
        if self.longitude is not None:
            longitude = float(self.longitude)
            if longitude < -180.0 or longitude > 180.0:
                raise ValueError("longitude must be between -180 and 180")
            object.__setattr__(self, "longitude", longitude)
        if self.sha256:
            digest = self.sha256.strip().lower()
            if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
                raise ValueError("sha256 must be a 64-character hexadecimal digest")
            object.__setattr__(self, "sha256", digest)
        object.__setattr__(self, "bands", tuple(str(band).strip() for band in self.bands if str(band).strip()))

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "DatasetRecord":
        """Create a record from a CSV row."""

        return cls(
            image_path=row.get("image_path", ""),
            source_name=row.get("source_name", ""),
            source_url=row.get("source_url", ""),
            capture_date=_optional_date(row.get("capture_date")),
            location_name=_optional_text(row.get("location_name")),
            latitude=_optional_float(row.get("latitude")),
            longitude=_optional_float(row.get("longitude")),
            sensor=_optional_text(row.get("sensor")),
            bands=_split_bands(row.get("bands")),
            stage=_optional_text(row.get("stage")),
            label_source=_optional_text(row.get("label_source")),
            label_confidence=_optional_float(row.get("label_confidence")),
            sha256=_optional_text(row.get("sha256")),
            license=_optional_text(row.get("license")),
            notes=_optional_text(row.get("notes")),
        )

    def to_row(self) -> dict[str, str]:
        """Serialize a record to the project CSV manifest format."""

        return {
            "image_path": self.image_path.as_posix(),
            "source_name": self.source_name,
            "source_url": self.source_url,
            "capture_date": self.capture_date.isoformat() if self.capture_date else "",
            "location_name": self.location_name or "",
            "latitude": _format_optional_number(self.latitude),
            "longitude": _format_optional_number(self.longitude),
            "sensor": self.sensor or "",
            "bands": ";".join(self.bands),
            "stage": self.stage or "",
            "label_source": self.label_source or "",
            "label_confidence": _format_optional_number(self.label_confidence),
            "sha256": self.sha256 or "",
            "license": self.license or "",
            "notes": self.notes or "",
        }


def load_manifest(path: str | Path) -> list[DatasetRecord]:
    """Load and validate a CSV manifest."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(MANIFEST_FIELDS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"manifest is missing required columns: {', '.join(sorted(missing))}")
        return [DatasetRecord.from_row(row) for row in reader]


def write_manifest(path: str | Path, records: Iterable[DatasetRecord]) -> None:
    """Write records to a CSV manifest."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_row())


def add_record_to_manifest(path: str | Path, record: DatasetRecord) -> None:
    """Append a record to a manifest, creating the file if needed."""

    manifest_path = Path(path)
    records = load_manifest(manifest_path) if manifest_path.exists() else []
    records.append(record)
    write_manifest(manifest_path, records)


def validate_manifest(path: str | Path) -> list[str]:
    """Return validation warnings for records that need provenance or label work."""

    warnings = []
    for index, record in enumerate(load_manifest(path), start=2):
        prefix = f"row {index}:"
        if not record.sha256:
            warnings.append(f"{prefix} missing sha256 integrity digest")
        if record.stage and not record.label_source:
            warnings.append(f"{prefix} labelled record is missing label_source")
        if record.stage and record.label_confidence is None:
            warnings.append(f"{prefix} labelled record is missing label_confidence")
        if not record.bands:
            warnings.append(f"{prefix} missing band metadata")
    return warnings


def compute_sha256(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute a file SHA-256 digest for dataset integrity checks."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_text(name: str, value: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{name} is required")
    return text


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _optional_float(value: str | None) -> float | None:
    text = _optional_text(value)
    return float(text) if text is not None else None


def _optional_date(value: str | None) -> date | None:
    text = _optional_text(value)
    return date.fromisoformat(text) if text else None


def _split_bands(value: str | None) -> tuple[str, ...]:
    text = _optional_text(value)
    if not text:
        return ()
    return tuple(part.strip() for part in text.split(";") if part.strip())


def _format_optional_number(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:g}"
