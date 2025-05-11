/**
 * Service Categories Management for Platform Administrators
 * Handles CRUD operations for service categories
 */

$(document).ready(function() {
    // Global variables
    let currentPage = 1;
    const itemsPerPage = 10;
    
    // Function to load categories with pagination and filtering
    function loadCategories(page = 1) {
        const categoryName = $('#categoryName').val();  
        const categoryId = $('#categoryId').val();    
        
        // Show loading indicator
        $('#categoryTableBody').html('<tr><td colspan="4" class="text-center">Loading categories...</td></tr>');
        
        // API call to get categories
        $.ajax({
            url: '/api/platform/service-categories', 
            type: 'GET',
            data: {
                name: categoryName,     
                category_id: categoryId,      
                page: page,                   
                items_per_page: itemsPerPage 
            },
            success: function(response) {
                const categories = response.categories || [];
                const totalCategories = response.total || 0;
                const totalPages = Math.ceil(totalCategories / itemsPerPage);
                
                // Update total count
                $('#total-categories').text(`Total of ${totalCategories} categories found`);
                
                // Generate table rows
                if (categories.length === 0) {
                    $('#categoryTableBody').html('<tr><td colspan="4" class="text-center text-muted">No categories found.</td></tr>');
                } else {
                    let tableHtml = '';
                    categories.forEach(function(category) {
                        tableHtml += `
                        <tr>
                            <td class="text-center">${category.id}</td>
                            <td>${category.name}</td>
                            <td class="service-description">${category.description || ''}</td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${category.id}" data-bs-toggle="modal" data-bs-target="#viewCategoryModal">
                                        <i class="bi bi-eye"></i> View
                                    </button>
                                    <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${category.id}" data-bs-toggle="modal" data-bs-target="#categoryModal">
                                        <i class="bi bi-pencil"></i> Edit
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${category.id}" data-name="${category.name}" data-bs-toggle="modal" data-bs-target="#deleteCategoryModal">
                                        <i class="bi bi-trash"></i> Delete
                                    </button>
                                </div>
                            </td>
                        </tr>`;
                    });
                    $('#categoryTableBody').html(tableHtml);
                }
                
                // Generate pagination
                generatePagination(page, totalPages);
                
                // Update current page
                currentPage = page;
            },
            error: function(error) {
                console.error('Error loading categories:', error);
                $('#categoryTableBody').html('<tr><td colspan="4" class="text-center text-danger">Error loading categories. Please try again.</td></tr>');
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
    
    // Function to view category details
    function viewCategory(categoryId) {
        $.ajax({
            url: `/api/platform/service-categories/${categoryId}`,
            type: 'GET',
            success: function(category) {
                // Populate modal with category details
                $('#viewCategoryID').text(category.id);
                $('#viewCategoryName').text(category.name);
                $('#viewCategoryDescription').text(category.description || 'No description provided.');
                $('#viewCategoryServices').text(category.service_count || 0);
                
                // Set category ID for edit button
                $('.edit-from-view-btn').data('id', category.id);
            },
            error: function(error) {
                console.error('Error loading category details:', error);
                $('#viewCategoryModal').modal('hide');
                showToast('Failed to load category details. Please try again.', false);
            }
        });
    }
    
    // Function to get category for editing
    function editCategory(categoryId) {
        // Set modal title for edit mode
        $('#categoryModalLabel').text('Edit Category');
        
        // Store category ID for save
        $('#editCategoryId').val(categoryId);
        
        $.ajax({
            url: `/api/platform/service-categories/${categoryId}`,
            type: 'GET',
            success: function(category) {
                // Populate form with category details
                $('#modalCategoryName').val(category.name);
                $('#modalCategoryDescription').val(category.description || '');
            },
            error: function(error) {
                console.error('Error loading category for edit:', error);
                $('#categoryModal').modal('hide');
                showToast('Failed to load category for editing. Please try again.', false);
            }
        });
    }
    
    // Function to save (create or update) category
    function saveCategory(isEdit, formData) {
        const url = isEdit ? `/api/platform/service-categories/${formData.id}` : '/api/platform/service-categories';
        const method = isEdit ? 'PUT' : 'POST';
        
        $.ajax({
            url: url,
            type: method,
            data: $.param(formData), 
            contentType: 'application/x-www-form-urlencoded',
            success: function(response) {
                showToast(`Category ${isEdit ? 'updated' : 'created'} successfully!`, true);
                $('#categoryModal').modal('hide');
                loadCategories(currentPage); // Reload current page
            },
            error: function(error) {
                console.error(`Error ${isEdit ? 'updating' : 'creating'} category:`, error);
                showToast(`Failed to ${isEdit ? 'update' : 'create'} category. Please try again.`, false);
            }
        });
    }
    
    // Function to delete category
    function deleteCategory(categoryId) {
        $.ajax({
            url: `/api/platform/service-categories/${categoryId}`,
            type: 'DELETE',
            success: function(response) {
                showToast('Category deleted successfully!', true);
                loadCategories(currentPage); // Reload current page
            },
            error: function(error) {
                console.error('Error deleting category:', error);
                showToast('Failed to delete category. Please try again.', false);
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
    
    // Event handler for search button
    $('#searchBtn').on('click', function() {
        loadCategories(1); // Reset to first page on new search
    });
    
    // Event handler for reset button
    $('#resetBtn').on('click', function() {
        $('#searchForm')[0].reset();
        loadCategories(1);
    });
    
    // Event handler for create category button
    $('#createCategoryBtn').on('click', function() {
        // Reset form and set for create mode
        $('#categoryForm')[0].reset();
        $('#editCategoryId').val('');
        $('#categoryModalLabel').text('Create Category');
    });
    
    // Event delegation for pagination clicks
    $('#pagination').on('click', '.page-link', function(e) {
        e.preventDefault();
        const page = $(this).data('page');
        loadCategories(page);
    });
    
    // Event delegation for view button
    $(document).on('click', '.view-btn', function() {
        const categoryId = $(this).data('id');
        viewCategory(categoryId);
    });
    
    // Event delegation for edit button
    $(document).on('click', '.edit-btn', function() {
        const categoryId = $(this).data('id');
        editCategory(categoryId);
    });
    
    // Event handler for edit from view modal button
    $('.edit-from-view-btn').on('click', function() {
        const categoryId = $(this).data('id');
        $('#viewCategoryModal').modal('hide');
        
        // Wait for the first modal to close before opening the second one
        setTimeout(function() {
            editCategory(categoryId);
            $('#categoryModal').modal('show');
        }, 500);
    });
    
    // Event delegation for delete button
    $(document).on('click', '.delete-btn', function() {
        const categoryId = $(this).data('id');
        const categoryName = $(this).data('name');
        
        $('#deleteCategoryName').text(categoryName);
        $('#confirmDeleteBtn').data('id', categoryId);
    });
    
    // Event handler for save category button
    $('#saveCategoryBtn').on('click', function() {
        const categoryName = $('#modalCategoryName').val().trim();
        
        // Check if category name is provided
        if (!categoryName) {
            showToast('Category name is required!', false);
            return;
        }
        
        const categoryId = $('#editCategoryId').val();
        const isEdit = !!categoryId; // Check if this is an edit operation
        
        // Prepare form data to send
        const formData = {
            name: categoryName,  // Name of the category
            description: $('#modalCategoryDescription').val().trim()  // Description of the category
        };
        
        // If this is an edit operation, include the ID
        if (isEdit) {
            formData.id = categoryId;
        }
        console.log('Form data:', formData); 
        saveCategory(isEdit, formData);
    })
    
    // Event handler for confirm delete button
    $('#confirmDeleteBtn').on('click', function() {
        const categoryId = $(this).data('id');
        deleteCategory(categoryId);
        $('#deleteCategoryModal').modal('hide');
    });
    
    // Initial load
    loadCategories();
    
    // Inform parent window about loaded height for iframe resizing
    if (window.parent) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 