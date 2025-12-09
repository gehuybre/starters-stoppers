---
kind: file
path: js/map.js
role: visualization
workflows: []
inputs: []
outputs: []
interfaces:
  - MapManager (class)
stability: legacy
owner: Unknown
safe_to_delete_when: Confirmed unused by any active page
superseded_by: null
last_reviewed: 2025-12-09
---

# File: js/map.js

## Role
Map management module using Leaflet.js. Displays a map of municipalities with choropleth coloring.

## Why it exists
Legacy visualization logic for a map-based dashboard. The current dashboard does not appear to use a map.

## Used by workflows
None known.

## Inputs
- GeoJSON data.

## Outputs
- Renders a Leaflet map into the `#map` container.

## Interfaces
- `MapManager` class.

## Ownership and lifecycle
Legacy. No direct replacement in the current dashboard (which focuses on charts).
