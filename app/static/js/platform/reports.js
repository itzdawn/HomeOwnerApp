/**
 * Reports Management for Platform Administrators
 * Handles service usage reports generation and export
 */

$(document).ready(function() {
    let datePicker;
    let reportChart;
    
    // Initialize date picker based on report type
    function initializeDatePicker(type) {
        if (datePicker) {
            datePicker.destroy(); // Destroy previous instance
        }
        
        const options = {
            altInput: true,
            altFormat: "F j, Y",
            dateFormat: "Y-m-d",
        };
        
        if (type === 'daily') {
            options.mode = 'single';
            options.defaultDate = 'today';
            options.maxDate = 'today';
        } else if (type === 'weekly') {
            options.mode = 'single';
            options.defaultDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000); // One week ago
            options.maxDate = 'today';
        } else if (type === 'monthly') {
            options.mode = 'single';
            options.defaultDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000); // One month ago
            options.maxDate = 'today';
        }
        
        datePicker = flatpickr("#reportDate", options);
    }
    
    // Function to generate a report
    function generateReport() {
        const reportType = $('#reportType').val();
        const dateValue = $('#reportDate').val();
        const groupBy = $('#groupBy').val();
        
        // Validation
        if (!dateValue) {
            alert('Please select a date or date range');
            return;
        }
        
        // Show loading state
        $('#report-placeholder').html('<div class="text-center my-5"><div class="spinner-border text-primary" role="status"></div><div class="mt-2">Generating report...</div></div>');
        $('#report-placeholder').show();
        $('.chart-container, #report-table-container').addClass('d-none');
        
        // API call to get report data
        $.ajax({
            url: '/api/platform/reports',
            type: 'GET',
            data: {
                reportType: reportType,
                dateValue: dateValue,
                groupBy: groupBy
            },
            success: function(reportData) {
                // Hide placeholder and show report actions
                $('#report-placeholder').hide();
                $('.report-actions').show();
                
                // Update report title
                $('#report-title').text(reportData.title || 'Generated Report');
                
                // Generate chart
                generateChart(reportData);
                
                // Generate table
                generateTable(reportData);
            },
            error: function(error) {
                console.error('Error generating report:', error);
                $('#report-placeholder').html('<div class="text-center text-danger my-5"><i class="bi bi-exclamation-triangle fs-1"></i><div class="mt-2">Failed to generate report. Please try again.</div></div>');
            }
        });
    }
    
    // Function to generate chart
    function generateChart(reportData) {
        // Prepare data for Chart.js
        const labels = reportData.rows.map(row => row[0]); // First column is label
        const values = reportData.rows.map(row => row[reportData.headers.length - 1]); // Last column is value (assume it's total revenue)
        
        const chartData = {
            labels: labels,
            datasets: [{
                label: reportData.headers[reportData.headers.length - 1],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                data: values
            }]
        };
        
        // Determine chart type based on data
        const chartType = labels.length > 10 ? 'line' : 'bar';
        
        // Create/update chart
        $('.chart-container').removeClass('d-none');
        
        const ctx = document.getElementById('reportChart').getContext('2d');
        
        if (reportChart) {
            reportChart.destroy();
        }
        
        reportChart = new Chart(ctx, {
            type: chartType,
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Function to generate table
    function generateTable(reportData) {
        const $tableHead = $('#report-table thead');
        const $tableBody = $('#report-table tbody');
        const $tableFoot = $('#report-table tfoot');
        
        $tableHead.empty();
        $tableBody.empty();
        $tableFoot.empty();
        
        // Populate Headers
        let headerHtml = '<tr>';
        reportData.headers.forEach(header => {
            headerHtml += `<th>${header}</th>`;
        });
        headerHtml += '</tr>';
        $tableHead.append(headerHtml);
        
        // Populate Rows
        reportData.rows.forEach(row => {
            let rowHtml = '<tr>';
            row.forEach((cell, index) => {
                // Format price columns with $ for better readability
                if (index > 0 && reportData.headers[index].toLowerCase().includes('revenue')) {
                    rowHtml += `<td>$${parseFloat(cell).toFixed(2)}</td>`;
                } else {
                    rowHtml += `<td>${cell}</td>`;
                }
            });
            rowHtml += '</tr>';
            $tableBody.append(rowHtml);
        });
        
        // Populate Totals
        if (reportData.totals && reportData.totals.length > 0) {
            let footerHtml = '<tr>';
            reportData.totals.forEach((total, index) => {
                if (index === 0) {
                    footerHtml += `<th>${total}</th>`;
                } else if (reportData.headers[index].toLowerCase().includes('revenue')) {
                    footerHtml += `<th>$${parseFloat(total).toFixed(2)}</th>`;
                } else {
                    footerHtml += `<th>${total}</th>`;
                }
            });
            footerHtml += '</tr>';
            $tableFoot.append(footerHtml);
        }
        
        // Show table container
        $('#report-table-container').removeClass('d-none');
    }
    
    // Function to export table to CSV
    function exportTableToCSV(filename) {
        const rows = [];
        const $table = document.getElementById('report-table');
        
        // Get headers
        const headerRow = [];
        const headers = $table.querySelectorAll('thead th');
        headers.forEach(header => headerRow.push('"' + header.innerText.replace(/"/g, '""') + '"'));
        rows.push(headerRow.join(','));
        
        // Get data rows
        const dataRows = $table.querySelectorAll('tbody tr');
        dataRows.forEach(row => {
            const rowData = [];
            const cells = row.querySelectorAll('td');
            cells.forEach(cell => rowData.push('"' + cell.innerText.replace(/"/g, '""') + '"'));
            rows.push(rowData.join(','));
        });
        
        // Get footer
        const footerRows = $table.querySelectorAll('tfoot tr');
        footerRows.forEach(row => {
            const rowData = [];
            const cells = row.querySelectorAll('th');
            cells.forEach(cell => rowData.push('"' + cell.innerText.replace(/"/g, '""') + '"'));
            rows.push(rowData.join(','));
        });
        
        // Create CSV content
        const csvContent = rows.join('\n');
        
        // Create download link
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    
    // Event handler for report type change
    $('#reportType').on('change', function() {
        initializeDatePicker($(this).val());
    });
    
    // Event handler for generate report button
    $('#generateReportBtn').on('click', function() {
        generateReport(); // Use real API call
    });
    
    // Initialize with default date picker
    initializeDatePicker($('#reportType').val());
    
    // Inform parent window about loaded height for iframe resizing
    if (window.parent) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 