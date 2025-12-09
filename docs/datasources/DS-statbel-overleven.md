---
kind: datasource
id: DS-statbel-overleven
owner: Statbel
status: active
source_url: https://statbel.fgov.be/nl/open-data/overleven-van-de-btw-plichtige-ondernemingen
update_frequency: yearly
last_reviewed: 2025-12-09
---

# DS: Statbel Overleven

## Description
Survival rates of VAT-liable enterprises. This dataset tracks the lifecycle of businesses, including starts, survivals, and cessations (bankruptcies, voluntary stops, mergers).

## Source
- **Main Page**: [Overleven van de btw-plichtige ondernemingen](https://statbel.fgov.be/nl/open-data/overleven-van-de-btw-plichtige-ondernemingen)
- **Metadata**: [VAR_VAT_SURVIVALS.xlsx](https://statbel.fgov.be/sites/default/files/files/opendata/TF_VAT_SURVIVAL/VAR_VAT_SURVIVALS.xlsx)
- **Download URL**: `https://statbel.fgov.be/sites/default/files/files/opendata/TF_VAT_SURVIVAL/TF_VAT_SURVIVALS.zip`

## Content
The dataset covers the period from 2008 to present.
Key variables include:
- Cohort year (Year of start)
- Survival year
- Region / Province (NIS codes)
- Economic activity (NACE-BEL)
- Size class (number of employees)
- Enterprise type (natural/legal person)

## Usage
Consumed by `scripts/update_data.py` (download) and `scripts/extract_chart_data_per_province.py` (processing).
Used to generate:
- 1-year and 3-year survival rates
- Number of new starters per year
- Starters index (2008 = 100)

## Update Frequency
- **Source**: Yearly.
- **Ingestion**: Weekly (Mondays) via `WF-update-data` (checks for updates).
