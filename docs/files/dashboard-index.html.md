---
kind: file
path: dashboard-index.html
role: entrypoint
workflows:
  - WF-deploy
inputs:
  - data/data-grafieken/
---

# Dashboard Entry Point

`dashboard-index.html` is the main entry point for the static dashboard. It loads the necessary CSS and JavaScript files to render the visualization interface.

## Features

- **Province Selection**: Interactive buttons to select/deselect provinces or regions.
- **Visualizations**: Renders 8 different charts/tables per province using Chart.js.
- **Data Loading**: Fetches CSV data dynamically via `js/dashboard-data-loader.js`.

## Structure

The HTML file provides the skeleton for:
- **Header**: Navigation and title.
- **Controls**: Province selection grid.
- **Sections**: Containers for each of the 8 metrics (Survival rates, Starters, Bankruptcies, etc.).
- **Footer**: Metadata and credits.

## Dependencies

- **CSS**: `css/layout-template.css`, `css/dashboard.css`
- **JS**: `js/dashboard-main.js`, `js/dashboard-data-loader.js`, `js/dashboard-charts.js`
- **External**: Chart.js (via CDN)

## Usage

Open this file in a browser (via a local server or GitHub Pages) to view the dashboard. It requires the `data/` directory to be populated with CSV files to function correctly.
