#!/usr/bin/env python3
"""
Analyse faillissementen in de bouwsector
Genereert CSV bestanden met verschillende analyses

BELANGRIJKE TERMINOLOGIE:
- "Faillissementen" (uit TF_BANKRUPTCIES): Juridische bankruptcies
- "Stopzettingen" (berekend uit TF_VAT_SURVIVALS): Alle beëindigingen
  (faillissementen + vrijwillige stopzettingen + fusies + liquidaties)
"""

import pandas as pd
import json
from collections import defaultdict

def load_survival_data():
    """Laad de survival data"""
    print("Laden van data...")
    df = pd.read_csv('data/TF_VAT_SURVIVALS.txt', sep='|', low_memory=False, dtype={'CD_RGN_REFNIS': str, 'CD_YEAR': int})
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

def map_region_code(code):
    """Map region codes to names"""
    code = str(code).strip() if pd.notna(code) else ''
    if code == '02000':
        return 'Vlaanderen'
    elif code == '03000':
        return 'Wallonië'
    elif code == '04000':
        return 'Brussel'
    else:
        return None

def map_worker_class(code, nl_desc):
    """Map worker class codes to readable names"""
    mapping = {
        '01': '0-4 werknemers',
        '02': '5-9 werknemers',
        '03': '10-49 werknemers',
        '04': '50+ werknemers'
    }
    return mapping.get(code, nl_desc)

def generate_regional_breakdown():
    """Genereer faillissementen per gewest 2019-2024 van bestaande data"""
    print("\n1. Berekenen faillissementen per gewest (2019-2024)...")
    
    # Load existing bankruptcies data
    with open('data/processed/bankruptcies_yearly.json', 'r') as f:
        yearly_data = json.load(f)
    
    results = []
    for year_data in yearly_data:
        year = year_data['year']
        if 2019 <= year <= 2024:
            bankruptcies = year_data['bankruptcies']
            results.append({
                'Jaar': year,
                'Vlaanderen': bankruptcies['vlaams_bouw'],
                'Wallonië': bankruptcies['waals_bouw'],
                'Brussel': bankruptcies['brussels_bouw']
            })
    
    result_df = pd.DataFrame(results)
    result_df.to_csv('data/processed/faillissementen_per_gewest_2019_2024.csv', index=False)
    print(f"   Opgeslagen: faillissementen_per_gewest_2019_2024.csv")
    print(f"   Rijen: {len(result_df)}")
    
    return result_df

def generate_company_size_2024(df):
    """Genereer faillissementen per omvang voor 2008 cohort per gewest"""
    print("\n2. Berekenen faillissementen per omvang (2008 cohort)...")
    print("   OPMERKING: Data voor 2024 niet beschikbaar in survival dataset")
    print("   Genereren data voor 2008 cohort als voorbeeld...")
    
    # Filter construction sector for 2008
    construction_2008 = df[
        (df['CD_NACE_LVL1'] == 'F') &
        (df['CD_YEAR'] == 2008)
    ].copy()
    
    # Map regions and worker classes
    construction_2008['Gewest'] = construction_2008['CD_RGN_REFNIS'].apply(map_region_code)
    construction_2008['Werknemersklasse'] = construction_2008.apply(
        lambda x: map_worker_class(x['CD_CLS_WRKR'], x['TX_CLS_WRKR_NL']), axis=1
    )
    
    construction_2008 = construction_2008[construction_2008['Gewest'].notna()]
    
    # Calculate failures in year 1
    construction_2008['Faillissementen_Jaar1'] = (
        construction_2008['MS_CNT_FIRST_REGISTRATIONS'] - 
        construction_2008['MS_CNT_SURV_YEAR_1']
    )
    
    # Group by region and worker class
    result = construction_2008.groupby(['Gewest', 'Werknemersklasse'])['Faillissementen_Jaar1'].sum().reset_index()
    result.columns = ['Gewest', 'Bedrijfsomvang', 'Aantal_Faillissementen_Jaar1']
    
    # Pivot for better readability
    pivot = result.pivot(index='Gewest', columns='Bedrijfsomvang', values='Aantal_Faillissementen_Jaar1')
    pivot = pivot.fillna(0).astype(int)
    pivot = pivot.reset_index()
    
    # Reorder columns in logical order
    column_order = ['Gewest', '0-4 werknemers', '5-9 werknemers', '10-49 werknemers', '50+ werknemers']
    available_cols = [col for col in column_order if col in pivot.columns]
    if available_cols:
        pivot = pivot[available_cols]
    
    pivot.to_csv('data/processed/faillissementen_per_omvang_2024.csv', index=False)
    print(f"   Opgeslagen: faillissementen_per_omvang_2024.csv (2008 data)")
    print(f"   Rijen: {len(pivot)}")
    
    return pivot

