"""
Extract data from each chart in the HTML dashboard and save as separate CSV files.
"""
import json
import csv
import os
from pathlib import Path

# Create output directory
output_dir = Path('data/data-grafieken')
output_dir.mkdir(parents=True, exist_ok=True)

# Load all data sources
print("Loading data sources...")

# 1. Load CSV data (survival rates)
csv_data = []
with open('data/processed/survival_rates_by_region.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_data.append({
            'gewest': row['Gewest'],
            'year': int(row['Year']),
            'bouwsector_1jaar': float(row['Bouwsector_1jaar']),
            'nietBouwsector_1jaar': float(row['Niet-bouwsector_1jaar']),
            'bouwsector_3jaar': float(row['Bouwsector_3jaar']),
            'nietBouwsector_3jaar': float(row['Niet-bouwsector_3jaar']),
            'bouwsector_starters': float(row['Bouwsector_starters']),
            'nietBouwsector_starters': float(row['Niet-bouwsector_starters'])
        })

# 2. Load bankruptcy trend data
with open('data/processed/bankruptcies_12month_trend.json', 'r') as f:
    bankruptcy_trend_data = json.load(f)

# 3. Load bankruptcy yearly data
with open('data/processed/bankruptcies_yearly.json', 'r') as f:
    bankruptcy_yearly_data = json.load(f)

print(f"Loaded {len(csv_data)} survival records")
print(f"Loaded {len(bankruptcy_trend_data)} bankruptcy trend records")
print(f"Loaded {len(bankruptcy_yearly_data)} bankruptcy yearly records")
print("Using TF_VAT_SURVIVALS data for all starter counts")

# Chart 1: Overlevingskans na 1 jaar
print("\n1. Creating 'Overlevingskans na 1 jaar.csv'...")
chart1_data = []
regions = ['Vlaams Gewest', 'Waals Gewest', 'Brussels Gewest']
for region in regions:
    region_data = [d for d in csv_data if d['gewest'] == region]
    for record in region_data:
        # Display year is creation year + 1 (when survival is measured)
        display_year = record['year'] + 1
        chart1_data.append({
            'Gewest': region,
            'Jaar': display_year,
            'Bouwsector (%)': record['bouwsector_1jaar'],
            'Niet-bouwsector (%)': record['nietBouwsector_1jaar']
        })

with open(output_dir / 'Overlevingskans na 1 jaar.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Gewest', 'Jaar', 'Bouwsector (%)', 'Niet-bouwsector (%)'])
    writer.writeheader()
    writer.writerows(chart1_data)
print(f"   Saved {len(chart1_data)} records")

# Chart 2: Overlevingskans na 3 jaar
print("\n2. Creating 'Overlevingskans na 3 jaar.csv'...")
chart2_data = []
for region in regions:
    # Filter out 2022 and 2023 (no 3-year survival data)
    region_data = [d for d in csv_data if d['gewest'] == region and d['year'] <= 2021]
    for record in region_data:
        # Display year is creation year + 3 (when survival is measured)
        display_year = record['year'] + 3
        chart2_data.append({
            'Gewest': region,
            'Jaar': display_year,
            'Bouwsector (%)': record['bouwsector_3jaar'],
            'Niet-bouwsector (%)': record['nietBouwsector_3jaar']
        })

with open(output_dir / 'Overlevingskans na 3 jaar.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Gewest', 'Jaar', 'Bouwsector (%)', 'Niet-bouwsector (%)'])
    writer.writeheader()
    writer.writerows(chart2_data)
print(f"   Saved {len(chart2_data)} records")

# Chart 3: Nieuwe starters Vlaamse bouwsector (absolute)
print("\n3. Creating 'Nieuwe starters Vlaamse bouwsector.csv'...")
# Use TF_VAT_SURVIVALS data (csv_data) instead of external JSON
vlaams_data = [d for d in csv_data if d['gewest'] == 'Vlaams Gewest']
chart3_data = [
    {'Jaar': record['year'], 'Aantal nieuwe starters': int(record['bouwsector_starters'])}
    for record in vlaams_data
]

