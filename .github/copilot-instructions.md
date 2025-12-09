# GitHub Copilot Instructions

## Project Overview
This project is a **static HTML/JS dashboard** visualizing construction sector data (bankruptcies, starters, survival rates) for Belgian provinces. It features a **Python-based data pipeline** that processes raw Statbel Open Data into CSV files consumed by the frontend.

## Architecture

### Frontend (Dashboard)
- **Entry Point**: `dashboard-index.html`
- **Controller**: `js/dashboard-main.js` - Orchestrates UI state, province selection, and data loading.
- **Data Layer**: `js/dashboard-data-loader.js` - Fetches CSV files from `data/data-grafieken/`. Handles mapping between generic filenames and region-specific files.
- **Visualization**: `js/dashboard-charts.js` - Renders charts using **Chart.js**.
- **Styling**: `css/dashboard.css`, `css/layout-template.css`.

### Backend (Data Pipeline)
- **Orchestrator**: `scripts/update_data.py` - Downloads raw zip files (`TF_BANKRUPTCIES`, `TF_VAT_SURVIVALS`) from Statbel and triggers processing.
- **Processor**: `scripts/extract_chart_data_per_province.py` - Parses raw text files and generates structured CSVs in `data/data-grafieken/`.
- **Raw Data**: `data/TF_BANKRUPTCIES.txt`, `data/TF_VAT_SURVIVALS.txt`.
- **Processed Data**: `data/data-grafieken/{ProvinceName}/*.csv`.

## Data Flow
1.  **Ingest**: `scripts/update_data.py` downloads/extracts Statbel data to `data/`.
2.  **Process**: `scripts/extract_chart_data_per_province.py` reads raw data, filters for NACE code "F" (Construction), and splits by province.
3.  **Serve**: Frontend loads CSVs via `fetch()` in `js/dashboard-data-loader.js`.
4.  **Render**: `js/dashboard-charts.js` transforms CSV data into Chart.js datasets.

## Key Conventions & Patterns

### Terminology
- **Faillissementen (Bankruptcies)**: Legal bankruptcies derived from `TF_BANKRUPTCIES`.
- **Stopzettingen (Cessations)**: All business cessations (bankruptcies + voluntary + mergers) derived from `TF_VAT_SURVIVALS`.
- **Starters**: New VAT registrations.

### Region & Province Codes
- **Regions**: Vlaanderen (`02000`), Wallonië (`03000`), Brussel (`04000`).
- **Provinces**: 5-digit NIS codes (e.g., Antwerpen `10000`, Limburg `70000`).
- **Mapping**: See `PROVINCES` dict in `scripts/extract_chart_data_per_province.py`.

### File Structure
- **Do not edit CSVs manually**. They are generated artifacts.
- **Frontend Logic**: Keep logic separated: `main.js` (events), `data-loader.js` (fetch), `charts.js` (render).
- **Python Scripts**: Use `pathlib` for robust path handling.

## Developer Workflow

### Updating Data
To fetch the latest data from Statbel and regenerate CSVs:
```bash
python3 scripts/update_data.py
```

### Frontend Development
- Open `dashboard-index.html` in a browser or use a simple HTTP server (e.g., `python3 -m http.server`).
- When adding new charts:
    1.  Update `scripts/extract_chart_data_per_province.py` to generate the new CSV.
    2.  Update `js/dashboard-data-loader.js` to include the new file in `this.csvFiles`.
    3.  Update `js/dashboard-charts.js` to render the new chart.
    4.  Add canvas element to `dashboard-index.html`.

### Debugging
- **Data Issues**: Check `data/TF_*.txt` headers and content. Statbel formats can change.
- **Frontend**: Use browser console. `Dashboard` instance is global or easily accessible for inspection.

## Documentation
- **Protocol**: Strictly follow the documentation standards defined in `.github/documentation-protocol.md`.
- **Location**: All documentation resides in `docs/`.
- **Updates**: When modifying code that affects workflows, data IO, or entrypoints, you must update the corresponding documentation.
