# Dashboard Starters & Faillissementen Bouwsector

Interactief dashboard voor analyse van overlevingskansen, starters en faillissementen in de Belgische bouwsector per provincie.

## 📊 Features

- **Overlevingskansen**: 1-jarige en 3-jarige overlevingskansen per provincie
- **Starters**: Nieuwe starters in de bouwsector (absolute cijfers en index)
- **Faillissementen**: Juridische faillissementen en 12-maandelijkse trends
- **Jaarlijks Overzicht**: Geconsolideerde cijfers sinds 2016
- **Interactieve Filtering**: Selecteer provincies of hele regio's (Vlaanderen, Wallonië, Brussels)
- **Data Tabellen**: Toggle tussen visualisaties en ruwe data

## 🚀 Live Demo

Deze site is automatisch beschikbaar via GitHub Pages:
**[https://GEBRUIKER.github.io/REPO-NAAM/](https://GEBRUIKER.github.io/REPO-NAAM/)**

## 📁 Repository Structuur

```
.
├── index.html                 # Hoofdpagina
├── css/                       # Stylesheets
│   ├── layout-template.css
│   └── dashboard.css
├── js/                        # JavaScript modules
│   ├── dashboard-data-loader.js
│   ├── dashboard-charts.js
│   └── dashboard-main.js
├── assets/                    # Afbeeldingen en assets
│   └── logo.png
├── data/                      # CSV data files
│   └── data-grafieken/        # Alle datasets per provincie
└── .github/
    └── workflows/
        └── deploy.yml         # Automatische deployment

```

## 🔄 Automatische Deployment

Bij elke push naar de `main` branch:
1. GitHub Actions pakt automatisch de laatste versie
2. Publiceert naar GitHub Pages
3. Site is binnen 1-2 minuten live

### Workflow Details
- **Trigger**: Push naar `main` of handmatig via `workflow_dispatch`
- **Permissions**: Automatisch geconfigureerd voor Pages deployment
- **Geen build stap**: Pure HTML/CSS/JS, direct serveerbaar

## 📋 Data Bronnen

Alle data komt van **Statbel**:

### Overlevingskansen & Starters
📊 [Overleven van de btw-plichtige ondernemingen](https://statbel.fgov.be/nl/open-data/overleven-van-de-btw-plichtige-ondernemingen)
- Meet **alle stopzettingen**: faillissementen + vrijwillige stopzettingen + fusies
- 1-jarige en 3-jarige overlevingskansen
- Aantal nieuwe starters per jaar

### Faillissementen (Juridisch)
⚖️ [Maandevolutie van de faillissementen volgens NACE](https://statbel.fgov.be/nl/open-data/maandevolutie-van-de-faillissementen-volgens-nace)
- **Enkel formele faillissementen** door rechtbank
- Dit is een **subset** van alle stopzettingen
- Maandelijkse trends en jaarlijkse totalen

*Alle data verwerkt door Embuild Vlaanderen*

## 🛠️ Technische Details

### Dependencies
- **Chart.js v4.4.0**: Voor alle grafieken en visualisaties (via CDN)
- **Pure JavaScript**: Geen build process nodig
- **Responsive CSS**: Werkt op desktop en mobile

### Browser Support
- Moderne browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript features
- CSS Grid & Flexbox

## 📝 Data Updates

Om de data bij te werken:
1. Vervang CSV files in `data/data-grafieken/`
2. Commit en push naar `main`
3. GitHub Actions deployed automatisch

### Data Structuur
Elke provincie heeft eigen directory met CSV files:
```
data/data-grafieken/
├── Antwerpen/
├── Vlaams-Brabant/
├── West-Vlaanderen/
... (alle 11 provincies + Brussels)
└── [Vlaamse en regionale aggregaties]
```

## 🏗️ Lokaal Ontwikkelen

```bash
# Clone de repository
git clone https://github.com/GEBRUIKER/REPO-NAAM.git
cd REPO-NAAM

# Start een lokale webserver
python3 -m http.server 8000
# Of gebruik: npx serve

# Open in browser
open http://localhost:8000
```

## 🎨 Styling Aanpassen

- **Layout**: `css/layout-template.css` (header, navigation, grid)
- **Dashboard**: `css/dashboard.css` (charts, buttons, tables)
- **Kleuren**: Zie CSS custom properties in `:root`

## 📈 Chart Configuratie

Alle chart settings in `js/dashboard-charts.js`:
- Kleuren per provincie
- Responsive settings
- Tooltips en legends
- Animations

## 🔧 Onderhoud

### GitHub Pages Instellingen
1. Ga naar **Settings** > **Pages**
2. Source: **GitHub Actions**
3. Geen verdere configuratie nodig

### Deployment Status
Check deployment status onder **Actions** tab in de repository.

## 📄 Licentie

Data: © Statbel (Open Data)  
Verwerking: Embuild Vlaanderen  
Dashboard: [Voeg licentie toe]

## 🤝 Contact

Voor vragen over de data of het dashboard, contacteer [contactinfo].

---

**Automatisch gegenereerd dashboard** | Powered by GitHub Pages & Chart.js
