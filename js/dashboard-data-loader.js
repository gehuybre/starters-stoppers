// Dashboard Data Loader - Loads all CSV files for selected provinces

class DataLoader {
    constructor() {
        this.provinces = [
            'Antwerpen', 'Vlaams-Brabant', 'West-Vlaanderen', 'Oost-Vlaanderen', 'Limburg',
            'Waals-Brabant', 'Henegouwen', 'Luik', 'Luxemburg', 'Namen', 'Brussels'
        ];
        
        this.csvFiles = [
            'Overlevingskans na 1 jaar.csv',
            'Overlevingskans na 3 jaar.csv',
            'Nieuwe starters bouwsector.csv',
            'Faillissementen bouwsector.csv',
            '12-maandelijkse trend faillissementen (index 2008 = 100).csv',
            '12-maandelijkse trend faillissementen bouwsector (absolute cijfers).csv',
            'Nieuwe starters (index 2008 = 100).csv',
            'Jaarlijkse cijfers bouwsector (sinds 2016).csv'
        ];
        
        // Map standard CSV names to regional CSV names for Vlaanderen
        this.regionalFileMap = {
            'Nieuwe starters bouwsector.csv': 'Nieuwe starters Vlaamse bouwsector.csv',
            'Faillissementen bouwsector.csv': 'Faillissementen Vlaamse bouwsector.csv',
            '12-maandelijkse trend faillissementen bouwsector (absolute cijfers).csv': '12-maandelijkse trend faillissementen Vlaamse bouwsector (absolute cijfers).csv',
            'Jaarlijkse cijfers bouwsector (sinds 2016).csv': 'Jaarlijkse cijfers Vlaanderen bouwsector (sinds 2016).csv'
        };
        
        // Files that use "Gewest" column and can be filtered
        this.gewestFiles = [
            'Overlevingskans na 1 jaar.csv',
            'Overlevingskans na 3 jaar.csv',
            'Nieuwe starters (index 2008 = 100).csv'
        ];
        
        // Map region names to "Gewest" column values
        this.gewestNameMap = {
            'Vlaanderen': 'Vlaams Gewest',
            'Wallonië': 'Waals Gewest',
            'Brussel': 'Brussels Gewest'
        };
        
        this.data = {};
    }

    async loadAllData(selectedProvinces, regions = []) {
        const promises = [];
        
        // Load provincial data
        for (const province of selectedProvinces) {
            for (const csvFile of this.csvFiles) {
                const path = `./data/data-grafieken/${province}/${csvFile}`;
                promises.push(this.loadCSV(path, province, csvFile));
            }
        }
        
        // Load regional data from root directory
        for (const region of regions) {
            for (const csvFile of this.csvFiles) {
                if (this.gewestFiles.includes(csvFile)) {
                    // Load from root file and filter by Gewest
                    const path = `./data/data-grafieken/${csvFile}`;
                    promises.push(this.loadGewestCSV(path, region, csvFile));
                } else if (csvFile === '12-maandelijkse trend faillissementen (index 2008 = 100).csv') {
                    // Special handling for multi-column regional file
                    const path = `./data/data-grafieken/${csvFile}`;
                    promises.push(this.loadTrendIndexCSV(path, region, csvFile));
                } else if (region === 'Vlaanderen' && this.regionalFileMap[csvFile]) {
                    // Use regional file name for Vlaanderen
                    const regionalFile = this.regionalFileMap[csvFile];
                    const path = `./data/data-grafieken/${regionalFile}`;
                    promises.push(this.loadRegionalCSV(path, 'Vlaanderen', csvFile));
                }
            }
        }
        
        await Promise.all(promises);
        return this.data;
    }

    async loadCSV(path, province, csvFile) {
        try {
            const response = await fetch(path);
            if (!response.ok) {
                console.error(`Failed to load ${path}: ${response.status}`);
                return;
            }
            
            const text = await response.text();
            const parsed = this.parseCSV(text);
            
            // Store data by CSV file name
            if (!this.data[csvFile]) {
                this.data[csvFile] = {};
            }
            this.data[csvFile][province] = parsed;
            
        } catch (error) {
            console.error(`Error loading ${path}:`, error);
        }
    }

    async loadRegionalCSV(path, region, csvFile) {
        try {
            const response = await fetch(path);
            if (!response.ok) {
                console.error(`Failed to load ${path}: ${response.status}`);
                return;
            }
            
            const text = await response.text();
            const parsed = this.parseCSV(text);
            
            // Add Provincie column to regional data
            const enrichedData = parsed.map(row => ({
                'Provincie': region,
                ...row
            }));
            
            // Store data by CSV file name
            if (!this.data[csvFile]) {
                this.data[csvFile] = {};
            }
            this.data[csvFile][region] = enrichedData;
            
        } catch (error) {
            console.error(`Error loading ${path}:`, error);
        }
    }

    async loadGewestCSV(path, region, csvFile) {
        try {
            const response = await fetch(path);
            if (!response.ok) {
                console.error(`Failed to load ${path}: ${response.status}`);
                return;
            }
            
            const text = await response.text();
            const parsed = this.parseCSV(text);
            
            // Filter by Gewest and rename column to Provincie
            const gewestName = this.gewestNameMap[region];
            const filteredData = parsed
                .filter(row => row['Gewest'] === gewestName)
                .map(row => {
                    const newRow = { 'Provincie': region };
                    Object.keys(row).forEach(key => {
                        if (key !== 'Gewest') {
                            newRow[key] = row[key];
                        }
                    });
                    return newRow;
                });
            
            // Store data by CSV file name
            if (!this.data[csvFile]) {
                this.data[csvFile] = {};
            }
            this.data[csvFile][region] = filteredData;
            
        } catch (error) {
            console.error(`Error loading ${path}:`, error);
        }
    }

