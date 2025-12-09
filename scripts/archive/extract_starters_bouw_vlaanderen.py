import csv
from collections import defaultdict

# Lees het bestand en filter voor Vlaanderen (CD_RGN_REFNIS = 02000) en Bouwnijverheid (CD_NACE_LVL1 = F)
input_file = 'data/TF_VAT_SURVIVALS.txt'
output_file = 'data/processed/starters_vlaamse_bouwsector_per_jaar.csv'

# Dictionary om totalen per jaar op te slaan
starters_per_jaar = defaultdict(int)

with open(input_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig verwijdert BOM automatisch
    # Lees eerste lijn om header te krijgen
    header = f.readline().strip()
    field_names = [col.strip() for col in header.split('|')]
    
    reader = csv.DictReader(f, delimiter='|', fieldnames=field_names)
    
    for row in reader:
        # Strip whitespace from values
        row = {k: v.strip() if v else '' for k, v in row.items()}
        
        # Filter voor Vlaams Gewest (02000) en Bouwnijverheid (F)
        if row.get('CD_RGN_REFNIS') == '02000' and row.get('CD_NACE_LVL1') == 'F':
            jaar = row['CD_YEAR']
            # MS_CNT_FIRST_REGISTRATIONS = aantal eerste registraties (starters)
            starters = int(row['MS_CNT_FIRST_REGISTRATIONS'])
            starters_per_jaar[jaar] += starters

# Sorteer jaren en schrijf naar CSV
jaren_gesorteerd = sorted(starters_per_jaar.keys())

with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Jaar', 'Aantal starters'])
    
    for jaar in jaren_gesorteerd:
        writer.writerow([jaar, starters_per_jaar[jaar]])

print(f"CSV bestand aangemaakt: {output_file}")
print(f"\nOverzicht:")
for jaar in jaren_gesorteerd:
    print(f"{jaar}: {starters_per_jaar[jaar]} starters")
