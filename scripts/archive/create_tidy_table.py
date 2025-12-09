#!/usr/bin/env python3
"""
Maak een tidy data tabel voor bouwsector faillissementen en stopzettingen

BELANGRIJKE TERMINOLOGIE:
- "aantal_faillissementen_juridisch" (uit TF_BANKRUPTCIES): Juridische bankruptcies
- "aantal_stopzettingen" (berekend uit TF_VAT_SURVIVALS): Alle beëindigingen
"""

import pandas as pd
import json

def load_bankruptcies_yearly():
    """Laad jaarlijkse faillissementen data"""
    with open('data/processed/bankruptcies_yearly.json', 'r') as f:
        data = json.load(f)
    
    rows = []
    for year_data in data:
        year = year_data['year']
        if year >= 2019:  # Focus op 2019-2024
            bankruptcies = year_data['bankruptcies']
            rows.append({
                'jaar': year,
                'gewest': 'Vlaanderen',
                'aantal_faillissementen': bankruptcies['vlaams_bouw']
            })
            rows.append({
                'jaar': year,
                'gewest': 'Wallonië',
                'aantal_faillissementen': bankruptcies['waals_bouw']
            })
            rows.append({
                'jaar': year,
                'gewest': 'Brussel',
                'aantal_faillissementen': bankruptcies['brussels_bouw']
            })
    
    return pd.DataFrame(rows)

def load_survival_data_by_size():
    """Laad survival data met grootte info (2008 cohort)"""
    df = pd.read_csv('data/TF_VAT_SURVIVALS.txt', sep='|', low_memory=False)
    
    # Strip whitespace
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    # Filter construction sector
    construction = df[
        (df['CD_NACE_LVL1'] == 'F') &
        (df['CD_YEAR'] == 2008)
    ].copy()
    
    # Map regions
    def map_region(code):
        code = str(code).strip() if pd.notna(code) else ''
        # Handle both string and integer formats
        if code in ['02000', '2000', '2']:
            return 'Vlaanderen'
        elif code in ['03000', '3000', '3']:
            return 'Wallonië'
        elif code in ['04000', '4000', '4']:
            return 'Brussel'
        return None
    
    construction['gewest'] = construction['CD_RGN_REFNIS'].apply(map_region)
    construction = construction[construction['gewest'].notna()]
    
    # Map worker classes
    def map_worker_class(code):
        # Convert to int if possible
        try:
            code_int = int(code) if pd.notna(code) else None
        except:
            code_int = None
        
        mapping = {
            1: '0-4 werknemers',
            2: '5-9 werknemers',
            3: '10-49 werknemers',
            4: '50-99 werknemers',
            5: '100+ werknemers'
        }
        return mapping.get(code_int, f'Onbekend ({code})')
    
    construction['grootte'] = construction['CD_CLS_WRKR'].apply(map_worker_class)
    
    # Calculate for 2008 cohort
    construction['aantal_starters'] = construction['MS_CNT_FIRST_REGISTRATIONS']
    construction['aantal_stopzettingen'] = (
        construction['MS_CNT_FIRST_REGISTRATIONS'] - 
        construction['MS_CNT_SURV_YEAR_1']
    )
    
    # Group by region and size
    result = construction.groupby(['gewest', 'grootte'], dropna=False).agg({
        'aantal_starters': 'sum',
        'aantal_stopzettingen': 'sum'
    }).reset_index()
    
    # Filter out rows with 0 values
    result = result[(result['aantal_starters'] > 0) | (result['aantal_stopzettingen'] > 0)]
    
    result['jaar'] = 2008
    
    return result

def create_tidy_table():
    """Maak complete tidy data tabel"""
    print("Maken van tidy data tabel...")
    
    # Laad data met grootte info (2008)
    data_2008 = load_survival_data_by_size()
    print(f"2008 cohort data geladen: {len(data_2008)} rijen")
    
    # Laad 2019-2024 faillissementen (zonder grootte info)
    bankruptcies_recent = load_bankruptcies_yearly()
    print(f"2019-2024 data geladen: {len(bankruptcies_recent)} rijen")
    
    # Voor recente jaren: voeg "Alle groottes" toe
    bankruptcies_recent['grootte'] = 'Alle groottes'
    bankruptcies_recent['aantal_starters'] = None
    # Hernoem kolom: dit zijn echte faillissementen uit TF_BANKRUPTCIES
    bankruptcies_recent = bankruptcies_recent.rename(columns={'aantal_faillissementen': 'aantal_faillissementen_juridisch'})
    
    # Combineer beide datasets
    # Reorder columns voor consistency
    data_2008 = data_2008[['jaar', 'gewest', 'grootte', 'aantal_starters', 'aantal_stopzettingen']]
    data_2008['aantal_faillissementen_juridisch'] = None  # Geen juridische data voor 2008 cohort
    bankruptcies_recent['aantal_stopzettingen'] = None  # Geen survival data voor recente jaren
    bankruptcies_recent = bankruptcies_recent[['jaar', 'gewest', 'grootte', 'aantal_starters', 'aantal_stopzettingen', 'aantal_faillissementen_juridisch']]
    
    tidy_df = pd.concat([data_2008, bankruptcies_recent], ignore_index=True)
    
    # Sort
    tidy_df = tidy_df.sort_values(['jaar', 'gewest', 'grootte']).reset_index(drop=True)
    
    # Convert None to empty string for CSV
    tidy_df['aantal_starters'] = tidy_df['aantal_starters'].fillna('')
    
    # Save
    output_file = 'data/processed/bouwsector_tidy_data.csv'
    tidy_df.to_csv(output_file, index=False)
    print(f"\nOpgeslagen: {output_file}")
    print(f"Totaal rijen: {len(tidy_df)}")
    print(f"\nKolommen: {', '.join(tidy_df.columns)}")
    print(f"\nJaren: {sorted(tidy_df['jaar'].unique())}")
    print(f"Gewesten: {sorted(tidy_df['gewest'].unique())}")
    print(f"Groottes: {sorted(tidy_df['grootte'].unique())}")
    
    # Show sample
    print("\n=== VOORBEELD (eerste 20 rijen) ===")
    print(tidy_df.head(20).to_string(index=False))
    
    return tidy_df

if __name__ == '__main__':
    create_tidy_table()

