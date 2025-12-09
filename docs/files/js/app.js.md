---
kind: file
path: js/app.js
role: controller
workflows: []
inputs: []
outputs: []
interfaces:
  - App (class)
stability: legacy
owner: Unknown
safe_to_delete_when: Confirmed unused by any active page
superseded_by: js/dashboard-main.js
last_reviewed: 2025-12-09
---

# File: js/app.js

## Role
Main application coordinator for a previous version of the dashboard or a different visualization project. It manages `MapManager`, `ChartManager`, `ControlsManager`, etc.

## Why it exists
Legacy entry point. It appears to be designed for a dashboard involving maps (`municipalities_enriched.geojson`) and different data sources (`averages.json`, `cpi.json`).

## Used by workflows
None known.

## Inputs
- Fetches `municipalities_enriched.geojson`, `averages.json`, `cpi.json`, `beleidsdomein_totals.json`.

## Outputs
- Initializes various manager modules.

## Interfaces
- `App` class.

## Ownership and lifecycle
Legacy. Superseded by `js/dashboard-main.js` for the current construction sector dashboard.