    async loadTrendIndexCSV(path, region, csvFile) {
        try {
            const response = await fetch(path);
            if (!response.ok) {
                console.error(`Failed to load ${path}: ${response.status}`);
                return;
            }
            
            const text = await response.text();
            const parsed = this.parseCSV(text);
            
            // Extract columns for this region
            const gewestName = this.gewestNameMap[region];
            const bouwColumn = `${gewestName} - Bouwsector`;
            const nietBouwColumn = `${gewestName} - Niet-bouwsector`;
            
            const regionData = parsed.map(row => ({
                'Provincie': region,
                'Jaar-Maand': row['Jaar-Maand'],
                'Bouwsector (index)': row[bouwColumn] || '-',
                'Niet-bouwsector (index)': row[nietBouwColumn] || '-'
            }));
            
            // Store data by CSV file name
            if (!this.data[csvFile]) {
                this.data[csvFile] = {};
            }
            this.data[csvFile][region] = regionData;
            
        } catch (error) {
            console.error(`Error loading ${path}:`, error);
        }
    }

    parseCSV(text) {
        const lines = text.trim().split('\n');
        if (lines.length < 2) return [];
        
        const headers = lines[0].split(',').map(h => h.trim());
        const data = [];
        
        for (let i = 1; i < lines.length; i++) {
            const values = this.parseCSVLine(lines[i]);
            const row = {};
            
            headers.forEach((header, index) => {
                row[header] = values[index] || '';
            });
            
            data.push(row);
        }
        
        return data;
    }

    parseCSVLine(line) {
        const values = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                values.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        
        values.push(current.trim());
        return values;
    }

    getProvinceColor(province) {
        const colors = {
            'Antwerpen': '#e74c3c',
            'Vlaams-Brabant': '#3498db',
            'West-Vlaanderen': '#2ecc71',
            'Oost-Vlaanderen': '#f39c12',
            'Limburg': '#9b59b6',
            'Waals-Brabant': '#1abc9c',
            'Henegouwen': '#e67e22',
            'Luik': '#34495e',
            'Luxemburg': '#16a085',
            'Namen': '#d35400',
            'Brussels': '#c0392b',
            'Vlaanderen': '#FFD700',
            'Wallonië': '#8B0000',
            'Brussel': '#c0392b'
        };
        
        return colors[province] || '#95a5a6';
    }

    calculateRegionAverage(csvFile, region) {
        const regionProvinces = {
            'Vlaanderen': ['Antwerpen', 'Vlaams-Brabant', 'West-Vlaanderen', 'Oost-Vlaanderen', 'Limburg'],
            'Wallonië': ['Waals-Brabant', 'Henegouwen', 'Luik', 'Luxemburg', 'Namen'],
            'Brussel': ['Brussels']
        };

        const provinces = regionProvinces[region];
        if (!provinces || !this.data[csvFile]) return [];

        // Collect all data points grouped by year/date
        const groupedData = {};
        
        provinces.forEach(province => {
            const provinceData = this.data[csvFile][province];
            if (!provinceData) return;

            provinceData.forEach(row => {
                // Use second column as key (Jaar or Jaar-Maand), skip Provincie column
                const columns = Object.keys(row);
                const timeCol = columns[1]; // Should be 'Jaar' or 'Jaar-Maand'
                const key = row[timeCol];
                
                if (!groupedData[key]) {
                    groupedData[key] = { count: 0, sums: {}, firstCol: columns[0] };
                    // Initialize sums for all numeric columns (skip first two: Provincie and Jaar)
                    for (let i = 2; i < columns.length; i++) {
                        groupedData[key].sums[columns[i]] = 0;
                    }
                }

                // Sum all numeric values and count entries
                groupedData[key].count++;
                for (let i = 2; i < columns.length; i++) {
                    const col = columns[i];
                    const value = parseFloat(row[col]);
                    if (!isNaN(value) && row[col] !== '-') {
                        groupedData[key].sums[col] += value;
                    }
                }
            });
        });

        // Calculate averages
        const averagedData = [];
        
        // Get column names from first entry to maintain order
        const firstProvince = provinces.find(p => this.data[csvFile][p]);
        if (!firstProvince || !this.data[csvFile][firstProvince][0]) return [];
        
        const columns = Object.keys(this.data[csvFile][firstProvince][0]);
        const timeCol = columns[1]; // Jaar or Jaar-Maand
        
        Object.keys(groupedData).sort().forEach(key => {
            const group = groupedData[key];
            const row = {};
            
            // Build row in same order as provincial data: Provincie, Jaar/Jaar-Maand, then data columns
            row['Provincie'] = region;
            row[timeCol] = key;

            Object.keys(group.sums).forEach(col => {
                if (group.count > 0) {
                    row[col] = (group.sums[col] / group.count).toFixed(2);
                } else {
                    row[col] = '0';
                }
            });

            averagedData.push(row);
        });

        return averagedData;
    }
}

// Export for use in other scripts
window.DataLoader = DataLoader;
