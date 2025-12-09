---
kind: file
path: js/controls.js
role: ui-controls
workflows: []
inputs: []
outputs: []
interfaces:
  - ControlsManager (class)
stability: legacy
owner: Unknown
safe_to_delete_when: Confirmed unused by any active page
superseded_by: js/dashboard-main.js
last_reviewed: 2025-12-09
---

# File: js/controls.js

## Role
Manages UI controls (tabs, checkboxes, search) for a previous version of the dashboard.

## Why it exists
Legacy UI logic.

## Used by workflows
None known.

## Inputs
- DOM elements for tabs and filters.

## Outputs
- Updates UI state and triggers chart updates via `ChartManager`.

## Interfaces
- `ControlsManager` class.

## Ownership and lifecycle
Legacy. Superseded by `js/dashboard-main.js`.
