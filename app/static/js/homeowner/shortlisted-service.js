/**
 * Shortlisted Services Management for Home Owners
 * Handles filtering, viewing and removing shortlisted services
 */

$(document).ready(function() {
    // Global variables
    let currentPage = 1;
    const itemsPerPage = 10;
    
    // Function to load categories
    function loadCategories() {
        $.ajax({
            url: '/api/cleaner/service-categories',
            type: 'GET',
            success: function(categories) {
                const categorySelect = $('#serviceCategory');
                categorySelect.empty();
                categorySelect.append('<option value="">All categories</option>');
                
                // Add each category to dropdown
                categories.forEach(function(category) {
                    categorySelect.append(`<option value="${category.id}">${category.name}</option>`);
                });
            },
            error: function(error) {
                console.error('Error loading categories:', error);
            }
        });
    }
    
    // Function to load shortlisted services with pagination and filtering
    function loadShortlistedServices(page = 1) {
        const keyword = $('#serviceName').val();
        const categoryId = $('#serviceCategory').val();
        
        // Show loading indicator
        $('#shortlistTableBody').html('<tr><td colspan="5" class="text-center">Loading shortlisted services...</td></tr>');
        
        // API call to get shortlisted services
        $.ajax({
            url: '/api/homeowner/shortlisted-services',
            type: 'GET',
            data: {
                service_name: keyword,
                categoryId: categoryId,
                page: page,
                items_per_page: itemsPerPage
            },
            success: function(response) {
                const services = response.services || [];
                const totalServices = response.total || 0;
                const totalPages = Math.ceil(totalServices / itemsPerPage);
                
                // Update total count
                $('#total-shortlisted').text(`Total of ${totalServices} shortlisted services found`);
                
                // Generate table rows
                if (services.length === 0) {
                    $('#shortlistTableBody').html('<tr><td colspan="5" class="text-center text-muted">You haven\'t shortlisted any services yet.</td></tr>');
                } else {
                    let tableHtml = '';
                    services.forEach(function(service) {
                        tableHtml += `
                        <tr>
                            <td>${service.name}</td>
                            <td>${service.categoryName}</td>
                            <td class="service-description">${service.description}</td>
                            <td class="text-center">$${service.price.toFixed(2)}</td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${service.id}" data-bs-toggle="modal" data-bs-target="#viewServiceModal">
                                        <i class="bi bi-eye"></i> View
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger remove-shortlist-btn" data-id="${service.id}" data-name="${service.name}" data-bs-toggle="modal" data-bs-target="#removeShortlistModal">
                                        <i class="bi bi-bookmark-dash"></i> Remove
                                    </button>
                                </div>
                            </td>
                        </tr>`;
                    });
                    $('#shortlistTableBody').html(tableHtml);
                }
                
                // Generate pagination
                generatePagination(page, totalPages);
                
                // Update current page
                currentPage = page;
            },
            error: function(error) {
                console.error('Error loading shortlisted services:', error);
                $('#shortlistTableBody').html('<tr><td colspan="5" class="text-center text-danger">Error loading shortlisted services. Please try again.</td></tr>');
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
    
    // Function to view service details
    function viewService(serviceId) {
        $.ajax({
            url: `/api/homeowner/shortlisted-services/${serviceId}`,
            type: 'GET',
            success: function(service) {
                // Populate modal with service details
                $('#viewServiceName').text(service.name);
                $('#viewCleanerName').text(service.cleanerName);
                $('#viewCategory').text(service.categoryName);
                $('#viewDescription').text(service.description);
                $('#viewPrice').text(service.price.toFixed(2));
                $('#viewShortlistDate').text(service.shortlistDate);
                
                // Set service ID for remove button
                $('.remove-from-view-btn').data('id', service.id);
                $('.remove-from-view-btn').data('name', service.name);
            },
            error: function(error) {
                console.error('Error loading service details:', error);
                $('#viewServiceModal').modal('hide');
                showToast('Failed to load service details. Please try again.', false);
            }
        });
    }
    
    // Function to remove a service from shortlist
    function removeShortlistedService(serviceId) {
        $.ajax({
            url: `/api/homeowner/shortlist/${serviceId}`,
            type: 'DELETE',
            success: function(response) {
                showToast('Service removed from shortlist successfully!', true);
                loadShortlistedServices(currentPage); // Reload current page
            },
            error: function(error) {
                console.error('Error removing service from shortlist:', error);
                showToast('Failed to remove service from shortlist. Please try again.', false);
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
        loadShortlistedServices(1); // Reset to first page on new filter
    });
    
    // Event handler for reset button
    $('#resetBtn').on('click', function() {
        $('#filterForm')[0].reset();
        loadShortlistedServices(1);
    });
    
    // Event delegation for pagination clicks
    $('#pagination').on('click', '.page-link', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        loadShortlistedServices(page);
    });
    
    // Event delegation for view button
    $(document).on('click', '.view-btn', function() {
        const serviceId = $(this).data('id');
        viewService(serviceId);
    });
    
    // Event delegation for remove button
    $(document).on('click', '.remove-shortlist-btn', function() {
        const serviceId = $(this).data('id');
        const serviceName = $(this).data('name');
        $('#removeServiceName').text(serviceName);
        $('#confirmRemoveBtn').data('id', serviceId);
    });
    
    // Event delegation for remove button in view modal
    $(document).on('click', '.remove-from-view-btn', function() {
        const serviceId = $(this).data('id');
        const serviceName = $(this).data('name') || $('#viewServiceName').text();
        $('#removeServiceName').text(serviceName);
        $('#confirmRemoveBtn').data('id', serviceId);
    });
    
    // Event handler for confirm remove button
    $('#confirmRemoveBtn').on('click', function() {
        const serviceId = $(this).data('id');
        removeShortlistedService(serviceId);
        $('#removeShortlistModal').modal('hide');
    });
    
    // Initial load
    loadCategories();
    loadShortlistedServices();
    
    // Inform parent window about loaded height for iframe resizing
    if (window.parent) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 