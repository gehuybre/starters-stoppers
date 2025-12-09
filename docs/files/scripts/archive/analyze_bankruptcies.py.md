---
kind: file
path: scripts/archive/analyze_bankruptcies.py
role: archived
workflows: []
inputs: []
---

# analyze_bankruptcies.py

## Purpose
This script was used to analyze bankruptcy data using pandas. It generated CSV files with various analyses. It is not part of the current automated dashboard update workflow which uses standard Python libraries to minimize dependencies.

## Status
**Archived**. This file is no longer used in the active data pipeline.

## Inputs
- `data/TF_VAT_SURVIVALS.txt`
- `data/TF_BANKRUPTCIES.txt`

## Outputs
- Various analysis CSV files.
