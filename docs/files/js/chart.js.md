---
kind: file
path: js/chart.js
role: visualization
workflows: []
inputs: []
outputs: []
interfaces:
  - ChartManager (class)
stability: legacy
owner: Unknown
safe_to_delete_when: Confirmed unused by any active page
superseded_by: js/dashboard-charts.js
last_reviewed: 2025-12-09
---

# File: js/chart.js

## Role
Chart management module for a previous version of the dashboard. It handles bar charts (`investmentChart`) and small multiples.

## Why it exists
Legacy visualization logic.

## Used by workflows
None known.

## Inputs
- Data from `App` class (municipalities, averages, etc.).

## Outputs
- Renders charts into canvas elements (e.g., `investmentChart`).

## Interfaces
- `ChartManager` class.

## Ownership and lifecycle
Legacy. Superseded by `js/dashboard-charts.js`.
