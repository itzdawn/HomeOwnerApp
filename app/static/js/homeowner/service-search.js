/**
 * Service Search functionality for Home Owners
 * Handles searching, viewing and shortlisting services
 */

$(document).ready(function() {
    // Global variables
    let currentPage = 1;
    const itemsPerPage = 10;
    
    // Function to load categories
    function loadCategories() {
        // API call to get categories
        $.ajax({
            url: '/api/service-categories',
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
    
    // Function to load services with pagination and filtering
    function loadServices(page = 1) {
        const keyword = $('#serviceName').val();
        const categoryId = $('#serviceCategory').val();
        
        // Show loading indicator
        $('#serviceTableBody').html('<tr><td colspan="5" class="text-center">Loading services...</td></tr>');
        
        // API call to get services
        $.ajax({
            url: '/api/services',
            type: 'GET',
            data: {
                keyword: keyword,
                category_id: categoryId,
                page: page,
                items_per_page: itemsPerPage
            },
            success: function(response) {
                const services = response.services || [];
                const totalServices = response.total || 0;
                const totalPages = Math.ceil(totalServices / itemsPerPage);
                
                // Update total count
                $('#total-found').text(`Total of ${totalServices} services found`);
                
                // Generate table rows
                if (services.length === 0) {
                    $('#serviceTableBody').html('<tr><td colspan="5" class="text-center text-muted">No services found matching your criteria.</td></tr>');
                } else {
                    let tableHtml = '';
                    services.forEach(function(service) {
                        tableHtml += `
                        <tr>
                            <td>${service.name}</td>
                            <td>${service.category_name}</td>
                            <td class="service-description">${service.description}</td>
                            <td class="text-center">$${service.price.toFixed(2)}</td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${service.id}" data-bs-toggle="modal" data-bs-target="#viewServiceModal">
                                        <i class="bi bi-eye"></i> View
                                    </button>
                                    <button class="btn btn-sm btn-outline-success shortlist-btn" data-id="${service.id}">
                                        <i class="bi bi-bookmark-plus"></i> Shortlist
                                    </button>
                                </div>
                            </td>
                        </tr>`;
                    });
                    $('#serviceTableBody').html(tableHtml);
                }
                
                // Generate pagination
                generatePagination(page, totalPages);
                
                // Update current page
                currentPage = page;
            },
            error: function(error) {
                console.error('Error loading services:', error);
                $('#serviceTableBody').html('<tr><td colspan="5" class="text-center text-danger">Error loading services. Please try again.</td></tr>');
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
            url: `/api/services/${serviceId}`,
            type: 'GET',
            success: function(service) {
                // Populate modal with service details
                $('#viewServiceName').text(service.name);
                $('#viewCleanerName').text(service.cleaner_name);
                $('#viewCategory').text(service.category_name);
                $('#viewDescription').text(service.description);
                $('#viewPrice').text(service.price.toFixed(2));
                $('#viewDuration').text(service.duration);
                $('#viewAvailability').text(service.availability === 'available' ? 'Available' : 'Unavailable');
                
                // Set service ID for shortlist button
                $('.shortlist-from-view-btn').data('id', service.id);
            },
            error: function(error) {
                console.error('Error loading service details:', error);
                $('#viewServiceModal').modal('hide');
                showToast('Failed to load service details. Please try again.', false);
            }
        });
    }
    
    // Function to shortlist a service
    function shortlistService(serviceId) {
        $.ajax({
            url: '/api/shortlist',
            type: 'POST',
            data: { service_id: serviceId },
            success: function(response) {
                showToast('Service shortlisted successfully!', true);
            },
            error: function(error) {
                console.error('Error shortlisting service:', error);
                showToast('Failed to shortlist service. Please try again.', false);
            }
        });
    }
    
    // Function to show toast message
    function showToast(message, isSuccess) {
        const toastEl = document.getElementById('successToast');
        const toastHeader = toastEl.querySelector('.toast-header');
        const toast = new bootstrap.Toast(toastEl);
        
        $('#toastMessage').text(message);
        
        if (isSuccess) {
            toastHeader.classList.remove('bg-danger');
            toastHeader.classList.add('bg-success');
        } else {
            toastHeader.classList.remove('bg-success');
            toastHeader.classList.add('bg-danger');
        }
        
        toast.show();
    }
    
    // Event handler for search button
    $('#searchBtn').on('click', function() {
        loadServices(1); // Reset to first page on new search
    });
    
    // Event handler for reset button
    $('#resetBtn').on('click', function() {
        $('#searchForm')[0].reset();
        loadServices(1);
    });
    
    // Event delegation for pagination clicks
    $('#pagination').on('click', '.page-link', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        loadServices(page);
    });
    
    // Event delegation for view button
    $(document).on('click', '.view-btn', function() {
        const serviceId = $(this).data('id');
        viewService(serviceId);
    });
    
    // Event delegation for shortlist button
    $(document).on('click', '.shortlist-btn, .shortlist-from-view-btn', function() {
        const serviceId = $(this).data('id');
        shortlistService(serviceId);
        
        // Close modal if shortlisting from modal
        if ($(this).hasClass('shortlist-from-view-btn')) {
            $('#viewServiceModal').modal('hide');
        }
    });
    
    // Initial load
    loadCategories();
    loadServices();
    
    // Inform parent window about loaded height for iframe resizing
    if (window.parent) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 