with open(output_dir / 'Nieuwe starters Vlaamse bouwsector.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Jaar', 'Aantal nieuwe starters'])
    writer.writeheader()
    writer.writerows(chart3_data)
print(f"   Saved {len(chart3_data)} records")

# Chart 4: Faillissementen Vlaamse bouwsector (absolute, yearly)
print("\n4. Creating 'Faillissementen Vlaamse bouwsector.csv'...")
chart4_data = []
for record in bankruptcy_yearly_data:
    if record['year'] >= 2005:
        bankruptcies = record.get('bankruptcies', {}).get('vlaams_bouw', 0)
        chart4_data.append({
            'Jaar': record['year'],
            'Aantal faillissementen': int(bankruptcies)
        })
chart4_data.sort(key=lambda x: x['Jaar'])

with open(output_dir / 'Faillissementen Vlaamse bouwsector.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Jaar', 'Aantal faillissementen'])
    writer.writeheader()
    writer.writerows(chart4_data)
print(f"   Saved {len(chart4_data)} records")

# Chart 5: 12-maandelijkse trend faillissementen (index 2008 = 100)
print("\n5. Creating '12-maandelijkse trend faillissementen (index 2008 = 100).csv'...")
# Find base values for 2008
base_2008 = next((d for d in bankruptcy_trend_data if d['year'] == 2008 and d['month'] == 12), None)
if not base_2008:
    base_2008 = next((d for d in bankruptcy_trend_data if d['year'] == 2008), None)

chart5_data = []
for record in bankruptcy_trend_data:
    if any([record.get('vlaams_bouw', 0) > 0, record.get('vlaams_niet_bouw', 0) > 0,
            record.get('waals_bouw', 0) > 0, record.get('waals_niet_bouw', 0) > 0,
            record.get('brussels_bouw', 0) > 0, record.get('brussels_niet_bouw', 0) > 0]):
        
        row = {
            'Jaar-Maand': record['date'],
            'Vlaams Gewest - Bouwsector': round((record.get('vlaams_bouw', 0) / base_2008['vlaams_bouw']) * 100, 2) if base_2008 else 0,
            'Vlaams Gewest - Niet-bouwsector': round((record.get('vlaams_niet_bouw', 0) / base_2008['vlaams_niet_bouw']) * 100, 2) if base_2008 else 0,
            'Waals Gewest - Bouwsector': round((record.get('waals_bouw', 0) / base_2008['waals_bouw']) * 100, 2) if base_2008 else 0,
            'Waals Gewest - Niet-bouwsector': round((record.get('waals_niet_bouw', 0) / base_2008['waals_niet_bouw']) * 100, 2) if base_2008 else 0,
            'Brussels Gewest - Bouwsector': round((record.get('brussels_bouw', 0) / base_2008['brussels_bouw']) * 100, 2) if base_2008 else 0,
            'Brussels Gewest - Niet-bouwsector': round((record.get('brussels_niet_bouw', 0) / base_2008['brussels_niet_bouw']) * 100, 2) if base_2008 else 0
        }
        chart5_data.append(row)

with open(output_dir / '12-maandelijkse trend faillissementen (index 2008 = 100).csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'Jaar-Maand', 
        'Vlaams Gewest - Bouwsector', 
        'Vlaams Gewest - Niet-bouwsector',
        'Waals Gewest - Bouwsector',
        'Waals Gewest - Niet-bouwsector',
        'Brussels Gewest - Bouwsector',
        'Brussels Gewest - Niet-bouwsector'
    ])
    writer.writeheader()
    writer.writerows(chart5_data)
print(f"   Saved {len(chart5_data)} records")

# Chart 6: 12-maandelijkse trend faillissementen Vlaamse bouwsector (absolute cijfers)
print("\n6. Creating '12-maandelijkse trend faillissementen Vlaamse bouwsector (absolute cijfers).csv'...")
chart6_data = []
for record in bankruptcy_trend_data:
    if record.get('vlaams_bouw', 0) > 0:
        chart6_data.append({
            'Jaar-Maand': record['date'],
            'Aantal faillissementen (12-maands som)': int(record['vlaams_bouw'])
        })