def generate_operational_years_analysis(df):
    """Analyseer faillissementen per werkingsjaar (2008 cohort)"""
    print("\n3. Analyseren correlatie met werkingsjaren (2008 cohort)...")
    
    # Filter construction sector for 2008
    construction = df[
        (df['CD_NACE_LVL1'] == 'F') &
        (df['CD_YEAR'] == 2008)
    ].copy()
    
    # Map regions
    construction['Gewest'] = construction['CD_RGN_REFNIS'].apply(map_region_code)
    construction = construction[construction['Gewest'].notna()]
    
    # Calculate failures at different stages per region
    results = []
    
    for gewest in ['Vlaanderen', 'Wallonië', 'Brussel']:
        year_data = construction[construction['Gewest'] == gewest]
        
        starters = year_data['MS_CNT_FIRST_REGISTRATIONS'].sum()
        
        # Failures in year 1 (start - year 1)
        fail_year_1 = (year_data['MS_CNT_FIRST_REGISTRATIONS'] - year_data['MS_CNT_SURV_YEAR_1']).sum()
        
        # Failures in year 2 (year 1 - year 2)
        fail_year_2 = (year_data['MS_CNT_SURV_YEAR_1'] - year_data['MS_CNT_SURV_YEAR_2']).sum()
        
        # Failures in year 3
        fail_year_3 = (year_data['MS_CNT_SURV_YEAR_2'] - year_data['MS_CNT_SURV_YEAR_3']).sum()
        
        # Failures in year 4
        fail_year_4 = (year_data['MS_CNT_SURV_YEAR_3'] - year_data['MS_CNT_SURV_YEAR_4']).sum()
        
        # Failures in year 5
        fail_year_5 = (year_data['MS_CNT_SURV_YEAR_4'] - year_data['MS_CNT_SURV_YEAR_5']).sum()
        
        # Calculate percentages
        results.append({
            'Gewest': gewest,
            'Aantal_Starters': int(starters),
            'Faillissementen_Jaar_1': int(fail_year_1),
            'Percentage_Jaar_1': round(fail_year_1/starters*100, 1) if starters > 0 else 0,
            'Faillissementen_Jaar_2': int(fail_year_2),
            'Percentage_Jaar_2': round(fail_year_2/starters*100, 1) if starters > 0 else 0,
            'Faillissementen_Jaar_3': int(fail_year_3),
            'Percentage_Jaar_3': round(fail_year_3/starters*100, 1) if starters > 0 else 0,
            'Faillissementen_Jaar_4': int(fail_year_4),
            'Percentage_Jaar_4': round(fail_year_4/starters*100, 1) if starters > 0 else 0,
            'Faillissementen_Jaar_5': int(fail_year_5),
            'Percentage_Jaar_5': round(fail_year_5/starters*100, 1) if starters > 0 else 0
        })
    
    result_df = pd.DataFrame(results)
    result_df.to_csv('data/processed/faillissementen_per_werkingsjaar.csv', index=False)
    print(f"   Opgeslagen: faillissementen_per_werkingsjaar.csv")
    print(f"   Rijen: {len(result_df)}")
    
    return result_df

