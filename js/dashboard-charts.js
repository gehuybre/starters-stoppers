// Dashboard Charts Manager - Creates and updates all charts

class ChartsManager {
    constructor(dataLoader) {
        this.dataLoader = dataLoader;
        this.charts = {};
    }

    createAllCharts(data, selectedProvinces) {
        this.destroyAllCharts();
        
        // Chart 1: Overlevingskans na 1 jaar
        this.createSurvival1YearChart(data, selectedProvinces);
        
        // Chart 2: Overlevingskans na 3 jaar
        this.createSurvival3YearChart(data, selectedProvinces);
        
        // Chart 3: Nieuwe starters bouwsector
        this.createStartersChart(data, selectedProvinces);
        
        // Chart 4: Faillissementen bouwsector
        this.createBankruptciesChart(data, selectedProvinces);
        
        // Chart 5: 12-maandelijkse trend (index)
        this.createTrendIndexChart(data, selectedProvinces);
        
        // Chart 6: 12-maandelijkse trend (absolute)
        this.createTrendAbsoluteChart(data, selectedProvinces);
        
        // Chart 7: Nieuwe starters (index)
        this.createStartersIndexChart(data, selectedProvinces);
        
        // Chart 8: Jaarlijkse cijfers (summary)
        this.createYearlySummaryChart(data, selectedProvinces);
    }

