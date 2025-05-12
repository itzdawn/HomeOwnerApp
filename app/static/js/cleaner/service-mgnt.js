/**
 * Service Management for Cleaners
 * Handles CRUD operations for services offered by cleaners
 */

$(document).ready(function() {
    // Initialize variables
    let currentPage = 1;
    const itemsPerPage = 10;
    
    // Load initial data
    loadServices();
    
    // Handle search button click
    $('#searchBtn').click(function() {
        loadServices(1); // Reset to first page on new search
    });
    
    // Handle reset button click
    $('#resetBtn').click(function() {
        $('#searchForm')[0].reset();
        loadServices(1);
    });
    
    // Handle create service button click
    $('#createServiceBtn').click(function() {
        // Reset form and set for create mode
        resetServiceForm();
        $('#serviceModalLabel').text('Create Service');
        $('#editMode').val('create');
    });
    
    // Handle edit button click
    $(document).on('click', '.edit-btn', function() {
        const serviceId = $(this).data('id');
        editService(serviceId);
    });
    
    // Handle edit from view button click
    $('.edit-from-view').click(function() {
        const serviceId = $('#viewServiceID').text();
        $('#viewServiceModal').modal('hide');
        
        // Wait for the first modal to close before opening the second one
        setTimeout(function() {
            editService(serviceId);
            $('#serviceModal').modal('show');
        }, 500);
    });
    
    // Handle view button click
    $(document).on('click', '.view-btn', function() {
        const serviceId = $(this).data('id');
        viewService(serviceId);
    });
    
    // Handle delete button click
    $(document).on('click', '.delete-btn', function() {
        const serviceId = $(this).data('id');
        const serviceName = $(this).closest('tr').find('td:nth-child(2)').text();
        $('#deleteServiceName').text(serviceName);
        $('#confirmDeleteBtn').data('id', serviceId);
    });
    
    // Handle save service button click
    $('#saveServiceBtn').click(function() {
        saveService();
    });
    
    // Handle confirm delete button click
    $('#confirmDeleteBtn').click(function() {
        const serviceId = $(this).data('id');
        deleteService(serviceId);
    });
    
    // Load services with pagination and filtering
    function loadServices(page = 1) {
        const serviceId = $('#serviceID').val().trim();
        const serviceName = $('#serviceName').val().trim();
        const categoryId = $('#serviceCategory').val();
        
        // Show loading indicator
        $('tbody').html('<tr><td colspan="8" class="text-center">Loading services...</td></tr>');
        
        // Log the request params for debugging
        console.log('Loading services with params:', {
            service_id: serviceId,
            service_name: serviceName,
            categoryId: categoryId,
            page: page,
            items_per_page: itemsPerPage
        });
        
        // Make API call to fetch services
        $.ajax({
            url: '/api/cleaner/services',
            type: 'GET',
            data: {
                service_id: serviceId,
                service_name: serviceName,
                categoryId: categoryId,
                page: page,
                items_per_page: itemsPerPage
            },
            xhrFields: {
                withCredentials: true  
            },
            success: function(response) {
                // Enhanced debugging
                console.log('API Raw Response:', response);
                console.log('Response Type:', typeof response);
                
                // Try to parse response if it's a string
                let parsedResponse = response;
                if (typeof response === 'string') {
                    try {
                        parsedResponse = JSON.parse(response);
                        console.log('Parsed JSON Response:', parsedResponse);
                    } catch (e) {
                        console.error('Failed to parse response as JSON:', e);
                    }
                }
                
                // Use the appropriate response object
                const responseObj = parsedResponse || response;
                
                const services = responseObj.services || [];
                const totalServices = responseObj.total || 0;
                const totalPages = Math.ceil(totalServices / itemsPerPage);
                
                console.log('Services array:', services);
                console.log('First service item (if available):', services[0] || 'No services returned');
                
                // Update current page
                currentPage = page;
                
                if (services.length === 0) {
                    $('tbody').html('<tr><td colspan="8" class="text-center">No services found</td></tr>');
                    updatePagination(0, 0);
                    return;
                }
                
                let tableHtml = '';
                services.forEach(function(service) {
                    // Format date if available
                    const creationDate = service.creationDate || 'N/A';
                    // Get category name directly from the API response
                    const categoryName = service.categoryName || 'N/A';
                    
                    console.log(`Service ${service.id} - Category Name: ${categoryName}, Category ID: ${service.categoryId}`);
                    
                    tableHtml += `
                    <tr>
                        <td class="text-center">${service.id}</td>
                        <td>${service.name}</td>
                        <td class="text-center">${categoryName}</td>
                        <td class="text-center">$${parseFloat(service.price).toFixed(2)}</td>
                        <td class="text-center">${service.shortlists || 0}</td>
                        <td class="text-center">${service.views || 0}</td>
                        <td class="text-center">${creationDate}</td>
                        <td class="text-center">
                            <div class="d-flex justify-content-center gap-2">
                                <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${service.id}" data-bs-toggle="modal" data-bs-target="#viewServiceModal">
                                    <i class="bi bi-eye"></i> View
                                </button>
                                <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${service.id}" data-bs-toggle="modal" data-bs-target="#serviceModal">
                                    <i class="bi bi-pencil"></i> Edit
                                </button>
                                <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${service.id}" data-bs-toggle="modal" data-bs-target="#deleteServiceModal">
                                    <i class="bi bi-trash"></i> Delete
                                </button>
                            </div>
                        </td>
                    </tr>`
                });
                
                // Update table body
                $('tbody').html(tableHtml);
                
                // Update pagination
                updatePagination(page, totalPages, totalServices);
            },
            error: function(error) {
                console.error('Error loading services:', error);
                // Enhanced error logging
                console.error('Error status:', error.status);
                console.error('Error text:', error.statusText);
                console.error('Error response:', error.responseText);
                $('tbody').html('<tr><td colspan="8" class="text-center text-danger">Error loading services. Please try again.</td></tr>');
            }
        });
    }
    
    // View service details
    function viewService(serviceId) {
        $.ajax({
            url: `/api/cleaner/services/${serviceId}`,
            type: 'GET',
            xhrFields: {
                withCredentials: true
            },
            success: function(service) {
                // Populate service details in modal
                $('#viewServiceID').text(service.id);
                $('#viewServiceName').text(service.name);
                // Display category name directly from the API response (service_category.name)
                $('#viewCategory').text(service.categoryName || 'N/A'); // Expecting API to provide categoryName
                $('#viewDescription').text(service.description);
                $('#viewPrice').text(parseFloat(service.price).toFixed(2));
                $('#viewShortlists').text(service.shortlists || 0);
                $('#viewViews').text(service.views || 0);
                $('#viewCreationDate').text(service.creationDate || 'N/A');
            },
            error: function(error) {
                console.error('Error loading service details:', error);
                $('#viewServiceModal').modal('hide');
                showToast('Failed to load service details. Please try again.', false);
            }
        });
    }
    
    // Edit service
    function editService(serviceId) {
        // Set modal title for edit mode
        $('#serviceModalLabel').text('Edit Service');
        $('#editMode').val('edit');
        
        $.ajax({
            url: `/api/cleaner/services/${serviceId}`,
            type: 'GET',
            xhrFields: {
                withCredentials: true
            },
            success: function(service) {
                console.log('Edit service data:', service);
                
                // Populate form with service details
                $('#modalServiceID').val(service.id);
                $('#modalServiceName').val(service.name);
                $('#modalCategory').val(service.categoryId);
                $('#modalDescription').val(service.description);
                $('#modalPrice').val(parseFloat(service.price).toFixed(2));
                
                // Handle any other specific fields or validations here
            },
            error: function(error) {
                console.error('Error loading service for edit:', error);
                $('#serviceModal').modal('hide');
                showToast('Failed to load service for editing. Please try again.', false);
            }
        });
    }
    
    // Save service (create or update)
    function saveService() {
        // Get form data
        const mode = $('#editMode').val();
        const isEdit = mode === 'edit';
        const serviceId = $('#modalServiceID').val();
        const serviceName = $('#modalServiceName').val().trim();
        const categoryId = parseInt($('#modalCategory').val(), 10);
        const description = $('#modalDescription').val().trim();
        const price = parseFloat($('#modalPrice').val());
        
        // Get optional fields if they exist
        const duration = $('#modalDuration').length ? parseFloat($('#modalDuration').val()) : null;
        const availability = $('#modalAvailability').length ? $('#modalAvailability').val() : 'available';
        
        // Validate form
        if (!serviceName) {
            showToast('Service name is required', false);
            return;
        }
        
        if (!categoryId) {
            showToast('Category is required', false);
            return;
        }
        
        if (!description) {
            showToast('Description is required', false);
            return;
        }
        
        if (isNaN(price) || price <= 0) {
            showToast('Valid price is required', false);
            return;
        }
        
        // Validate duration if it exists in the form
        if (duration !== null && (isNaN(duration) || duration <= 0)) {
            showToast('Valid duration is required', false);
            return;
        }
        
        // Prepare data - matching the entity field names
        const serviceData = {
            name: serviceName,
            description: description,
            categoryId: categoryId,
            price: price
        };
        
        // Add optional fields if they exist and are valid
        if (duration !== null) {
            serviceData.duration = duration;
        }
        if (availability) {
            serviceData.availability = availability;
        }
        
        // API endpoint and method based on create/edit mode
        const url = isEdit ? `/api/cleaner/services/${serviceId}` : '/api/cleaner/services';
        const method = isEdit ? 'PUT' : 'POST';
        
        console.log('Saving service with data:', serviceData);
        
        // Make API call
        $.ajax({
            url: url,
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(serviceData),
            xhrFields: {
                withCredentials: true
            },
            success: function(response) {
                console.log('Save service response:', response);
                showToast(`Service ${isEdit ? 'updated' : 'created'} successfully`, true);
                $('#serviceModal').modal('hide');
                
                // Reload services to refresh the list
                setTimeout(function() {
                    loadServices(currentPage);
                }, 500);
            },
            error: function(error) {
                console.error('Error saving service:', error);
                const errorMsg = getErrorMessage(error);
                showToast(`Failed to ${isEdit ? 'update' : 'create'} service: ${errorMsg}`, false);
            }
        });
    }
    
    // Delete service
    function deleteService(serviceId) {
        $.ajax({
            url: `/api/cleaner/services/${serviceId}`,
            type: 'DELETE',
            xhrFields: {
                withCredentials: true
            },
            success: function(response) {
                showToast('Service deleted successfully', true);
                $('#deleteServiceModal').modal('hide');
                loadServices(currentPage);
            },
            error: function(error) {
                console.error('Error deleting service:', error);
                const errorMsg = getErrorMessage(error);
                showToast(`Failed to delete service: ${errorMsg}`, false);
                $('#deleteServiceModal').modal('hide');
            }
        });
    }
    
    // Reset service form
    function resetServiceForm() {
        $('#serviceForm')[0].reset();
        $('#modalServiceID').val('');
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
    
    // Show toast message
    function showToast(message, isSuccess) {
        const toastEl = document.getElementById('successToast');
        const toast = new bootstrap.Toast(toastEl);
        
        $('#toastMessage').text(message);
        
        const toastHeader = toastEl.querySelector('.toast-header');
        if (isSuccess) {
            toastHeader.classList.remove('bg-danger');
            toastHeader.classList.add('bg-success');
            toastHeader.querySelector('strong').textContent = 'Success';
            toastHeader.querySelector('i').className = 'bi bi-check-circle me-2';
        } else {
            toastHeader.classList.remove('bg-success');
            toastHeader.classList.add('bg-danger');
            toastHeader.querySelector('strong').textContent = 'Error';
            toastHeader.querySelector('i').className = 'bi bi-exclamation-triangle me-2';
        }
        
        toast.show();
    }
    
    // Notify parent page that iframe content is loaded
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }


    // Update pagination controls
    function updatePagination(currentPage, totalPages, totalItems = 0) {
        // Update total count
        $('.pagination-container .text-muted').text(`Total of ${totalItems} services found`);
        
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
            loadServices(page);
        }
    });
}); 