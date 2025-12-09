---
kind: datasource
id: DS-statbel-faillissementen
owner: Statbel
status: active
source_url: https://statbel.fgov.be/nl/open-data/maandevolutie-van-de-faillissementen-volgens-nace
update_frequency: monthly
last_reviewed: 2025-12-09
---

# DS: Statbel Faillissementen

## Description
Monthly evolution of bankruptcies according to NACE codes. This dataset provides information on legal bankruptcies declared by commercial courts.

## Source
- **Main Page**: [Maandevolutie van de faillissementen volgens NACE](https://statbel.fgov.be/nl/open-data/maandevolutie-van-de-faillissementen-volgens-nace)
- **Metadata**: [Method_BANKRUPTCIES.xlsx](https://statbel.fgov.be/sites/default/files/files/opendata/BRI_Nace/Method_BANKRUPTCIES.xlsx)
- **Download URL**: `https://statbel.fgov.be/sites/default/files/files/opendata/BRI_Nace/TF_BANKRUPTCIES.zip` (Note: URL may contain year, e.g., `TF_BANKRUPTCIES(2025).zip`)

## Content
The dataset covers the period from 2005 to present.
Key variables include:
- Reference period (Month/Year)
- NACE code (Economic activity)
- Region / Province / Municipality (NIS codes)
- Legal form of the enterprise
- Number of bankruptcies
- Number of job losses

## Usage
Consumed by `scripts/update_data.py` (download) and `scripts/extract_chart_data_per_province.py` (processing).
Used to generate:
- Monthly bankruptcy trends
- Annual bankruptcy totals
- Comparisons between provinces for the construction sector (NACE 'F').

## Update Frequency
- **Source**: Monthly (approx. 15 days after reference period).
- **Ingestion**: Weekly (Mondays) via `WF-update-data`.
