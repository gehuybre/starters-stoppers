---
kind: file
path: scripts/archive/extract_chart_data.py
role: archived
workflows: []
inputs: []
---

# extract_chart_data.py

## Purpose
This script was used to extract chart data from processed CSV files. It has been superseded by `scripts/extract_chart_data_per_province.py` which handles the province-level data extraction required for the current dashboard.

## Status
**Archived**. This file is no longer used in the active data pipeline.

## Inputs
- `data/processed/survival_rates_by_region.csv` (Legacy path)

## Outputs
- CSV files in `data/data-grafieken/` (Legacy structure)
