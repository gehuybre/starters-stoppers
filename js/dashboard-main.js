// Dashboard Main - Coordinates everything

class Dashboard {
    constructor() {
        this.dataLoader = new DataLoader();
        this.chartsManager = new ChartsManager(this.dataLoader);
        this.selectedProvinces = [];
        this.currentData = null;
        this.provinceButtons = null;
        this.useRegionAverages = false;
    }

    async init() {
        console.log('Initializing dashboard...');
        
        // Setup controls
        this.setupControls();
        
        // Setup table toggles
        this.setupTableToggles();
        
        // Load Vlaanderen data by default
        this.selectedProvinces = ['Vlaanderen'];
        this.useRegionAverages = true;
        await this.loadAndRender();
        
        console.log('Dashboard initialized successfully');
    }

    setupControls() {
        // Get all province buttons
        this.provinceButtons = document.querySelectorAll('.btn-province');
        
        // Add click handlers to province buttons
        this.provinceButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.toggleProvince(btn);
            });
        });

        // Add click handlers to region buttons
        document.querySelectorAll('.btn-region').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleRegionAction(action);
            });
        });
    }

    toggleProvince(button) {
        const province = button.dataset.province;
        button.classList.toggle('active');
        
        if (button.classList.contains('active')) {
            if (!this.selectedProvinces.includes(province)) {
                this.selectedProvinces.push(province);
            }
        } else {
            this.selectedProvinces = this.selectedProvinces.filter(p => p !== province);
        }
        
        this.loadAndRender();
    }

    handleRegionAction(action) {
        const regionButtons = document.querySelectorAll('.btn-region');
        
        switch(action) {
            case 'vlaanderen':
                this.toggleRegion('Vlaanderen', regionButtons, action);
                break;
            case 'wallonie':
                this.toggleRegion('Wallonië', regionButtons, action);
                break;
            case 'brussels':
                this.toggleRegion('Brussel', regionButtons, action);
                break;
            case 'all':
                // Deactivate all buttons first
                this.provinceButtons.forEach(btn => btn.classList.remove('active'));
                regionButtons.forEach(btn => btn.classList.remove('active'));
                this.selectedProvinces = ['Vlaanderen', 'Wallonië', 'Brussel'];
                this.useRegionAverages = true;
                regionButtons.forEach(btn => {
                    if (['vlaanderen', 'wallonie', 'brussels'].includes(btn.dataset.action)) {
                        btn.classList.add('active');
                    }
                });
                break;
            case 'none':
                this.provinceButtons.forEach(btn => btn.classList.remove('active'));
                regionButtons.forEach(btn => btn.classList.remove('active'));
                this.selectedProvinces = [];
                this.useRegionAverages = false;
                break;
        }
        
        this.loadAndRender();
    }

    toggleRegion(regionName, regionButtons, action) {
        const button = Array.from(regionButtons).find(btn => btn.dataset.action === action);
        
        if (this.selectedProvinces.includes(regionName)) {
            // Remove region
            this.selectedProvinces = this.selectedProvinces.filter(p => p !== regionName);
            if (button) button.classList.remove('active');
            // If no regions left, disable region averages
            if (!this.selectedProvinces.some(p => ['Vlaanderen', 'Wallonië', 'Brussel'].includes(p))) {
                this.useRegionAverages = false;
            }
        } else {
            // Add region
            this.selectedProvinces.push(regionName);
            this.useRegionAverages = true;
            if (button) button.classList.add('active');
        }
    }

    activateButtons(provinces) {
        this.provinceButtons.forEach(btn => {
            if (provinces.includes(btn.dataset.province)) {
                btn.classList.add('active');
            }
        });
    }

    setupTableToggles() {
        document.querySelectorAll('.btn-toggle-table').forEach(btn => {
            btn.addEventListener('click', () => {
                const tableId = btn.dataset.table;
                const container = document.getElementById(tableId + '-container');
                if (container) {
                    container.classList.toggle('hidden');
                }
            });
        });
    }

    async loadAndRender() {
        if (this.selectedProvinces.length === 0) {
            this.clearAll();
            return;
        }

        try {
            // Show loading state
            this.showLoading();

            // Separate regions and provinces
            const regions = this.selectedProvinces.filter(p => ['Vlaanderen', 'Wallonië', 'Brussel'].includes(p));
            const provinces = this.selectedProvinces.filter(p => !['Vlaanderen', 'Wallonië', 'Brussel'].includes(p));
            
            // Load all data (both provincial and regional)
            await this.dataLoader.loadAllData([...new Set(provinces)], regions);

            // Build currentData - use loaded data directly
            this.currentData = {};
            this.dataLoader.csvFiles.forEach(csvFile => {
                this.currentData[csvFile] = {};
                
                // Add regional data (directly loaded)
                regions.forEach(region => {
                    if (this.dataLoader.data[csvFile] && this.dataLoader.data[csvFile][region]) {
                        this.currentData[csvFile][region] = this.dataLoader.data[csvFile][region];
                    }
                });
                
                // Add individual province data
                provinces.forEach(province => {
                    if (this.dataLoader.data[csvFile] && this.dataLoader.data[csvFile][province]) {
                        this.currentData[csvFile][province] = this.dataLoader.data[csvFile][province];
                    }
                });
            });

            // Render charts
            this.chartsManager.createAllCharts(this.currentData, this.selectedProvinces);

            // Render tables
            this.renderAllTables();

            // Hide loading state
            this.hideLoading();

        } catch (error) {
            console.error('Error loading and rendering:', error);
            alert('Er is een fout opgetreden bij het laden van de data. Zie console voor details.');
        }
    }

    renderAllTables() {
        this.renderTable('Overlevingskans na 1 jaar.csv', 'survival-1year-table', 
            ['Provincie', 'Jaar', 'Bouwsector (%)']);
        
        this.renderTable('Overlevingskans na 3 jaar.csv', 'survival-3year-table', 
            ['Provincie', 'Jaar', 'Bouwsector (%)']);
        
        this.renderTable('Nieuwe starters bouwsector.csv', 'starters-table', 
            ['Provincie', 'Jaar', 'Aantal nieuwe starters']);
        
        this.renderTable('Faillissementen bouwsector.csv', 'bankruptcies-table', 
            ['Provincie', 'Jaar', 'Aantal faillissementen']);
        
        this.renderTable('12-maandelijkse trend faillissementen (index 2008 = 100).csv', 'trend-index-table', 
            ['Provincie', 'Jaar-Maand', 'Bouwsector (index)', 'Niet-bouwsector (index)']);
        
        this.renderTable('12-maandelijkse trend faillissementen bouwsector (absolute cijfers).csv', 'trend-absolute-table', 
            ['Provincie', 'Jaar-Maand', 'Aantal faillissementen (12-maands som)']);
        
        this.renderTable('Nieuwe starters (index 2008 = 100).csv', 'starters-index-table', 
            ['Provincie', 'Jaar', 'Bouwsector (index)', 'Niet-bouwsector (index)']);
        
        this.renderTable('Jaarlijkse cijfers bouwsector (sinds 2016).csv', 'yearly-summary-table', 
            ['Provincie', 'Jaar', '1-jarige overlevingskans (%)', '3-jarige overlevingskans (%)', 
             'Nieuwe starters', 'Jaarlijkse faillissementen']);
    }

    renderTable(csvKey, tableId, columns) {
        const table = document.getElementById(tableId);
        if (!table) return;

        const tbody = table.querySelector('tbody');
        tbody.innerHTML = '';

        const csvData = this.currentData[csvKey];
        if (!csvData) return;

        // Collect all rows from all selected provinces
        const allRows = [];
        for (const province of this.selectedProvinces) {
            if (!csvData[province]) continue;
            
            csvData[province].forEach(row => {
                allRows.push({
                    provincie: province,
                    ...row
                });
            });
        }

        // Sort by first column (usually year or date)
        const firstDataColumn = columns[1]; // Skip "Provincie" column
        allRows.sort((a, b) => {
            const aVal = a[firstDataColumn];
            const bVal = b[firstDataColumn];
            if (aVal < bVal) return -1;
            if (aVal > bVal) return 1;
            return a.provincie.localeCompare(b.provincie);
        });

        // Render rows
        allRows.forEach(row => {
            const tr = document.createElement('tr');
            
            columns.forEach(col => {
                const td = document.createElement('td');
                if (col === 'Provincie') {
                    td.textContent = row.provincie;
                } else {
                    td.textContent = row[col] || '-';
                }
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
    }

    showLoading() {
        // Add a simple loading indicator
        document.body.style.cursor = 'wait';
    }

    hideLoading() {
        document.body.style.cursor = 'default';
    }

    clearAll() {
        // Clear all charts
        this.chartsManager.destroyAllCharts();

        // Clear all tables
        const tables = document.querySelectorAll('table tbody');
        tables.forEach(tbody => {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 20px; color: #999;">Selecteer provincies om data te tonen</td></tr>';
        });
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
    dashboard.init();
});
