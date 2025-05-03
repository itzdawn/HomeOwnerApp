/**
 * Service History Management for Home Owners
 * Handles filtering, viewing, rebooking and providing feedback for past services
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
    
    // Function to load service history with pagination and filtering
    function loadServiceHistory(page = 1) {
        const keyword = $('#serviceName').val();
        const dateRange = $('#dateRange').val();
        const cleanerName = $('#cleanerName').val();
        
        // Show loading indicator
        $('#historyTableBody').html('<tr><td colspan="6" class="text-center">Loading service history...</td></tr>');
        
        // API call to get service history
        $.ajax({
            url: '/api/service-history',
            type: 'GET',
            data: {
                keyword: keyword,
                date_range: dateRange,
                cleaner_name: cleanerName,
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
                                    <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${service.id}" data-bs-toggle="modal" data-bs-target="#viewHistoryModal">
                                        <i class="bi bi-eye"></i> View Details
                                    </button>
                                    <button class="btn btn-sm btn-outline-success rebook-list-btn" data-id="${service.id}">
                                        <i class="bi bi-arrow-repeat"></i> Book Again
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
            url: `/api/service-history/${serviceId}`,
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
                $('#viewBookingId').text(service.booking_id || 'N/A');
                
                // Set service ID for rebook button
                $('#rebookBtn').data('id', service.service_id);
                
                // Handle feedback display
                if (service.has_feedback) {
                    // Show existing feedback
                    $('#existingFeedback').show();
                    $('#addFeedbackForm').hide();
                    $('#addFeedbackBtn').hide();
                    
                    // Populate feedback & rating
                    $('#viewFeedback').text(service.feedback || 'No comments provided.');
                    
                    // Update stars to reflect rating
                    const stars = $('#viewRating i');
                    stars.removeClass('bi-star-fill bi-star').addClass('bi-star');
                    for (let i = 0; i < service.rating; i++) {
                        $(stars[i]).removeClass('bi-star').addClass('bi-star-fill');
                    }
                } else {
                    // Show option to add feedback
                    $('#existingFeedback').hide();
                    $('#addFeedbackForm').hide();
                    $('#addFeedbackBtn').show();
                }
            },
            error: function(error) {
                console.error('Error loading service history details:', error);
                $('#viewHistoryModal').modal('hide');
                showToast('Failed to load service details. Please try again.', false);
            }
        });
    }
    
    // Function to rebook a service
    function rebookService(serviceId) {
        $.ajax({
            url: '/api/rebook-service',
            type: 'POST',
            data: { service_id: serviceId },
            success: function(response) {
                showToast('Service added to your cart for booking!', true);
                // Optionally redirect to booking/checkout page
                // window.location.href = '/booking/checkout'; 
            },
            error: function(error) {
                console.error('Error rebooking service:', error);
                showToast('Failed to rebook service. Please try again.', false);
            }
        });
    }
    
    // Function to submit feedback
    function submitFeedback(serviceId, rating, feedback) {
        $.ajax({
            url: '/api/service-feedback',
            type: 'POST',
            data: {
                service_history_id: serviceId,
                rating: rating,
                feedback: feedback
            },
            success: function(response) {
                showToast('Thank you for your feedback!', true);
                
                // Update the UI to show feedback
                $('#existingFeedback').show();
                $('#addFeedbackForm').hide();
                $('#addFeedbackBtn').hide();
                
                // Update displayed feedback
                $('#viewFeedback').text(feedback || 'No comments provided.');
                
                // Update stars to reflect rating
                const stars = $('#viewRating i');
                stars.removeClass('bi-star-fill bi-star').addClass('bi-star');
                for (let i = 0; i < rating; i++) {
                    $(stars[i]).removeClass('bi-star').addClass('bi-star-fill');
                }
            },
            error: function(error) {
                console.error('Error submitting feedback:', error);
                showToast('Failed to submit feedback. Please try again.', false);
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
    
    // Event delegation for rebook button in list
    $(document).on('click', '.rebook-list-btn', function() {
        const serviceId = $(this).data('id');
        rebookService(serviceId);
    });
    
    // Event handler for rebook button in modal
    $('#rebookBtn').on('click', function() {
        const serviceId = $(this).data('id');
        rebookService(serviceId);
        $('#viewHistoryModal').modal('hide');
    });
    
    // Event handler for add feedback button
    $('#addFeedbackBtn').on('click', function() {
        // Reset form
        $('#ratingValue').val(0);
        $('.rating-star').removeClass('bi-star-fill').addClass('bi-star');
        $('#feedback').val('');
        
        // Show feedback form
        $('#existingFeedback').hide();
        $('#addFeedbackForm').show();
    });
    
    // Event handler for cancel feedback button
    $('#cancelFeedbackBtn').on('click', function() {
        $('#addFeedbackForm').hide();
        $('#addFeedbackBtn').show();
    });
    
    // Event handler for rating stars
    $(document).on('click', '.rating-star', function() {
        const value = $(this).data('value');
        $('#ratingValue').val(value);
        
        // Update stars UI
        $('.rating-star').removeClass('bi-star-fill').addClass('bi-star');
        $('.rating-star').each(function() {
            if ($(this).data('value') <= value) {
                $(this).removeClass('bi-star').addClass('bi-star-fill');
            }
        });
    });
    
    // Event handler for submit feedback button
    $('#submitFeedbackBtn').on('click', function() {
        const rating = parseInt($('#ratingValue').val());
        const feedback = $('#feedback').val().trim();
        
        if (rating === 0) {
            showToast('Please select a rating.', false);
            return;
        }
        
        submitFeedback(currentServiceId, rating, feedback);
    });
    
    // Initial load
    loadServiceHistory();
    
    // Inform parent window about loaded height for iframe resizing
    if (window.parent) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 