---
kind: file
path: js/dashboard-charts.js
role: visualization
workflows:
  - WF-deploy
inputs:
  - name: Parsed Data
    from: DataLoader
    type: json
    schema: Structured data object
outputs:
  - name: Charts
    to: Canvas Elements
    type: other
    schema: Chart.js instances rendered into <canvas> tags
interfaces:
  - ChartsManager (class)
stability: stable
owner: Unknown
safe_to_delete_when: Never
superseded_by: null
last_reviewed: 2025-12-09
---

# File: js/dashboard-charts.js

## Role
Manages the creation, update, and destruction of Chart.js instances. It transforms the raw data provided by `DataLoader` into the format required by Chart.js datasets.

## Why it exists
To encapsulate all visualization logic, including chart configuration, styling (colors, fonts), and data transformation for specific chart types (line charts, bar charts).

## Used by workflows
- [WF-deploy](../workflows/WF-deploy.md) (implicitly, as part of the deployed site)

## Inputs
- **Parsed Data**: Receives data objects from `DataLoader`.

## Outputs
- **Charts**: Renders visual charts into the `<canvas>` elements defined in the HTML. Populates HTML tables with data.

## Interfaces
- `ChartsManager`: Class exposing `createAllCharts(data, selectedProvinces)` and specific methods for each of the 8 chart types.

## Ownership and lifecycle
Stable. Core component for visualization.