with open(output_dir / '12-maandelijkse trend faillissementen Vlaamse bouwsector (absolute cijfers).csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Jaar-Maand', 'Aantal faillissementen (12-maands som)'])
    writer.writeheader()
    writer.writerows(chart6_data)
print(f"   Saved {len(chart6_data)} records")

# Chart 7: Nieuwe starters (index 2008 = 100)
print("\n7. Creating 'Nieuwe starters (index 2008 = 100).csv'...")
# Calculate base values for 2008
base_values = {}
for region in regions:
    region_2008 = next((d for d in csv_data if d['gewest'] == region and d['year'] == 2008), None)
    if region_2008:
        base_values[region] = {
            'bouwsector': region_2008['bouwsector_starters'],
            'nietBouwsector': region_2008['nietBouwsector_starters']
        }

chart7_data = []
for region in regions:
    region_data = [d for d in csv_data if d['gewest'] == region]
    for record in region_data:
        if region in base_values:
            bouw_index = (record['bouwsector_starters'] / base_values[region]['bouwsector']) * 100
            niet_bouw_index = (record['nietBouwsector_starters'] / base_values[region]['nietBouwsector']) * 100
            chart7_data.append({
                'Gewest': region,
                'Jaar': record['year'],
                'Bouwsector (index)': round(bouw_index, 2),
                'Niet-bouwsector (index)': round(niet_bouw_index, 2)
            })

with open(output_dir / 'Nieuwe starters (index 2008 = 100).csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Gewest', 'Jaar', 'Bouwsector (index)', 'Niet-bouwsector (index)'])
    writer.writeheader()
    writer.writerows(chart7_data)
print(f"   Saved {len(chart7_data)} records")

# Chart 8: Jaarlijkse cijfers Vlaanderen bouwsector (data table, since 2016)
print("\n8. Creating 'Jaarlijkse cijfers Vlaanderen bouwsector (sinds 2016).csv'...")
vlaams_data = [d for d in csv_data if d['gewest'] == 'Vlaams Gewest' and d['year'] >= 2016]
chart8_data = []

for record in sorted(vlaams_data, key=lambda x: x['year'], reverse=True):
    year = record['year']
    bankruptcy_data = next((d for d in bankruptcy_yearly_data if d['year'] == year), None)
    bankruptcies = bankruptcy_data.get('bankruptcies', {}).get('vlaams_bouw', 0) if bankruptcy_data else 0
    
    # Use starters from TF_VAT_SURVIVALS (csv_data)
    starters_value = record['bouwsector_starters']
    
    # 3-year survival (0.0 means no data available)
    survival_3jaar = record['bouwsector_3jaar'] if record['bouwsector_3jaar'] > 0 else None
    
    chart8_data.append({
        'Jaar': year,
        '1-jarige overlevingskans (%)': round(record['bouwsector_1jaar'], 2),
        '3-jarige overlevingskans (%)': round(survival_3jaar, 2) if survival_3jaar else '-',
        'Nieuwe starters': int(starters_value),
        'Jaarlijkse faillissementen': int(bankruptcies)  # Uit TF_BANKRUPTCIES = juridische faillissementen
    })

with open(output_dir / 'Jaarlijkse cijfers Vlaanderen bouwsector (sinds 2016).csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'Jaar',
        '1-jarige overlevingskans (%)',
        '3-jarige overlevingskans (%)',
        'Nieuwe starters',
        'Jaarlijkse faillissementen'
    ])
    writer.writeheader()
    writer.writerows(chart8_data)
print(f"   Saved {len(chart8_data)} records")

print(f"\n✅ All chart data exported to {output_dir}/")
print("\nCreated files:")
for csv_file in sorted(output_dir.glob('*.csv')):
    print(f"   - {csv_file.name}")