def generate_starting_companies(df):
    """Genereer aantal startende ondernemingen per gewest (2008 data)"""
    print("\n4. Berekenen startende ondernemingen per gewest...")
    print("   OPMERKING: Alleen 2008 data beschikbaar in survival dataset")
    
    # Filter construction sector for 2008
    construction = df[
        (df['CD_NACE_LVL1'] == 'F') &
        (df['CD_YEAR'] == 2008)
    ].copy()
    
    # Map regions
    construction['Gewest'] = construction['CD_RGN_REFNIS'].apply(map_region_code)
    construction = construction[construction['Gewest'].notna()]
    
    # Group by region
    result = construction.groupby('Gewest')['MS_CNT_FIRST_REGISTRATIONS'].sum().reset_index()
    result.columns = ['Gewest', 'Aantal_Starters_2008']
    
    result.to_csv('data/processed/startende_ondernemingen_per_gewest.csv', index=False)
    print(f"   Opgeslagen: startende_ondernemingen_per_gewest.csv (2008 data)")
    print(f"   Rijen: {len(result)}")
    
    return result

def generate_economic_cycle_analysis():
    """Genereer economische cyclus analyse van bestaande data"""
    print("\n5. Genereren economische cyclus analyse (2005-2024)...")
    
    # Load existing bankruptcies data
    with open('data/processed/bankruptcies_yearly.json', 'r') as f:
        yearly_data = json.load(f)
    
    results = []
    for year_data in yearly_data:
        if year_data['year'] >= 2005:
            year = year_data['year']
            bankruptcies = year_data['bankruptcies']
            
            results.append({
                'Jaar': year,
                'Vlaanderen_Bouw': bankruptcies['vlaams_bouw'],
                'Wallonië_Bouw': bankruptcies['waals_bouw'],
                'Brussel_Bouw': bankruptcies['brussels_bouw'],
                'Totaal_Bouw': (bankruptcies['vlaams_bouw'] + 
                               bankruptcies['waals_bouw'] + 
                               bankruptcies['brussels_bouw']),
                'Vlaanderen_Totaal': (bankruptcies['vlaams_bouw'] + 
                                     bankruptcies['vlaams_niet_bouw']),
                'Wallonië_Totaal': (bankruptcies['waals_bouw'] + 
                                   bankruptcies['waals_niet_bouw']),
                'Brussel_Totaal': (bankruptcies['brussels_bouw'] + 
                                  bankruptcies['brussels_niet_bouw'])
            })
    
    result_df = pd.DataFrame(results)
    result_df.to_csv('data/processed/economische_cyclus_analyse.csv', index=False)
    print(f"   Opgeslagen: economische_cyclus_analyse.csv")
    print(f"   Rijen: {len(result_df)}")
    
    return result_df

def main():
    """Hoofdfunctie"""
    print("="*60)
    print("ANALYSE FAILLISSEMENTEN BOUWSECTOR")
    print("="*60)
    
    # Load data
    df = load_survival_data()
    print(f"Data geladen: {len(df)} rijen (2008 cohort)")
    print("OPMERKING: Survival data bevat alleen 2008 cohort")
    print("Voor 2019-2024 cijfers wordt bankruptcies_yearly.json gebruikt")
    
    # Generate all analyses
    regional = generate_regional_breakdown()
    size_2024 = generate_company_size_2024(df)
    operational = generate_operational_years_analysis(df)
    starters = generate_starting_companies(df)
    economic = generate_economic_cycle_analysis()
    
    print("\n" + "="*60)
    print("ANALYSE COMPLEET")
    print("="*60)
    print("\nGegenereerde bestanden:")
    print("  1. faillissementen_per_gewest_2019_2024.csv - Faillissementen 2019-2024")
    print("  2. faillissementen_per_omvang_2024.csv - Per bedrijfsgrootte (2008 data)")
    print("  3. faillissementen_per_werkingsjaar.csv - Correlatie met werkingsjaren")
    print("  4. startende_ondernemingen_per_gewest.csv - Starters per gewest (2008)")
    print("  5. economische_cyclus_analyse.csv - Tijd reeks 2005-2024")
    print("\nAlle bestanden zijn opgeslagen in: data/processed/")
    print("="*60)

if __name__ == '__main__':
    main()

