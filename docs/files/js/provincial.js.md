---
kind: file
path: js/provincial.js
role: visualization
workflows: []
inputs: []
outputs: []
interfaces:
  - ProvincialManager (class)
stability: legacy
owner: Unknown
safe_to_delete_when: Confirmed unused by any active page
superseded_by: null
last_reviewed: 2025-12-09
---

# File: js/provincial.js

## Role
Visualization module for provincial data, likely for a different dataset (financial accounts/rekeningen).

## Why it exists
Legacy visualization logic. It fetches `provincie_totals.json`, `provincie_detailed.json`, etc., which are different from the current dashboard's CSV data sources.

## Used by workflows
None known.

## Inputs
- JSON data files (`provincie_totals.json`, etc.).

## Outputs
- Renders charts and tables.

## Interfaces
- `ProvincialManager` class.

## Ownership and lifecycle
Legacy.
