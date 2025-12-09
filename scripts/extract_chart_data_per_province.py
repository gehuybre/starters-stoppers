"""
Extract data from each chart per PROVINCE and save as separate CSV files.
Creates a subfolder for each province in data/data-grafieken/
"""
import json
import csv
import os
from pathlib import Path
from collections import defaultdict

# Get script directory and set paths relative to dashboard root
SCRIPT_DIR = Path(__file__).parent
DASHBOARD_DIR = SCRIPT_DIR.parent
DATA_DIR = DASHBOARD_DIR / "data"

# Base output directory
base_output_dir = DATA_DIR / "data-grafieken"

# Province codes and names (Dutch names for folder structure)
PROVINCES = {
    "10000": "Antwerpen",
    "20001": "Vlaams-Brabant",
    "20002": "Waals-Brabant",
    "30000": "West-Vlaanderen",
    "40000": "Oost-Vlaanderen",
    "50000": "Henegouwen",
    "60000": "Luik",
    "70000": "Limburg",
    "80000": "Luxemburg",
    "90000": "Namen"
}

# Brussels has no provinces, we'll create a separate folder for it
BRUSSELS_REGION = "04000"

# NACE code for construction
NACE_CONSTRUCTION = "F"


def parse_number(value):
    """Parse number from string, handling empty values"""
    if not value or value == "" or value == "?" or value == "??.??":
        return 0
    try:
        cleaned = str(value).strip().replace(".", "").replace(",", ".")
        return float(cleaned)
    except:
        return 0


def create_province_folders():
    """Create folders for each province"""
    folders = []
    for prov_code, prov_name in PROVINCES.items():
        folder = base_output_dir / prov_name
        folder.mkdir(parents=True, exist_ok=True)
        folders.append((prov_code, prov_name, folder))
    
    # Add Brussels
    brussels_folder = base_output_dir / "Brussels"
    brussels_folder.mkdir(parents=True, exist_ok=True)
    folders.append((BRUSSELS_REGION, "Brussels", brussels_folder))
    
    return folders


def process_survival_data_by_province():
    """Process TF_VAT_SURVIVALS.txt and aggregate by province"""
    print("Processing survival data by province...")
    
    data_file = DATA_DIR / 'TF_VAT_SURVIVALS.txt'
    
    # Structure: {province: {year: {construction/non_construction: [registrations, surv_1, surv_3]}}}
    province_data = defaultdict(lambda: defaultdict(lambda: {
        "construction": [0, 0, 0],
        "non_construction": [0, 0, 0]
    }))
    
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='|')
        
        for row in reader:
            year = row.get('CD_YEAR', row.get('\ufeffCD_YEAR', '')).strip()
            province = row.get('CD_PROV_REFNIS', '').strip()
            nace_lvl1 = row.get('CD_NACE_LVL1', '').strip()
            
            if not year or not nace_lvl1:
                continue
            
            # Handle Brussels (no province code)
            if not province or province == '':
                region = row.get('CD_RGN_REFNIS', '').strip()
                if region == BRUSSELS_REGION:
                    province = BRUSSELS_REGION
                else:
                    continue
            
            # Skip if province not in our list
            if province not in PROVINCES and province != BRUSSELS_REGION:
                continue
            
            # Check if construction sector
            is_construction = (nace_lvl1 == NACE_CONSTRUCTION)
            
            # Parse metrics
            first_reg = parse_number(row.get('MS_CNT_FIRST_REGISTRATIONS', '0'))
            surv_1 = parse_number(row.get('MS_CNT_SURV_YEAR_1', '0'))
            surv_3 = parse_number(row.get('MS_CNT_SURV_YEAR_3', '0'))
            
            if first_reg == 0:
                continue
            
            # Aggregate
            sector_key = "construction" if is_construction else "non_construction"
            province_data[province][year][sector_key][0] += first_reg
            province_data[province][year][sector_key][1] += surv_1
            province_data[province][year][sector_key][2] += surv_3
    
    return province_data


