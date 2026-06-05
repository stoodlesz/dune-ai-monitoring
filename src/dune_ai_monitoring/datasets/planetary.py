"""Planetary Computer STAC helpers for Sentinel-2 imagery."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any
from urllib import parse, request

PLANETARY_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
PLANETARY_SAS_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/token"
SENTINEL2_COLLECTION = "sentinel-2-l2a"


def search_sentinel2_items(
    bbox: tuple[float, float, float, float],
    date_range: str,
    *,
    max_cloud_cover: float = 20.0,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search Planetary Computer for Sentinel-2 L2A STAC items."""

    payload = {
        "collections": [SENTINEL2_COLLECTION],
        "bbox": list(bbox),
        "datetime": date_range,
        "query": {"eo:cloud_cover": {"lt": max_cloud_cover}},
        "limit": limit,
    }
    response = _json_request(PLANETARY_STAC_URL, payload)
    return list(response.get("features", []))


def select_least_cloudy(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Select the least cloudy STAC item from search results."""

    if not items:
        raise ValueError("no Sentinel-2 items matched the search")
    return min(items, key=lambda item: item.get("properties", {}).get("eo:cloud_cover", 100.0))


def signed_asset_href(item: dict[str, Any], asset_key: str) -> str:
    """Return a signed href for one item asset."""

    assets = item.get("assets", {})
    if asset_key not in assets:
        available = ", ".join(sorted(assets))
        raise ValueError(f"asset '{asset_key}' not found. Available assets: {available}")

    token_url = f"{PLANETARY_SAS_URL}/{SENTINEL2_COLLECTION}"
    with request.urlopen(token_url) as response:
        token_payload = json.loads(response.read().decode("utf-8"))
    token = token_payload["token"]
    href = assets[asset_key]["href"]
    separator = "&" if parse.urlparse(href).query else "?"
    return f"{href}{separator}{token}"


def download_asset(href: str, destination: str | Path) -> Path:
    """Download an asset href to a local file."""

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    with request.urlopen(href) as response, path.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return path


def item_datetime(item: dict[str, Any]) -> str | None:
    """Return the date portion of a STAC item's datetime."""

    value = item.get("properties", {}).get("datetime")
    return value[:10] if value else None


def item_cloud_cover(item: dict[str, Any]) -> float | None:
    """Return a STAC item's cloud cover if present."""

    value = item.get("properties", {}).get("eo:cloud_cover")
    return float(value) if value is not None else None


def _json_request(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

