"""Dataset metadata structures for labelled dune imagery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DUNE_STAGES = (
    "embryo_dune",
    "yellow_dune",
    "grey_dune",
    "mature_dune_grassland",
    "dune_scrub_or_woodland",
)


@dataclass(frozen=True)
class ImageRecord:
    """Metadata for one labelled source image or tile."""

    image_path: Path
    stage: str
    location: str | None = None
    captured_at: str | None = None
    sensor: str | None = None

    def __post_init__(self) -> None:
        normalized_stage = validate_stage(self.stage)
        object.__setattr__(self, "stage", normalized_stage)
        object.__setattr__(self, "image_path", Path(self.image_path))


def validate_stage(stage: str) -> str:
    """Validate and normalize a psammosere stage label."""

    normalized = stage.strip().lower().replace(" ", "_").replace("-", "_")
    if normalized not in DUNE_STAGES:
        valid = ", ".join(DUNE_STAGES)
        raise ValueError(f"unknown dune stage '{stage}'. Expected one of: {valid}")
    return normalized
