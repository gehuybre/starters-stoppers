#!/usr/bin/env python3
"""
Download and process Statbel data for dashboard
Downloads TF_BANKRUPTCIES and TF_VAT_SURVIVALS from Statbel and processes them
"""

import os
import sys
import zipfile
import urllib.request
import ssl
import shutil
from pathlib import Path
from datetime import datetime

# URLs for Statbel data
# BANKRUPTCIES_URL is generated dynamically in main() to handle year updates
VAT_SURVIVALS_URL = "https://statbel.fgov.be/sites/default/files/files/opendata/TF_VAT_SURVIVAL/TF_VAT_SURVIVALS.zip"

# Directories
SCRIPT_DIR = Path(__file__).parent
DASHBOARD_DIR = SCRIPT_DIR.parent
DATA_DIR = DASHBOARD_DIR / "data"
PROCESSED_DIR = DATA_DIR / "data-grafieken"

def download_and_extract(url, filename, target_dir):
    """Download a zip file and extract it"""
    print(f"Downloading {filename}...")
    
    zip_path = target_dir / filename
    
    # Create SSL context that doesn't verify certificates
    # (Statbel certificates can be problematic)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Download file
    try:
        with urllib.request.urlopen(url, context=ssl_context) as response:
            with open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"✓ Downloaded {filename}")
    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")
        return False
    
    # Extract zip
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"✓ Extracted {filename}")
        
        # Remove zip file
        zip_path.unlink()
        
        return True
    except Exception as e:
        print(f"✗ Error extracting {filename}: {e}")
        return False

def run_processing_scripts():
    """Run the existing processing scripts"""
    print("\nProcessing data...")
    
    # Change to script directory so relative paths work
    os.chdir(SCRIPT_DIR)
    
    scripts = [
        "extract_chart_data_per_province.py",
    ]
    
    for script in scripts:
        script_path = SCRIPT_DIR / script
        if script_path.exists():
            print(f"\nRunning {script}...")
            result = os.system(f"python3 {script_path}")
            if result == 0:
                print(f"✓ {script} completed successfully")
            else:
                print(f"✗ {script} failed with exit code {result}")
                return False
        else:
            print(f"✗ Script not found: {script}")
            return False
    
    return True

def verify_data():
    """Verify that processed data exists"""
    print("\nVerifying processed data...")
    
    if not PROCESSED_DIR.exists():
        print(f"✗ Processed data directory not found: {PROCESSED_DIR}")
        return False
    
    # Check for province folders
    expected_provinces = ['Antwerpen', 'Vlaams-Brabant', 'West-Vlaanderen', 
                         'Oost-Vlaanderen', 'Limburg', 'Waals-Brabant',
                         'Henegouwen', 'Luik', 'Luxemburg', 'Namen', 'Brussels']
    
    found_provinces = [d.name for d in PROCESSED_DIR.iterdir() if d.is_dir()]
    
    if len(found_provinces) == 0:
        print(f"✗ No province data found in {PROCESSED_DIR}")
        return False
    
    print(f"✓ Found data for {len(found_provinces)} provinces/regions")
    for prov in found_provinces:
        csv_count = len(list((PROCESSED_DIR / prov).glob("*.csv")))
        print(f"  - {prov}: {csv_count} CSV files")
    
    return True

def main():
    """Main execution"""
    print("=" * 60)
    print("Statbel Data Update Script")
    print("=" * 60)
    
    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Download bankruptcies data
    print("\n[1/4] Downloading bankruptcies data...")
    
    current_year = datetime.now().year
    download_success = False
    
    # Try current year first, then previous year (in case new year file isn't created yet)
    years_to_try = [current_year, current_year - 1]
    
    for year in years_to_try:
        url = f"https://statbel.fgov.be/sites/default/files/files/opendata/BRI_Nace/TF_BANKRUPTCIES%28{year}%29.zip"
        print(f"Attempting to download data for year {year}...")
        if download_and_extract(url, "TF_BANKRUPTCIES.zip", DATA_DIR):
            download_success = True
            break
    
    if not download_success:
        print("\n✗ Failed to download bankruptcies data")
        sys.exit(1)
    
    # Step 2: Download VAT survivals data
    print("\n[2/4] Downloading VAT survivals data...")
    if not download_and_extract(VAT_SURVIVALS_URL, "TF_VAT_SURVIVALS.zip", DATA_DIR):
        print("\n✗ Failed to download VAT survivals data")
        sys.exit(1)
    
    # Step 3: Process data with existing scripts
    print("\n[3/4] Processing data...")
    if not run_processing_scripts():
        print("\n✗ Data processing failed")
        sys.exit(1)
    
    # Step 4: Verify data
    print("\n[4/4] Verifying processed data...")
    if not verify_data():
        print("\n✗ Data verification failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Data update completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