def process_bankruptcy_trend_by_province():
    """Process bankruptcy trend data by province from TF_BANKRUPTCIES.txt"""
    print("Processing bankruptcies by province (yearly aggregation)...")
    
    data_file = DATA_DIR / 'TF_BANKRUPTCIES.txt'
    
    # Structure: {province: {year_month: {construction/non_construction: count}}}
    province_data = defaultdict(lambda: defaultdict(lambda: {
        "construction": 0,
        "non_construction": 0
    }))
    
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='|')
        
        for row in reader:
            year = row.get('CD_YEAR', '').strip()
            month = row.get('CD_MONTH', '').strip()
            province = row.get('CD_PROV_REFNIS', '').strip()
            nace_section = row.get('TX_NACE_REV2_SECTION', '').strip()
            bankruptcies = parse_number(row.get('MS_COUNTOF_BANKRUPTCIES', '0'))
            
            if not year or not month or bankruptcies == 0:
                continue
            
            # Handle Brussels
            if not province or province == '':
                region = row.get('CD_RGN_REFNIS', '').strip()
                if region == BRUSSELS_REGION:
                    province = BRUSSELS_REGION
                else:
                    continue
            
            if province not in PROVINCES and province != BRUSSELS_REGION:
                continue
            
            # Check if construction
            is_construction = (nace_section == NACE_CONSTRUCTION)
            
            year_month = f"{year}-{month.zfill(2)}"
            sector_key = "construction" if is_construction else "non_construction"
            province_data[province][year_month][sector_key] += bankruptcies
    
    return province_data


def calculate_12month_rolling(monthly_data):
    """Calculate 12-month rolling sum"""
    sorted_dates = sorted(monthly_data.keys())
    rolling_data = {}
    
    for i, date in enumerate(sorted_dates):
        if i < 11:  # Need at least 12 months
            continue
        
        # Sum last 12 months
        last_12 = sorted_dates[i-11:i+1]
        construction_sum = sum(monthly_data[d]["construction"] for d in last_12)
        non_construction_sum = sum(monthly_data[d]["non_construction"] for d in last_12)
        
        rolling_data[date] = {
            "construction": construction_sum,
            "non_construction": non_construction_sum
        }
    
    return rolling_data


def process_bankruptcy_yearly_by_province():
    """Process yearly bankruptcy data by province"""
    print("Processing yearly bankruptcy data by province...")
    
    data_file = DATA_DIR / 'TF_BANKRUPTCIES.txt'
    
    # Structure: {province: {year: {construction/non_construction: count}}}
    province_data = defaultdict(lambda: defaultdict(lambda: {
        "construction": 0,
        "non_construction": 0
    }))
    
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='|')
        
        for row in reader:
            year = row.get('CD_YEAR', '').strip()
            province = row.get('CD_PROV_REFNIS', '').strip()
            nace_section = row.get('TX_NACE_REV2_SECTION', '').strip()
            bankruptcies = parse_number(row.get('MS_COUNTOF_BANKRUPTCIES', '0'))
            
            if not year or bankruptcies == 0:
                continue
            
            # Handle Brussels
            if not province or province == '':
                region = row.get('CD_RGN_REFNIS', '').strip()
                if region == BRUSSELS_REGION:
                    province = BRUSSELS_REGION
                else:
                    continue
            
            if province not in PROVINCES and province != BRUSSELS_REGION:
                continue
            
            is_construction = (nace_section == NACE_CONSTRUCTION)
            sector_key = "construction" if is_construction else "non_construction"
            province_data[province][year][sector_key] += bankruptcies
    
    return province_data


def create_csv_files_per_province():
    """Create all CSV files for each province"""
    
    # Create folders
    folders = create_province_folders()
    print(f"Created folders for {len(folders)} provinces/regions")
    
    # Load survival data
    survival_data = process_survival_data_by_province()
    
    # Load bankruptcy data
    bankruptcy_monthly = process_bankruptcy_trend_by_province()
    bankruptcy_yearly = process_bankruptcy_yearly_by_province()
    
    # Process each province
    for prov_code, prov_name, folder in folders:
        print(f"\n=== Processing {prov_name} ===")
        
        # Get data for this province
        prov_survival = survival_data.get(prov_code, {})
        prov_bankruptcy_monthly = bankruptcy_monthly.get(prov_code, {})
        prov_bankruptcy_yearly = bankruptcy_yearly.get(prov_code, {})
        
        # 1. Overlevingskans na 1 jaar
        create_survival_1year_csv(folder, prov_survival, prov_name)
        
        # 2. Overlevingskans na 3 jaar
        create_survival_3year_csv(folder, prov_survival, prov_name)
        
        # 3. Nieuwe starters bouwsector
        create_starters_csv(folder, prov_survival, prov_name)
        
        # 4. Faillissementen bouwsector (yearly)
        create_bankruptcies_yearly_csv(folder, prov_bankruptcy_yearly, prov_name)
        
        # 5. 12-maandelijkse trend faillissementen (index 2008 = 100)
        create_bankruptcy_trend_index_csv(folder, prov_bankruptcy_monthly, prov_name)
        
        # 6. 12-maandelijkse trend faillissementen bouwsector (absolute)
        create_bankruptcy_trend_absolute_csv(folder, prov_bankruptcy_monthly, prov_name)
        
        # 7. Nieuwe starters (index 2008 = 100)
        create_starters_index_csv(folder, prov_survival, prov_name)
        
        # 8. Jaarlijkse cijfers bouwsector (sinds 2016)
        create_yearly_summary_csv(folder, prov_survival, prov_bankruptcy_yearly, prov_name)


