# Dune du Pilat

## Image Summary

- Local file: `data/raw/sentinel2/dune_pilat_rendered_preview_2025_07.png`
- Manifest source: `https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items/S2B_MSIL2A_20250711T105619_R094_T30TXQ_20250711T132409`
- Planetary Computer item: `S2B_MSIL2A_20250711T105619_R094_T30TXQ_20250711T132409`
- Capture date: 2025-07-11
- Sensor: Sentinel-2 MSI
- Downloaded asset: `rendered_preview`
- Cloud cover: 0.027724%
- SHA-256: `50d0f2c269cfacf8e14de57f2b90d453b1ebc97de6ae889f73a2f00f6e034699`

## Area Context

- Bounding box: `-1.26,44.55,-1.16,44.63`
- Approximate bounding-box area: 70,600,373 m^2 (70.60 km^2)
- Approximate centre point: 44.589, -1.214

This area value is the size of the search box, not the measured area of sand dunes. Measuring dune area needs a later classification or segmentation step that separates sand, vegetation, water, and urban pixels.

## Label Context

- Stage label: `yellow_dune`
- Label source: `manual_review`
- Label confidence: 0.6

This label is a starting research annotation for the downloaded scene, not a verified pixel-level ecological map.

## Next Analysis Step

Use this registered image as input for preprocessing: crop or tile the image, then begin separating visible sand, vegetation, water, and built-up areas before estimating dune extent.
