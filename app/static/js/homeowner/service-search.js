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
        fetch("/api/cleaner/service-categories") 
            .then(response => response.json())
            .then(categories => {
                const select = document.getElementById("serviceCategory");

                // Clear and add default option
                select.innerHTML = '<option value="">All categories</option>';

                // Add each category as an option
                categories.forEach(category => {
                    const option = document.createElement("option");
                    option.value = category.id;
                    option.textContent = category.name;
                    select.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Failed to load categories:", error);
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
            url: '/api/homeowner/available-services',
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
                            <td>${service.categoryName}</td>
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
            url: `/api/homeowner/services/${serviceId}`,
            type: 'GET',
            success: function(service) {
                // Populate modal with service details
                $('#viewServiceName').text(service.name);
                $('#viewCleanerName').text(service.cleanerName);
                $('#viewCategory').text(service.categoryName);
                $('#viewDescription').text(service.description);
                $('#viewPrice').text(service.price.toFixed(2));
                
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
            url: '/api/homeowner/shortlist',
            type: 'POST',
            data: { service_id: serviceId },
             contentType: 'application/x-www-form-urlencoded',
            success: function(response) {
                showToast('Service shortlisted successfully!', true);
                if (window.parent) {
                    window.parent.postMessage({ type: 'refreshShortlist' }, '*');
                }
            },
            error: function(error) {
                console.error('Error shortlisting service:', error);
                let message = 'Failed to shortlist service. Please try again.';
                if (error.responseJSON && error.responseJSON.error) {
                    message = error.responseJSON.error;
                }
                showToast(message, false);
            }
        });
    }
    
    // Function to show toast message
    function showToast(message, isSuccess) {
        const toastEl = document.getElementById('successToast');
        const toastHeader = toastEl.querySelector('.toast-header');
        const icon = toastHeader.querySelector('i');
        const title = toastHeader.querySelector('strong');
        const toast = new bootstrap.Toast(toastEl);

        $('#toastMessage').text(message);

        if (isSuccess) {
            toastHeader.classList.remove('bg-danger');
            toastHeader.classList.add('bg-success');
            icon.className = 'bi bi-check-circle me-2';
            title.textContent = 'Success';
        } else {
            toastHeader.classList.remove('bg-success');
            toastHeader.classList.add('bg-danger');
            icon.className = 'bi bi-exclamation-triangle me-2';
            title.textContent = 'Error';
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