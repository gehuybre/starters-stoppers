# CSV-bestanden per Provincie

## Overzicht

Dit project bevat nu CSV-bestanden met gedetailleerde cijfers **per provincie** in plaats van per gewest. De data is gegenereerd met het script `extract_chart_data_per_province.py`.

## Mappenstructuur

In de map `data/data-grafieken/` zijn nu submappen aangemaakt voor elke provincie:

### Vlaamse provincies:
- **Antwerpen**
- **Vlaams-Brabant**
- **West-Vlaanderen**
- **Oost-Vlaanderen**
- **Limburg**

### Waalse provincies:
- **Waals-Brabant**
- **Henegouwen**
- **Luik**
- **Luxemburg**
- **Namen**

### Brussels Hoofdstedelijk Gewest:
- **Brussels** (heeft geen provincies, maar wordt als aparte regio behandeld)

## CSV-bestanden per provincie

Elke provinciemap bevat de volgende 8 CSV-bestanden:

1. **Overlevingskans na 1 jaar.csv**
   - 1-jarige overlevingskans van nieuwe bedrijven in de bouwsector
   - Kolommen: `Provincie`, `Jaar`, `Bouwsector (%)`

2. **Overlevingskans na 3 jaar.csv**
   - 3-jarige overlevingskans (beschikbaar tot 2021)
   - Kolommen: `Provincie`, `Jaar`, `Bouwsector (%)`

3. **Nieuwe starters bouwsector.csv**
   - Aantal nieuwe startende bouwbedrijven per jaar
   - Kolommen: `Jaar`, `Aantal nieuwe starters`

4. **Faillissementen bouwsector.csv**
   - Jaarlijkse faillissementen in de bouwsector (vanaf 2005)
   - Kolommen: `Jaar`, `Aantal faillissementen`

5. **12-maandelijkse trend faillissementen (index 2008 = 100).csv**
   - Maandelijkse 12-maands rollende som, geïndexeerd op 2008
   - Kolommen: `Jaar-Maand`, `Bouwsector (index)`, `Niet-bouwsector (index)`

6. **12-maandelijkse trend faillissementen bouwsector (absolute cijfers).csv**
   - Maandelijkse 12-maands rollende som in absolute cijfers
   - Kolommen: `Jaar-Maand`, `Aantal faillissementen (12-maands som)`

7. **Nieuwe starters (index 2008 = 100).csv**
   - Aantal starters geïndexeerd op 2008
   - Kolommen: `Provincie`, `Jaar`, `Bouwsector (index)`, `Niet-bouwsector (index)`

8. **Jaarlijkse cijfers bouwsector (sinds 2016).csv**
   - Samenvatting van alle belangrijke cijfers vanaf 2016
   - Kolommen: `Jaar`, `1-jarige overlevingskans (%)`, `3-jarige overlevingskans (%)`, `Nieuwe starters`, `Jaarlijkse faillissementen`
   - **Let op**: "Jaarlijkse faillissementen" = juridische faillissementen uit TF_BANKRUPTCIES

## Databronnen

De data is afkomstig van twee bronnen:

### 1. Overlevingsdata (TF_VAT_SURVIVALS.txt)
- **TF_VAT_SURVIVALS.txt** - Statbel data over overlevingskansen en oprichtingen
- Meet **alle stopzettingen**: faillissementen, vrijwillige stopzettingen, fusies, liquidaties, etc.
- Gebruikt voor: overlevingskansen en aantal starters

### 2. Faillissementendata (TF_BANKRUPTCIES.txt)
- **TF_BANKRUPTCIES.txt** - Statbel data over **juridische faillissementen**
- Dit zijn enkel bedrijven die formeel failliet verklaard zijn door een rechtbank
- Dit is een **subset** van alle stopzettingen (veel bedrijven stoppen vrijwillig zonder faillissement)
- Gebruikt voor: alle grafieken met "faillissementen" in de naam

## Script gebruiken

Om de CSV-bestanden opnieuw te genereren:

```bash
python3 extract_chart_data_per_province.py
```

Het script:
1. Leest de brondata (TF_VAT_SURVIVALS.txt en TF_BANKRUPTCIES.txt)
2. Aggregeert de data per provincie
3. Maakt submappen aan voor elke provincie
4. Genereert alle 8 CSV-bestanden per provincie

## Verschil met originele bestanden

De originele CSV-bestanden in `data/data-grafieken/` (zonder submap) bevatten geaggregeerde cijfers **per gewest**:
- Vlaams Gewest
- Waals Gewest
- Brussels Gewest

De nieuwe CSV-bestanden in de submappen bevatten meer gedetailleerde cijfers **per provincie**, waardoor provinciale analyses mogelijk zijn.

## Gebruik

Deze provinciale data kan gebruikt worden voor:
- Provinciale vergelijkingen
- Regionale analyses binnen een gewest
- Gedetailleerde dashboards per provincie
- Identificatie van regionale trends en verschillen

---

*Gegenereerd op: 8 december 2024*
