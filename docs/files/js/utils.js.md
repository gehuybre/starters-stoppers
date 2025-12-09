---
kind: file
path: js/utils.js
role: utility
workflows: []
inputs: []
outputs: []
interfaces:
  - colorPalette (const)
  - lineStyles (const)
  - getColorForRegion (function)
stability: legacy
owner: Unknown
safe_to_delete_when: Confirmed unused by any active page
superseded_by: null
last_reviewed: 2025-12-09
---

# File: js/utils.js

## Role
Shared utilities and constants, primarily for color palettes and styling.

## Why it exists
To provide consistent styling across the legacy modules (`chart.js`, `map.js`, etc.).

## Used by workflows
None known.

## Inputs
- None.

## Outputs
- Exports constants and helper functions.

## Interfaces
- `colorPalette`, `lineStyles`, `getColorForRegion`, `getLineStyle`, `getColorScale`.

## Ownership and lifecycle
Legacy. The current dashboard seems to define its own colors in `dashboard-charts.js` or `dashboard.css`.
