/**
 * Service History Management for Cleaners
 * Handles searching, filtering, and viewing completed service details
 */

$(document).ready(function() {
    // Initialize variables
    let currentPage = 1;
    const itemsPerPage = 10;
    
    // Load initial data
    loadServiceHistory();
    
    // Handle search button click
    $('#searchBtn').click(function() {
        loadServiceHistory(1); // Reset to first page on new search
    });
    
    // Handle reset button click
    $('#resetBtn').click(function() {
        $('#searchForm')[0].reset();
        loadServiceHistory(1);
    });
    
    // Load service history with pagination and filtering
    function loadServiceHistory(page = 1) {
        // Get filter parameters
        const serviceName = $('#serviceName').val().trim();
        const categoryId = $('#serviceCategory').val();
        const startDate = $('#startDate').val();
        const endDate = $('#endDate').val();
        // Show loading indicator
        $('tbody').html('<tr><td colspan="7" class="text-center">Loading service history...</td></tr>');
        
        // Log the request params for debugging
       console.log('Loading service history with params:', {
            service_name: serviceName,
            categoryId: categoryId,
            start_date: startDate,
            end_date: endDate,
            page: page,
            items_per_page: itemsPerPage
        });
                
        // Make API call to fetch service history
        $.ajax({
            url: '/api/cleaner/service-history',
            type: 'GET',
            data: {
                service_name: serviceName,
                categoryId: categoryId,
                start_date: startDate,
                end_date: endDate,
                page: page,
                items_per_page: itemsPerPage
            },
            xhrFields: {
                withCredentials: true
            },
            success: function(response) {
                // Log the response for debugging
                console.log('API Response:', response);
                
                const services = response.services || [];
                const totalServices = response.total || 0;
                const totalPages = Math.ceil(totalServices / itemsPerPage);
                
                // Update current page
                currentPage = page;
                
                if (services.length === 0) {
                    $('tbody').html('<tr><td colspan="6" class="text-center">No service history found</td></tr>');
                    updatePagination(0, 0);
                    return;
                }
                
                let tableHtml = '';
                services.forEach(function(service) {
                    // Get formatted values
                    const rating = parseFloat(service.rating || 0);
                    const ratingHtml = generateRatingStars(rating);
                    
                    // Use safe property access with proper mapping to display names instead of IDs
                    const homeownerName = service.homeowner_name || 'Unknown';
                    const serviceName = service.name || 'N/A';
                    const serviceDateFormatted = service.service_date || 'N/A';
                    const categoryName = service.category_name || 'N/A';
                    const serviceId = service.CompletedServiceId || service.id || service.service_id;
                    
                    tableHtml += `
                    <tr 
                        data-id="${serviceId}"
                        data-name="${serviceName}"
                        data-category-name="${categoryName}"
                        data-category-id="${service.categoryId}"
                        data-homeowner="${homeownerName}"
                        data-date="${serviceDateFormatted}">
                        
                        <td class="text-center">${serviceId}</td>
                        <td>${serviceName}</td>
                        <td class="text-center">${categoryName}</td>
                        <td class="text-center">${serviceDateFormatted}</td>
                        <td>${homeownerName}</td>
                        <td class="text-center"><span class="badge bg-success">Completed</span></td>
                        <td class="text-center">
                            <div class="d-flex justify-content-center gap-2">
                                <button class="btn btn-sm btn-outline-secondary view-btn" data-bs-toggle="modal" data-bs-target="#viewServiceModal">
                                    <i class="bi bi-eye"></i> View Details
                                </button>
                            </div>
                        </td>
                    </tr>`;
                });
                
                // Update table body
                $('tbody').html(tableHtml);
                
                // Update pagination
                updatePagination(page, totalPages, totalServices);
            },
            error: function(error) {
                console.error('Error loading service history:', error);
                // Log detailed error information
                console.error('Error details:', error.responseText || error.statusText);
                $('tbody').html('<tr><td colspan="6" class="text-center text-danger">Error loading service history. Please try again.</td></tr>');
            }
        });
    }
    
    // Generate rating stars HTML based on rating value
    function generateRatingStars(rating) {
        let html = '';
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        
        // Add full stars
        for (let i = 0; i < fullStars; i++) {
            html += '<i class="bi bi-star-fill text-warning"></i>';
        }
        
        // Add half star if needed
        if (halfStar) {
            html += '<i class="bi bi-star-half text-warning"></i>';
        }
        
        // Add empty stars
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            html += '<i class="bi bi-star text-warning"></i>';
        }
        
        return html;
    }
    
    // Update pagination controls
    function updatePagination(currentPage, totalPages, totalItems = 0) {
        // Update total count
        $('.pagination-container .text-muted').text(`Total of ${totalItems} completed services found`);
        
        const pagination = $('.pagination');
        pagination.empty();
        
        // No pagination needed if only one page
        if (totalPages <= 1) {
            pagination.append(`
                <li class="page-item disabled">
                    <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
                </li>
                <li class="page-item active"><a class="page-link" href="#">1</a></li>
                <li class="page-item disabled">
                    <a class="page-link" href="#">Next</a>
                </li>
            `);
            return;
        }
        
        // Previous button
        pagination.append(`
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage - 1}" tabindex="-1">Previous</a>
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
    
    // Handle pagination clicks
    $(document).on('click', '.pagination .page-link', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        if (page) {
            loadServiceHistory(page);
        }
    });
    
    // Handle view button click
    $(document).on('click', '.view-btn', function () {
        const serviceId = $(this).closest('tr').data('id');

        $.get(`/api/cleaner/completed-service/${serviceId}`, function (service) {
            displayServiceDetails(service);
        }).fail(function (xhr) {
            const errorMessage = xhr.responseJSON?.error || "Unknown error";
            alert("Failed to load service details: " + errorMessage);
        });
    });
    
    // View service details in modal 
    function displayServiceDetails(service) {
        $('#viewCompletedServiceId').text(service.CompletedServiceId || 'N/A');
        $('#viewServiceName').text(service.name || 'N/A');               // Modal title
        $('#viewServiceNameText').text(service.name || 'N/A');           // Detail row
        $('#viewCategory').text(service.category_name || 'N/A');
        $('#viewHomeOwner').text(service.homeowner_name || 'N/A');
        $('#viewServiceDate').text(service.service_date || 'N/A');
        $('#viewStatus').html('<span class="badge bg-success">Completed</span>');
    }
    
    
    // Extract error message from response
    function getErrorMessage(xhr) {
        let errorMsg = 'Unknown error occurred';
        try {
            if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMsg = xhr.responseJSON.message;
            } else if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMsg = xhr.responseJSON.error;
            } else if (xhr.responseText) {
                const response = JSON.parse(xhr.responseText);
                errorMsg = response.message || response.error || errorMsg;
            }
        } catch (e) {
            console.warn('Could not parse error response as JSON');
        }
        return errorMsg || xhr.statusText || 'Server error';
    }
    
    // Notify parent page that iframe content is loaded (if in iframe)
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 