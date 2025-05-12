/**
 * Service History Management for Home Owners
 * Handles filtering, viewing and providing feedback for past services
 */

$(document).ready(function() {
    // Global variables
    let currentPage = 1;
    const itemsPerPage = 10;
    let currentServiceId = null;
    
    // Initialize flatpickr date range picker
    flatpickr("#dateRange", {
        mode: "range",
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "M j, Y",
        maxDate: "today"
    });
    
    function loadCategories() {
        $.ajax({
            url: '/api/cleaner/service-categories',
            type: 'GET',
            success: function(categories) {
                const categorySelect = $('#categorySelect');
                categorySelect.empty();
                categorySelect.append('<option value="">All Categories</option>');

                categories.forEach(category => {
                    categorySelect.append(`<option value="${category.id}">${category.name}</option>`);
                });
            },
            error: function(err) {
                console.error('Failed to load categories:', err);
            }
        });
    }
    // Function to load service history with pagination and filtering
    function loadServiceHistory(page = 1) {
        const keyword = $('#serviceName').val();
        const dateRange = $('#dateRange').val();
        const categoryId = $('#categorySelect').val();
        
        // Show loading indicator
        $('#historyTableBody').html('<tr><td colspan="6" class="text-center">Loading service history...</td></tr>');
        
        // API call to get service history
        $.ajax({
            url: '/api/homeowner/completed-services',
            type: 'GET',
            data: {
                service_name: keyword,
                start_date: dateRange ? dateRange.split(" to ")[0] : null,
                end_date: dateRange ? dateRange.split(" to ")[1] : null,
                categoryId: $('#categorySelect').val(), 
                page: page,
                items_per_page: itemsPerPage
            },
            success: function(response) {
                const services = response.services || [];
                const totalServices = response.total || 0;
                const totalPages = Math.ceil(totalServices / itemsPerPage);
                
                // Update total count
                $('#total-history').text(`Total of ${totalServices} service records found`);
                
                // Generate table rows
                if (services.length === 0) {
                    $('#historyTableBody').html('<tr><td colspan="6" class="text-center text-muted">No past service records found.</td></tr>');
                } else {
                    let tableHtml = '';
                    services.forEach(function(service) {
                        tableHtml += `
                        <tr>
                            <td>${service.name}</td>
                            <td>${service.category_name}</td>
                            <td>${service.cleaner_name}</td>
                            <td class="text-center">${service.service_date}</td>
                            <td class="text-center">$${service.price.toFixed(2)}</td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${service.CompletedServiceId}" data-bs-toggle="modal" data-bs-target="#viewHistoryModal">
                                        <i class="bi bi-eye"></i> View Details
                                    </button>
                                </div>
                            </td>
                        </tr>`;
                    });
                    $('#historyTableBody').html(tableHtml);
                }
                
                // Generate pagination
                generatePagination(page, totalPages);
                
                // Update current page
                currentPage = page;
            },
            error: function(error) {
                console.error('Error loading service history:', error);
                $('#historyTableBody').html('<tr><td colspan="6" class="text-center text-danger">Error loading service history. Please try again.</td></tr>');
            }
        });
    }
    
    // Function to generate pagination links
    function generatePagination(currentPage, totalPages) {
        const pagination = $('#pagination');
        pagination.empty();
        
        // Only show pagination if we have more than one page
        if (totalPages <= 1) return;
        
        // Previous button
        pagination.append(`
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>
            </li>
        `);
        
        // Page numbers
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, startPage + 4);
        
        for (let i = startPage; i <= endPage; i++) {
            pagination.append(`
                <li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `);
        }
        
        // Next button
        pagination.append(`
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>
            </li>
        `);
    }
    
    // Function to view service history details
    function viewServiceHistory(serviceId) {
        $.ajax({
            url: `/api/homeowner/service-history/${serviceId}`,
            type: 'GET',
            success: function(service) {
                // Store current service ID for feedback
                currentServiceId = serviceId;
                
                // Populate modal with service details
                $('#viewServiceName').text(service.name);
                $('#viewCategory').text(service.category_name);
                $('#viewDescription').text(service.description);
                $('#viewPrice').text(service.price.toFixed(2));
                $('#viewDateCompleted').text(service.service_date);
                $('#viewCleanerName').text(service.cleaner_name);
                
            },
            error: function(error) {
                console.error('Error loading service history details:', error);
                $('#viewHistoryModal').modal('hide');
                showToast('Failed to load service details. Please try again.', false);
            }
        });
    }
    
    // Function to show toast message
    function showToast(message, isSuccess) {
        const toastEl = document.getElementById('messageToast');
        const toastHeader = toastEl.querySelector('.toast-header');
        const icon = toastHeader.querySelector('i.bi');
        const toast = new bootstrap.Toast(toastEl);
        
        $('#toastMessage').text(message);
        
        if (isSuccess) {
            toastHeader.classList.remove('bg-danger');
            toastHeader.classList.add('bg-success');
            icon.className = 'bi bi-check-circle me-2';
        } else {
            toastHeader.classList.remove('bg-success');
            toastHeader.classList.add('bg-danger');
            icon.className = 'bi bi-exclamation-triangle me-2';
        }
        
        toast.show();
    }
    
    // Event handler for filter button
    $('#filterBtn').on('click', function() {
        loadServiceHistory(1); // Reset to first page on new filter
    });
    
    // Event handler for reset button
    $('#resetBtn').on('click', function() {
        $('#filterForm')[0].reset();
        loadServiceHistory(1);
    });
    
    // Event delegation for pagination clicks
    $('#pagination').on('click', '.page-link', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        loadServiceHistory(page);
    });
    
    // Event delegation for view button
    $(document).on('click', '.view-btn', function() {
        const serviceId = $(this).data('id');
        viewServiceHistory(serviceId);
    });
    
    
    // Initial load
    loadCategories();
    loadServiceHistory();
    
    // Inform parent window about loaded height for iframe resizing
    if (window.parent) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 