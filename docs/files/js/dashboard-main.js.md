---
kind: file
path: js/dashboard-main.js
role: controller
workflows:
  - WF-deploy
inputs:
  - name: DOM Elements
    from: dashboard-index.html
    type: other
    schema: HTML elements with specific IDs and classes
outputs:
  - name: UI State
    to: DOM
    type: other
    schema: Updates active classes on buttons, toggles visibility of tables
interfaces:
  - Dashboard (class)
stability: stable
owner: Unknown
safe_to_delete_when: Never
superseded_by: null
last_reviewed: 2025-12-09
---

# File: js/dashboard-main.js

## Role
The main controller for the dashboard application. It orchestrates the initialization process, handles user interactions (province selection, region toggles), and coordinates data loading and chart rendering.

## Why it exists
To separate the application logic and event handling from data fetching (`dashboard-data-loader.js`) and visualization (`dashboard-charts.js`).

## Used by workflows
- [WF-deploy](../workflows/WF-deploy.md) (implicitly, as part of the deployed site)

## Inputs
- **DOM Elements**: Interacts with buttons (`.btn-province`, `.btn-region`), chart containers, and table toggles defined in `dashboard-index.html`.

## Outputs
- **UI State**: Updates the visual state of buttons (active/inactive) and visibility of data tables. Triggers chart updates via `ChartsManager`.

## Interfaces
- `Dashboard`: The main class instantiated in the global scope to start the app.

## Ownership and lifecycle
Stable. Core component of the current dashboard.
