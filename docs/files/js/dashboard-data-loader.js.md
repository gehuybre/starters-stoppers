---
kind: file
path: js/dashboard-data-loader.js
role: data-access
workflows:
  - WF-deploy
inputs:
  - name: CSV Files
    from: data/data-grafieken/
    type: csv
    schema: Standardized CSV structure for charts
outputs:
  - name: Parsed Data
    to: Memory (JavaScript Object)
    type: json
    schema: Structured object mapping files and provinces to data arrays
interfaces:
  - DataLoader (class)
stability: stable
owner: Unknown
safe_to_delete_when: Never
superseded_by: null
last_reviewed: 2025-12-09
---

# File: js/dashboard-data-loader.js

## Role
Responsible for fetching and parsing CSV data files from the server. It handles the mapping between generic filenames and region-specific files (e.g., mapping "Vlaanderen" requests to specific aggregated files).

## Why it exists
To abstract the data fetching logic and file path management away from the main application logic and chart rendering.

## Used by workflows
- [WF-deploy](../workflows/WF-deploy.md) (implicitly, as part of the deployed site)

## Inputs
- **CSV Files**: Fetches files like `Overlevingskans na 1 jaar.csv` from `data/data-grafieken/{Province}/`.

## Outputs
- **Parsed Data**: Returns a nested object structure containing parsed CSV data, organized by file type and province/region.

## Interfaces
- `DataLoader`: Class exposing `loadAllData(selectedProvinces, regions)` and internal CSV parsing methods.

## Ownership and lifecycle
Stable. Core component for data ingestion in the frontend.