    createSurvival1YearChart(data, selectedProvinces) {
        const csvKey = 'Overlevingskans na 1 jaar.csv';
        console.log('Creating survival 1 year chart, data:', data[csvKey], 'provinces:', selectedProvinces);
        const chartData = this.prepareLineChartData(data[csvKey], selectedProvinces, 'Jaar', 'Bouwsector (%)');
        
        const ctx = document.getElementById('survival-1year-chart');
        if (!ctx) {
            console.error('Canvas element survival-1year-chart not found');
            return;
        }
        this.charts['survival-1year'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('Overlevingskans na 1 jaar (%)', 'Jaar', 'Percentage (%)')
        });
    }

    createSurvival3YearChart(data, selectedProvinces) {
        const csvKey = 'Overlevingskans na 3 jaar.csv';
        console.log('Creating survival 3 year chart, data:', data[csvKey], 'provinces:', selectedProvinces);
        const chartData = this.prepareLineChartData(data[csvKey], selectedProvinces, 'Jaar', 'Bouwsector (%)');
        
        const ctx = document.getElementById('survival-3year-chart');
        if (!ctx) {
            console.error('Canvas element survival-3year-chart not found');
            return;
        }
        this.charts['survival-3year'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('Overlevingskans na 3 jaar (%)', 'Jaar', 'Percentage (%)')
        });
    }

    createStartersChart(data, selectedProvinces) {
        const csvKey = 'Nieuwe starters bouwsector.csv';
        console.log('Creating starters chart, data:', data[csvKey], 'provinces:', selectedProvinces);
        const chartData = this.prepareLineChartData(data[csvKey], selectedProvinces, 'Jaar', 'Aantal nieuwe starters');
        
        const ctx = document.getElementById('starters-chart');
        if (!ctx) {
            console.error('Canvas element starters-chart not found');
            return;
        }
        this.charts['starters'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('Nieuwe starters bouwsector', 'Jaar', 'Aantal')
        });
    }

    createBankruptciesChart(data, selectedProvinces) {
        const csvKey = 'Faillissementen bouwsector.csv';
        console.log('Creating bankruptcies chart, data:', data[csvKey], 'provinces:', selectedProvinces);
        const chartData = this.prepareLineChartData(data[csvKey], selectedProvinces, 'Jaar', 'Aantal faillissementen');
        
        const ctx = document.getElementById('bankruptcies-chart');
        if (!ctx) {
            console.error('Canvas element bankruptcies-chart not found');
            return;
        }
        this.charts['bankruptcies'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('Faillissementen bouwsector', 'Jaar', 'Aantal')
        });
    }

    createTrendIndexChart(data, selectedProvinces) {
        const csvKey = '12-maandelijkse trend faillissementen (index 2008 = 100).csv';
        console.log('Creating trend index chart, data:', data[csvKey], 'provinces:', selectedProvinces);
        const chartData = this.prepareMultiLineChartData(
            data[csvKey], 
            selectedProvinces, 
            'Jaar-Maand', 
            ['Bouwsector (index)', 'Niet-bouwsector (index)']
        );
        
        const ctx = document.getElementById('trend-index-chart');
        if (!ctx) {
            console.error('Canvas element trend-index-chart not found');
            return;
        }
        this.charts['trend-index'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('12-maandelijkse trend (index 2008 = 100)', 'Jaar-Maand', 'Index', true)
        });
    }

    createTrendAbsoluteChart(data, selectedProvinces) {
        const csvKey = '12-maandelijkse trend faillissementen bouwsector (absolute cijfers).csv';
        console.log('Creating trend absolute chart, data:', data[csvKey], 'provinces:', selectedProvinces);
        const chartData = this.prepareLineChartData(
            data[csvKey], 
            selectedProvinces, 
            'Jaar-Maand', 
            'Aantal faillissementen (12-maands som)'
        );
        
        const ctx = document.getElementById('trend-absolute-chart');
        this.charts['trend-absolute'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('12-maandelijkse trend (absolute)', 'Jaar-Maand', 'Aantal', true)
        });
    }

    createStartersIndexChart(data, selectedProvinces) {
        const csvKey = 'Nieuwe starters (index 2008 = 100).csv';
        const chartData = this.prepareMultiLineChartData(
            data[csvKey], 
            selectedProvinces, 
            'Jaar', 
            ['Bouwsector (index)', 'Niet-bouwsector (index)']
        );
        
        const ctx = document.getElementById('starters-index-chart');
        this.charts['starters-index'] = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: this.getLineChartOptions('Nieuwe starters (index 2008 = 100)', 'Jaar', 'Index')
        });
    }

    createYearlySummaryChart(data, selectedProvinces) {
        const csvKey = 'Jaarlijkse cijfers bouwsector (sinds 2016).csv';
        
        // For this chart, we'll show multiple metrics as grouped bars
        const chartData = this.prepareGroupedBarChartData(
            data[csvKey],
            selectedProvinces,
            'Jaar',
            ['Nieuwe starters', 'Jaarlijkse faillissementen']
        );
        
        const ctx = document.getElementById('yearly-summary-chart');
        this.charts['yearly-summary'] = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: this.getBarChartOptions('Jaarlijkse cijfers bouwsector (sinds 2016)', 'Jaar', 'Aantal')
        });
    }

    prepareLineChartData(csvData, selectedProvinces, xKey, yKey) {
        const datasets = [];
        
        for (const province of selectedProvinces) {
            if (!csvData || !csvData[province]) continue;
            
            const provinceData = csvData[province];
            const sortedData = provinceData.sort((a, b) => {
                const aVal = a[xKey];
                const bVal = b[xKey];
                return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
            });
            
            datasets.push({
                label: province,
                data: sortedData.map(row => ({
                    x: row[xKey],
                    y: parseFloat(row[yKey]) || 0
                })),
                borderColor: this.dataLoader.getProvinceColor(province),
                backgroundColor: this.dataLoader.getProvinceColor(province) + '20',
                borderWidth: 2,
                tension: 0.1,
                pointRadius: 3,
                pointHoverRadius: 5
            });
        }
        
        return { datasets };
    }

    prepareMultiLineChartData(csvData, selectedProvinces, xKey, yKeys) {
        const datasets = [];
        
        for (const province of selectedProvinces) {
            if (!csvData || !csvData[province]) continue;
            
            const provinceData = csvData[province];
            const sortedData = provinceData.sort((a, b) => {
                const aVal = a[xKey];
                const bVal = b[xKey];
                return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
            });
            
            const baseColor = this.dataLoader.getProvinceColor(province);
            
            yKeys.forEach((yKey, index) => {
                const isDashed = index > 0;
                datasets.push({
                    label: `${province} - ${yKey}`,
                    data: sortedData.map(row => ({
                        x: row[xKey],
                        y: parseFloat(row[yKey]) || 0
                    })),
                    borderColor: baseColor,
                    backgroundColor: baseColor + '20',
                    borderWidth: 2,
                    borderDash: isDashed ? [5, 5] : [],
                    tension: 0.1,
                    pointRadius: 2,
                    pointHoverRadius: 4
                });
            });
        }
        
        return { datasets };
    }

    prepareGroupedBarChartData(csvData, selectedProvinces, xKey, yKeys) {
        const datasets = [];
        
        // Get all unique x values across all provinces
        const allXValues = new Set();
        for (const province of selectedProvinces) {
            if (!csvData || !csvData[province]) continue;
            csvData[province].forEach(row => allXValues.add(row[xKey]));
        }
        const sortedXValues = Array.from(allXValues).sort();
        
        // Create a dataset for each metric
        yKeys.forEach(yKey => {
            for (const province of selectedProvinces) {
                if (!csvData || !csvData[province]) continue;
                
                const provinceData = csvData[province];
                const dataMap = new Map(provinceData.map(row => [row[xKey], row[yKey]]));
                
                datasets.push({
                    label: `${province} - ${yKey}`,
                    data: sortedXValues.map(x => parseFloat(dataMap.get(x)) || 0),
                    backgroundColor: this.dataLoader.getProvinceColor(province) + '80',
                    borderColor: this.dataLoader.getProvinceColor(province),
                    borderWidth: 1
                });
            }
        });
        
        return {
            labels: sortedXValues,
            datasets
        };
    }

    getLineChartOptions(title, xLabel, yLabel, skipXLabels = false) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    type: 'category',
                    title: {
                        display: true,
                        text: xLabel
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        autoSkip: skipXLabels,
                        maxTicksLimit: skipXLabels ? 20 : undefined
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: yLabel
                    },
                    beginAtZero: false,
                    grace: '10%'
                }
            }
        };
    }

    getBarChartOptions(title, xLabel, yLabel) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: xLabel
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: yLabel
                    },
                    beginAtZero: false,
                    grace: '10%'
                }
            }
        };
    }

    destroyAllCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {};
    }
}

// Export for use in other scripts
window.ChartsManager = ChartsManager;