def create_survival_1year_csv(folder, survival_data, prov_name):
    """Chart 1: Overlevingskans na 1 jaar"""
    rows = []
    
    for year, sectors in sorted(survival_data.items()):
        year_int = int(year)
        display_year = year_int + 1  # Measured after 1 year
        
        construction = sectors["construction"]
        non_construction = sectors["non_construction"]
        
        if construction[0] > 0:  # Has registrations
            survival_rate = (construction[1] / construction[0]) * 100
            rows.append({
                'Provincie': prov_name,
                'Jaar': display_year,
                'Bouwsector (%)': round(survival_rate, 2),
            })
        
        if non_construction[0] > 0:
            survival_rate = (non_construction[1] / non_construction[0]) * 100
            # Add non-construction in separate row or column as needed
    
    if rows:
        with open(folder / 'Overlevingskans na 1 jaar.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Provincie', 'Jaar', 'Bouwsector (%)'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: Overlevingskans na 1 jaar.csv ({len(rows)} records)")


def create_survival_3year_csv(folder, survival_data, prov_name):
    """Chart 2: Overlevingskans na 3 jaar"""
    rows = []
    
    for year, sectors in sorted(survival_data.items()):
        year_int = int(year)
        
        # Only include years where 3-year data is available (up to 2021)
        if year_int > 2021:
            continue
        
        display_year = year_int + 3
        
        construction = sectors["construction"]
        
        if construction[0] > 0 and construction[2] > 0:
            survival_rate = (construction[2] / construction[0]) * 100
            rows.append({
                'Provincie': prov_name,
                'Jaar': display_year,
                'Bouwsector (%)': round(survival_rate, 2),
            })
    
    if rows:
        with open(folder / 'Overlevingskans na 3 jaar.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Provincie', 'Jaar', 'Bouwsector (%)'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: Overlevingskans na 3 jaar.csv ({len(rows)} records)")


def create_starters_csv(folder, survival_data, prov_name):
    """Chart 3: Nieuwe starters bouwsector"""
    rows = []
    
    for year, sectors in sorted(survival_data.items()):
        construction = sectors["construction"]
        
        if construction[0] > 0:
            rows.append({
                'Jaar': int(year),
                'Aantal nieuwe starters': int(construction[0])
            })
    
    if rows:
        with open(folder / 'Nieuwe starters bouwsector.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Jaar', 'Aantal nieuwe starters'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: Nieuwe starters bouwsector.csv ({len(rows)} records)")


def create_bankruptcies_yearly_csv(folder, bankruptcy_yearly, prov_name):
    """Chart 4: Faillissementen bouwsector (yearly)"""
    rows = []
    
    for year, sectors in sorted(bankruptcy_yearly.items()):
        year_int = int(year)
        if year_int >= 2005:
            bankruptcies = int(sectors["construction"])
            rows.append({
                'Jaar': year_int,
                'Aantal faillissementen': bankruptcies
            })
    
    if rows:
        with open(folder / 'Faillissementen bouwsector.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Jaar', 'Aantal faillissementen'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: Faillissementen bouwsector.csv ({len(rows)} records)")


def create_bankruptcy_trend_index_csv(folder, bankruptcy_monthly, prov_name):
    """Chart 5: 12-maandelijkse trend (index 2008 = 100)"""
    
    # Calculate 12-month rolling
    rolling_data = calculate_12month_rolling(bankruptcy_monthly)
    
    # Find base values for 2008
    base_2008 = None
    for date in sorted(rolling_data.keys()):
        if date.startswith('2008'):
            base_2008 = rolling_data[date]
            break
    
    if not base_2008 or base_2008["construction"] == 0:
        print(f"   Skipped: 12-maandelijkse trend (index) - no 2008 base data")
        return
    
    rows = []
    for date, sectors in sorted(rolling_data.items()):
        if sectors["construction"] > 0 or sectors["non_construction"] > 0:
            rows.append({
                'Jaar-Maand': date,
                'Bouwsector (index)': round((sectors["construction"] / base_2008["construction"]) * 100, 2),
                'Niet-bouwsector (index)': round((sectors["non_construction"] / base_2008["non_construction"]) * 100, 2) if base_2008["non_construction"] > 0 else 0
            })
    
    if rows:
        with open(folder / '12-maandelijkse trend faillissementen (index 2008 = 100).csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Jaar-Maand', 'Bouwsector (index)', 'Niet-bouwsector (index)'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: 12-maandelijkse trend (index).csv ({len(rows)} records)")


def create_bankruptcy_trend_absolute_csv(folder, bankruptcy_monthly, prov_name):
    """Chart 6: 12-maandelijkse trend bouwsector (absolute)"""
    
    rolling_data = calculate_12month_rolling(bankruptcy_monthly)
    
    rows = []
    for date, sectors in sorted(rolling_data.items()):
        if sectors["construction"] > 0:
            rows.append({
                'Jaar-Maand': date,
                'Aantal faillissementen (12-maands som)': int(sectors["construction"])
            })
    
    if rows:
        with open(folder / '12-maandelijkse trend faillissementen bouwsector (absolute cijfers).csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Jaar-Maand', 'Aantal faillissementen (12-maands som)'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: 12-maandelijkse trend (absolute).csv ({len(rows)} records)")


def create_starters_index_csv(folder, survival_data, prov_name):
    """Chart 7: Nieuwe starters (index 2008 = 100)"""
    
    # Find 2008 base values
    base_2008 = survival_data.get('2008')
    if not base_2008 or base_2008["construction"][0] == 0:
        print(f"   Skipped: Nieuwe starters (index) - no 2008 base data")
        return
    
    base_construction = base_2008["construction"][0]
    base_non_construction = base_2008["non_construction"][0]
    
    rows = []
    for year, sectors in sorted(survival_data.items()):
        construction = sectors["construction"]
        non_construction = sectors["non_construction"]
        
        if construction[0] > 0:
            rows.append({
                'Provincie': prov_name,
                'Jaar': int(year),
                'Bouwsector (index)': round((construction[0] / base_construction) * 100, 2),
                'Niet-bouwsector (index)': round((non_construction[0] / base_non_construction) * 100, 2) if base_non_construction > 0 else 0
            })
    
    if rows:
        with open(folder / 'Nieuwe starters (index 2008 = 100).csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Provincie', 'Jaar', 'Bouwsector (index)', 'Niet-bouwsector (index)'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: Nieuwe starters (index).csv ({len(rows)} records)")


def create_yearly_summary_csv(folder, survival_data, bankruptcy_yearly, prov_name):
    """Chart 8: Jaarlijkse cijfers bouwsector (sinds 2016)"""
    rows = []
    
    for year, sectors in sorted(survival_data.items(), reverse=True):
        year_int = int(year)
        
        if year_int < 2016:
            continue
        
        construction = sectors["construction"]
        
        # Calculate 1-year survival rate
        if construction[0] > 0 and construction[1] > 0:
            survival_1yr = (construction[1] / construction[0]) * 100
        else:
            survival_1yr = 0
        
        # Calculate 3-year survival rate (only available up to 2021)
        if year_int <= 2021 and construction[0] > 0 and construction[2] > 0:
            survival_3yr = (construction[2] / construction[0]) * 100
        else:
            survival_3yr = None
        
        # Get bankruptcies
        bankruptcies = 0
        if str(year_int) in bankruptcy_yearly:
            bankruptcies = int(bankruptcy_yearly[str(year_int)]["construction"])
        
        rows.append({
            'Jaar': year_int,
            '1-jarige overlevingskans (%)': round(survival_1yr, 2) if survival_1yr > 0 else '-',
            '3-jarige overlevingskans (%)': round(survival_3yr, 2) if survival_3yr else '-',
            'Nieuwe starters': int(construction[0]),
            'Jaarlijkse faillissementen': bankruptcies
        })
    
    if rows:
        with open(folder / 'Jaarlijkse cijfers bouwsector (sinds 2016).csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Jaar',
                '1-jarige overlevingskans (%)',
                '3-jarige overlevingskans (%)',
                'Nieuwe starters',
                'Jaarlijkse faillissementen'
            ])
            writer.writeheader()
            writer.writerows(rows)
        print(f"   Created: Jaarlijkse cijfers bouwsector (sinds 2016).csv ({len(rows)} records)")


if __name__ == "__main__":
    print("=" * 80)
    print("Extracting chart data per PROVINCE")
    print("=" * 80)
    
    create_csv_files_per_province()
    
    print("\n" + "=" * 80)
    print("✅ All CSV files created per province!")
    print(f"📁 Output location: {base_output_dir}")
    print("=" * 80)
