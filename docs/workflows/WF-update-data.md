---
kind: workflow
id: WF-update-data
owner: Unknown
status: active
trigger: schedule (Mon 6:00 UTC), workflow_dispatch, push (scripts/**)
inputs: []
outputs:
  - name: data/
    type: files
    description: Updated CSV files in data/data-grafieken/ and raw text files
entrypoints:
  - .github/workflows/update-data.yml
files:
  - scripts/update_data.py
  - scripts/extract_chart_data_per_province.py
last_reviewed: 2025-12-09
---

# Update Dashboard Data

This workflow automatically updates the dashboard data by downloading the latest statistics from Statbel and processing them into CSV files for the frontend.

## Purpose

To ensure the dashboard always displays the most recent bankruptcy and survival data without manual intervention.

## Process

1.  **Trigger**: Runs weekly on Mondays, manually, or on script changes.
2.  **Setup**: Installs Python dependencies.
3.  **Execution**: Runs `scripts/update_data.py` which:
    - Downloads `TF_BANKRUPTCIES.zip` and `TF_VAT_SURVIVALS.zip` from Statbel.
    - Extracts them to `data/`.
    - Runs `scripts/extract_chart_data_per_province.py` to generate CSVs in `data/data-grafieken/`.
4.  **Commit**: Checks for changes in `data/` and commits them to the repository if any.

## Outputs

- Updates `data/TF_BANKRUPTCIES.txt` and `data/TF_VAT_SURVIVALS.txt`.
- Updates CSV files in `data/data-grafieken/` and its subdirectories.

## Data Flow

```
Statbel.be
    ↓
[GitHub Actions: Download]
    ↓
TF_BANKRUPTCIES.txt + TF_VAT_SURVIVALS.txt
    ↓
[Python Scripts: Process]
    ↓
data/data-grafieken/[Province]/[Charts].csv
    ↓
[Git Commit & Push]
    ↓
GitHub Pages publiceert automatisch
```

## Troubleshooting

- **GitHub Actions fails at download**: Check if Statbel URLs are still valid. Update in `scripts/update_data.py`.
- **No changes detected but data is old**: Statbel might not have updated their data yet. Check their website.
- **Dashboard shows no data**: Verify that `data/data-grafieken/` folders contain CSV files.
- **Charts do not load**: Check browser console (F12) for JavaScript errors.

