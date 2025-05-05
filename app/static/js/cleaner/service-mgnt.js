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
        const category = $('#serviceCategory').val();
        
        // Show loading indicator
        $('tbody').html('<tr><td colspan="6" class="text-center">Loading services...</td></tr>');
        
        // Log the request params for debugging
        console.log('Loading services with params:', {
            service_id: serviceId,
            service_name: serviceName,
            category: category,
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
                category: category,
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
                    $('tbody').html('<tr><td colspan="6" class="text-center">No services found</td></tr>');
                    updatePagination(0, 0);
                    return;
                }
                
                let tableHtml = '';
                services.forEach(function(service) {
                    tableHtml += `
                    <tr>
                        <td class="text-center">${service.id}</td>
                        <td>${service.name}</td>
                        <td class="service-description">${service.description}</td>
                        <td class="text-center">$${service.price.toFixed(2)}</td>
                        <td class="text-center">
                            <span class="metric-badge me-2"><i class="bi bi-eye"></i> ${service.views}</span>
                            <span class="metric-badge"><i class="bi bi-bookmark"></i> ${service.shortlists}</span>
                        </td>
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
                    </tr>`;
                });
                
                // Update table body
                $('tbody').html(tableHtml);
                
                // Update pagination
                updatePagination(page, totalPages, totalServices);
            },
            error: function(error) {
                console.error('Error loading services:', error);
                // Log detailed error information
                console.error('Error details:', error.responseText || error.statusText);
                $('tbody').html('<tr><td colspan="6" class="text-center text-danger">Error loading services. Please try again.</td></tr>');
            }
        });
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
    
    // View service details
    function viewService(serviceId) {
        $.ajax({
            url: `/api/cleaner/services/${serviceId}`,
            type: 'GET',
            xhrFields: {
                withCredentials: true  // Ensures cookies are sent with the request
            },
            success: function(service) {
                // Populate service details in modal
                $('#viewServiceID').text(service.id);
                $('#viewServiceName').text(service.name);
                $('#viewCategory').text(service.category_name);
                $('#viewDescription').text(service.description);
                $('#viewPrice').text(service.price.toFixed(2));
                $('#viewDuration').text(service.duration);
                $('#viewAvailability').text(service.availability === 'available' ? 'Available' : 'Unavailable');
                $('#viewViews').text(service.views);
                $('#viewShortlists').text(service.shortlists);
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
                withCredentials: true  // Ensures cookies are sent with the request
            },
            success: function(service) {
                // Populate form with service details
                $('#modalServiceID').val(service.id);
                $('#modalServiceName').val(service.name);
                $('#modalCategory').val(service.category_id);
                $('#modalDescription').val(service.description);
                $('#modalPrice').val(service.price.toFixed(2));
                $('#modalDuration').val(service.duration);
                $('#modalAvailability').val(service.availability);
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
        const categoryId = $('#modalCategory').val();
        const description = $('#modalDescription').val().trim();
        const price = parseFloat($('#modalPrice').val());
        const duration = parseFloat($('#modalDuration').val());
        const availability = $('#modalAvailability').val();
        
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
        
        if (isNaN(duration) || duration <= 0) {
            showToast('Valid duration is required', false);
            return;
        }
        
        // Prepare data
        const serviceData = {
            name: serviceName,
            category_id: categoryId,
            description: description,
            price: price,
            duration: duration,
            availability: availability
        };
        
        // API endpoint and method based on create/edit mode
        const url = isEdit ? `/api/cleaner/services/${serviceId}` : '/api/cleaner/services';
        const method = isEdit ? 'PUT' : 'POST';
        
        // Make API call
        $.ajax({
            url: url,
            type: method,
            data: serviceData,
            xhrFields: {
                withCredentials: true  // Ensures cookies are sent with the request
            },
            success: function(response) {
                showToast(`Service ${isEdit ? 'updated' : 'created'} successfully`, true);
                $('#serviceModal').modal('hide');
                loadServices(currentPage);
            },
            error: function(error) {
                console.error('Error saving service:', error);
                showToast(`Failed to ${isEdit ? 'update' : 'create'} service. Please try again.`, false);
            }
        });
    }
    
    // Delete service
    function deleteService(serviceId) {
        $.ajax({
            url: `/api/cleaner/services/${serviceId}`,
            type: 'DELETE',
            xhrFields: {
                withCredentials: true  // Ensures cookies are sent with the request
            },
            success: function(response) {
                showToast('Service deleted successfully', true);
                $('#deleteServiceModal').modal('hide');
                loadServices(currentPage);
            },
            error: function(error) {
                console.error('Error deleting service:', error);
                showToast('Failed to delete service. Please try again.', false);
                $('#deleteServiceModal').modal('hide');
            }
        });
    }
    
    // Reset service form
    function resetServiceForm() {
        $('#serviceForm')[0].reset();
        $('#modalServiceID').val('');
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
        } else {
            toastHeader.classList.remove('bg-success');
            toastHeader.classList.add('bg-danger');
        }
        
        toast.show();
    }
    
    // Notify parent page that iframe content is loaded
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 