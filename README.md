# Starters, stoppers en overlevingskans voor bouwbedrijven per provincie

Een interactief dashboard voor het visualiseren van bouwsector data per provincie in België.

## Functionaliteiten

### Provincieselectie met Knoppen
- Klik op provincieknoppen om ze te selecteren/deselecteren
- Actieve knoppen worden groen gemarkeerd
- Snelknoppen voor hele regio's:
  - **Vlaanderen** - Selecteert alle 5 Vlaamse provincies
  - **Wallonië** - Selecteert alle 5 Waalse provincies
  - **Brussels** - Selecteert Brussels Hoofdstedelijk Gewest
  - **Alles** - Selecteert alle provincies en gewesten
  - **Niets** - Deselecteert alles

### Navigatie
- Klikbare links in de header voor directe toegang tot elke sectie
- Smooth scrolling naar de gewenste grafiek
- 8 secties met data en visualisaties

### Inklapbare Tabellen
- Elke sectie heeft een "Toon/Verberg Tabel" knop
- Tabellen zijn standaard verborgen voor overzichtelijkheid
- Klik op de knop om de volledige data te bekijken

### 8 Grafieken en Tabellen

Het dashboard toont voor elke geselecteerde provincie:

1. **Overlevingskans na 1 jaar** *(Berekend uit TF_VAT_SURVIVALS)*
   - Lijndiagram met overlevingspercentages per jaar
   - Data tabel met alle cijfers
   - **Let op**: Meet alle stopzettingen, niet enkel faillissementen

2. **Overlevingskans na 3 jaar** *(Berekend uit TF_VAT_SURVIVALS)*
   - Lijndiagram (data tot 2021)
   - Data tabel met details
   - **Let op**: Meet alle stopzettingen, niet enkel faillissementen

3. **Nieuwe starters bouwsector**
   - Absolute aantallen per jaar
   - Vergelijking tussen provincies

4. **Faillissementen bouwsector** *(Juridische bankruptcies uit TF_BANKRUPTCIES)*
   - Jaarlijkse faillissementscijfers vanaf 2005
   - Trends per provincie
   - **Let op**: Dit zijn enkel formele faillissementen, niet alle stopzettingen

5. **12-maandelijkse trend faillissementen (index 2008 = 100)** *(Juridische bankruptcies)*
   - Geïndexeerde 12-maands rollende som
   - Bouwsector vs. Niet-bouwsector

6. **12-maandelijkse trend faillissementen (absolute cijfers)** *(Juridische bankruptcies)*
   - Absolute 12-maands rollende som
   - Alleen bouwsector

7. **Nieuwe starters (index 2008 = 100)**
   - Geïndexeerde startaantallen
   - Bouwsector vs. Niet-bouwsector

8. **Jaarlijkse cijfers bouwsector (sinds 2016)** *(Gecombineerde data)*
   - Staafdiagram met meerdere metrics
   - Overzicht alle belangrijke cijfers
   - Combineert overlevingskansen (stopzettingen) met juridische faillissementen

## Gebruik

### Stap-voor-stap
1. Start een lokale webserver (zie hieronder)
2. Open het dashboard in je browser
3. Klik op provincieknoppen of gebruik snelknoppen voor regio's
4. Scroll door de grafieken of gebruik de navigatie in de header
5. Klik op "Toon/Verberg Tabel" om detaildata te bekijken

### Lokaal openen
1. **Belangrijk**: Gebruik een lokale webserver vanwege CORS-beperkingen bij het laden van CSV-bestanden

### Met Python lokale server:
```bash
# In de dashboard-provincies folder
python3 -m http.server 8000

# Open in browser:
# http://localhost:8000
```

### Met Node.js:
```bash
npm install -g http-server
http-server -p 8000
```

## Structuur

```
dashboard-provincies/
├── index.html                      # Hoofd HTML bestand
├── css/
│   ├── layout-template.css        # Basis layout (van Embuild template)
│   ├── longread.css               # Longread styles
│   ├── longread-custom.css        # Custom longread
│   └── dashboard.css              # Dashboard-specifieke styles
├── js/
│   ├── dashboard-main.js          # Hoofdcoördinator
│   ├── dashboard-data-loader.js   # CSV data loader
│   └── dashboard-charts.js        # Chart.js visualisaties
└── assets/
    └── logo.png                   # Logo afbeelding
```

## Data Locatie

Het dashboard laadt CSV-bestanden van:
```
../data/data-grafieken/{provincie}/{csv-bestand}
```

Bijvoorbeeld:
- `../data/data-grafieken/Antwerpen/Nieuwe starters bouwsector.csv`
- `../data/data-grafieken/Limburg/Faillissementen bouwsector.csv`

## Technologieën

- **HTML5** - Structuur
- **CSS3** - Styling met CSS variables
- **JavaScript (ES6+)** - Logica en interactiviteit
- **Chart.js v4** - Grafiekbibliotheek
- **CSV parsing** - Client-side data verwerking

## Kleurenschema per Provincie

| Provincie | Kleur |
|-----------|-------|
| Antwerpen | #e74c3c (rood) |
| Vlaams-Brabant | #3498db (blauw) |
| West-Vlaanderen | #2ecc71 (groen) |
| Oost-Vlaanderen | #f39c12 (oranje) |
| Limburg | #9b59b6 (paars) |
| Waals-Brabant | #1abc9c (turquoise) |
| Henegouwen | #e67e22 (donker oranje) |
| Luik | #34495e (donkergrijs) |
| Luxemburg | #16a085 (teal) |
| Namen | #d35400 (donker oranje-rood) |
| Brussels | #c0392b (bordeaux) |

## Browser Compatibiliteit

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Features

- ✅ **Klikbare provincieknoppen** - Geen dropdown, maar echte selecteerbare knoppen
- ✅ **Navigatie in header** - Directe links naar elke sectie
- ✅ **Inklapbare tabellen** - Verberg/toon detaildata per sectie
- ✅ **Regio-snelknoppen** - Vlaanderen, Wallonië, Brussels op gelijk niveau
- ✅ **Responsive design** - Werkt op desktop, tablet en mobiel
- ✅ **Real-time grafiek updates** - Grafieken passen zich direct aan
- ✅ **Kleurgecodeerde provincies** - Elke provincie heeft unieke kleur
- ✅ **Smooth scrolling** - Vloeiende navigatie tussen secties
- ✅ **Automatische data parsing** - CSV's worden automatisch ingeladen
- ✅ **Error handling** - Robuuste foutafhandeling

## Troubleshooting

### CSV's laden niet
- Zorg dat je een lokale webserver gebruikt (niet `file://`)
- Controleer of de data-grafieken folder correct is geplaatst (één niveau hoger)
- Check de browser console voor specifieke fouten

### Grafieken renderen niet
- Controleer of Chart.js correct is geladen
- Ververs de pagina
- Check de browser console

### Provincieknoppen werken niet
- Controleer of JavaScript correct is geladen
- Check de browser console voor fouten
- Ververs de pagina en probeer opnieuw

---

*Dashboard gemaakt op: 8 december 2024*
