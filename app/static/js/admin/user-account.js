$(document).ready(function() {
    // Initialize the page
    initializePage();
    
    // Function to initialize the page
    function initializePage() {
        console.log("Initializing user account page");
        // Load initial data
        loadUsers();
        // Initialize form validation
        initializeFormValidation();
        // Initialize event handlers
        initializeEventHandlers();
    }
    
    // Function to initialize form validation
    function initializeFormValidation() {
        const accountForm = document.getElementById('accountForm');
        if (accountForm) {
            accountForm.addEventListener('submit', function(event) {
                event.preventDefault();
                event.stopPropagation();
            }, false);
        }
    }
    
    // Function to initialize event handlers
    function initializeEventHandlers() {
        // Create account button click handler
        $('#createAccountBtn').click(function() {
            console.log("Create account button clicked");
            resetForm('create');
        });
        
        // Edit button click handler
        $(document).on('click', '.edit-btn', function() {
            const userId = $(this).data('id');
            console.log("Edit button clicked for user ID:", userId);
            loadUserDetails(userId);
        });
        
        // View button click handler
        $(document).on('click', '.view-btn', function() {
            const userId = $(this).data('id');
            console.log("View button clicked for user ID:", userId);
            loadUserDetailsForView(userId);
        });
        
        // Save account button handler
        $('#saveAccountBtn').click(function() {
            console.log("Save account button clicked");
            saveAccount();
        });
        
        // Search button click handler
        $('#searchBtn').click(function() {
            searchUsers();
        });
        
        // Reset button click handler
        $('#resetBtn').click(function() {
            $('#searchForm')[0].reset();
            loadUsers();
        });
        
        // Edit from view button
        $('#editFromViewBtn').click(function() {
            const userId = $('#viewAccountID').text();
            console.log("Edit from view button clicked for user ID:", userId);
            if (userId && userId !== 'Loading...') {
                $('#viewAccountModal').modal('hide');
                loadUserDetails(userId);
            }
        });
    }
    
    // Reset form function to reuse for create mode
    function resetForm(mode) {
        if (mode === 'create') {
            $('#accountModalLabel').text('Create Account');
            $('#editMode').val('create');
            $('#userId').val('');
            $('#accountForm')[0].reset();
            $('.password-fields').show();
            // Ensure password fields are required in create mode
            $('#modalPassword').prop('required', true);
            $('#modalConfirmPassword').prop('required', true);
            $('#modalUsername').prop('readonly', false);
        }
    }
    
    // Function to load user details for editing
    function loadUserDetails(userId) {
        console.log("Loading user details for edit, ID:", userId);
        
        $.ajax({
            url: API_ENDPOINTS.GET_USERS + '/' + userId,
            type: 'GET',
            dataType: 'json',
            success: function(user) {
                console.log("User data loaded successfully:", user);
                
                // Set form to edit mode
                $('#accountModalLabel').text('Edit Account');
                $('#editMode').val('edit');
                $('#userId').val(user.id);
                
                // Populate form fields
                $('#modalAccountID').val(user.id);
                $('#modalUsername').val(user.username).prop('readonly', true);
                $('#modalUserRole').val(user.role);
                $('#modalStatus').val(user.status);
                
                // Hide password fields and make them not required in edit mode
                $('.password-fields').hide();
                $('#modalPassword').prop('required', false).val(''); // Also clear any potential value
                $('#modalConfirmPassword').prop('required', false).val(''); // Also clear any potential value
                
                // Show the modal
                $('#accountModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error("Error loading user details:", error);
                let errorMsg = getErrorMessage(xhr, error);
                showMessage('Error', 'Failed to load user details: ' + errorMsg, 'danger');
            }
        });
    }
    
    // Function to load user details for viewing
    function loadUserDetailsForView(userId) {
        console.log("Loading user details for view, ID:", userId);
        
        // Show loading state
        $('#viewAccountID').text('Loading...');
        $('#viewUsername').text('Loading...');
        $('#viewRole').text('Loading...');
        $('#viewStatus').text('Loading...');
        
        $.ajax({
            url: API_ENDPOINTS.GET_USERS + '/' + userId,
            type: 'GET',
            dataType: 'json',
            success: function(user) {
                console.log("User data loaded for view:", user);
                
                // Format role name for display
                let roleName = '';
                switch(user.role) {
                    case 'Admin': roleName = 'Administrator'; break;
                    case 'Cleaner': roleName = 'Cleaner'; break;
                    case 'HomeOwner': roleName = 'Home Owner'; break;
                    case 'PlatformManagement': roleName = 'Platform Management'; break;
                    default: roleName = user.role;
                }
                
                // Format status for display
                let statusText = user.status === 1 ? 'Active' : 'Inactive';
                
                // Populate view modal with user data
                $('#viewAccountID').text(user.id);
                $('#viewUsername').text(user.username);
                $('#viewRole').text(roleName);
                $('#viewStatus').text(statusText);
            },
            error: function(xhr, status, error) {
                console.error("Error loading user details for view:", error);
                let errorMsg = getErrorMessage(xhr, error);
                $('#viewUsername').text('Error loading data');
                $('#viewAccountID').text('-');
                $('#viewRole').text('-');
                $('#viewStatus').text('-');
                showMessage('Error', 'Failed to load user details: ' + errorMsg, 'danger');
            }
        });
    }
    
    // Function to load all users
    function loadUsers() {
        console.log("Loading user list");
        
        // Show loading indicator
        $('tbody').html('<tr><td colspan="5" class="text-center">Loading...</td></tr>');
        
        $.ajax({
            url: API_ENDPOINTS.GET_USERS,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                console.log("Users loaded successfully, count:", data.length);
                // Clear loading indicator
                $('tbody').empty();
                
                // Update total count
                $('#total-count').text(data.length);
                
                // Check if any data returned
                if (data.length === 0) {
                    $('tbody').html('<tr><td colspan="5" class="text-center">No users found</td></tr>');
                    return;
                }
                
                // Populate table with user data
                data.forEach(function(user) {
                    let statusBadge = user.status === 1 ? 
                        '<span class="badge rounded-pill bg-success">Active</span>' : 
                        '<span class="badge rounded-pill bg-secondary">Inactive</span>';
                    
                    let roleName = '';
                    switch(user.role) {
                        case 'Admin': roleName = 'Administrator'; break;
                        case 'Cleaner': roleName = 'Cleaner'; break;
                        case 'HomeOwner': roleName = 'Home Owner'; break;
                        case 'PlatformManagement': roleName = 'Platform Management'; break;
                        default: roleName = user.role;
                    }
                    
                    let adminBadge = user.role === 'Admin' ? ' <span class="badge bg-danger">System</span>' : '';
                    
                    let row = `
                        <tr>
                            <td class="text-center">${user.id}</td>
                            <td>${user.username}${adminBadge}</td>
                            <td class="text-center">${roleName}</td>
                            <td class="text-center">${statusBadge}</td>
                            <td class="text-center">
                                <div class="operation-buttons">
                                    <button type="button" class="btn btn-sm btn-outline-secondary view-btn" data-id="${user.id}" data-bs-toggle="modal" data-bs-target="#viewAccountModal">
                                        <i class="bi bi-eye"></i> View
                                    </button>
                                    <button type="button" class="btn btn-sm btn-outline-primary edit-btn" data-id="${user.id}" data-bs-toggle="modal" data-bs-target="#accountModal">
                                        <i class="bi bi-pencil"></i> Edit
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                    $('tbody').append(row);
                });
            },
            error: function(xhr, status, error) {
                console.error("Error loading users:", error);
                let errorMsg = getErrorMessage(xhr, error);
                // Display error message
                $('tbody').html('<tr><td colspan="5" class="text-center text-danger">' +
                    '<i class="bi bi-exclamation-triangle me-2"></i>Error loading users: ' + errorMsg + '</td></tr>');
            }
        });
    }
    
    // Search users function
    function searchUsers() {
        console.log("Searching users with criteria");
        
        // Get search parameters
        const userId = $('#userID').val().trim();
        const username = $('#username').val().trim();
        const role = $('#role').val();
        
        // Build query string
        let queryParams = {};
        if (userId) queryParams.user_id = userId;
        if (username) queryParams.username = username;
        if (role) queryParams.role = role;
        
        console.log("Search parameters:", queryParams);
        
        // Show loading indicator
        $('tbody').html('<tr><td colspan="5" class="text-center">Searching...</td></tr>');
        
        $.ajax({
            url: API_ENDPOINTS.GET_USERS,
            type: 'GET',
            data: queryParams,
            dataType: 'json',
            success: function(data) {
                console.log("Search results:", data.length);
                // Clear loading indicator
                $('tbody').empty();
                
                // Update total count
                $('#total-count').text(data.length);
                
                // Check if any data returned
                if (data.length === 0) {
                    $('tbody').html('<tr><td colspan="5" class="text-center">No users found</td></tr>');
                    return;
                }
                
                // Populate table with user data
                data.forEach(function(user) {
                    let statusBadge = user.status === 1 ? 
                        '<span class="badge rounded-pill bg-success">Active</span>' : 
                        '<span class="badge rounded-pill bg-secondary">Inactive</span>';
                    
                    let roleName = '';
                    switch(user.role) {
                        case 'Admin': roleName = 'Administrator'; break;
                        case 'Cleaner': roleName = 'Cleaner'; break;
                        case 'HomeOwner': roleName = 'Home Owner'; break;
                        case 'PlatformManagement': roleName = 'Platform Management'; break;
                        default: roleName = user.role;
                    }
                    
                    let adminBadge = user.role === 'Admin' ? ' <span class="badge bg-danger">System</span>' : '';
                    
                    let row = `
                        <tr>
                            <td class="text-center">${user.id}</td>
                            <td>${user.username}${adminBadge}</td>
                            <td class="text-center">${roleName}</td>
                            <td class="text-center">${statusBadge}</td>
                            <td class="text-center">
                                <div class="operation-buttons">
                                    <button type="button" class="btn btn-sm btn-outline-secondary view-btn" data-id="${user.id}" data-bs-toggle="modal" data-bs-target="#viewAccountModal">
                                        <i class="bi bi-eye"></i> View
                                    </button>
                                    <button type="button" class="btn btn-sm btn-outline-primary edit-btn" data-id="${user.id}" data-bs-toggle="modal" data-bs-target="#accountModal">
                                        <i class="bi bi-pencil"></i> Edit
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                    $('tbody').append(row);
                });
            },
            error: function(xhr, status, error) {
                console.error("Error searching users:", error);
                let errorMsg = getErrorMessage(xhr, error);
                // Display error message
                $('tbody').html('<tr><td colspan="5" class="text-center text-danger">' +
                    '<i class="bi bi-exclamation-triangle me-2"></i>Error searching users: ' + errorMsg + '</td></tr>');
            }
        });
    }
    
    // Function to save user account (create or update)
    function saveAccount() {
        console.log("Saving account data");
        
        // Form validation
        const form = document.getElementById('accountForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        // Get form data
        const mode = $('#editMode').val();
        const userId = $('#userId').val();
        const username = $('#modalUsername').val().trim();
        const password = $('#modalPassword').val();
        const confirmPassword = $('#modalConfirmPassword').val();
        const role = $('#modalUserRole').val();
        const status = $('#modalStatus').val();
        
        console.log("Form data for " + mode + " mode:", { username, role, status });
        
        // Validation for required fields
        if (!username) {
            showMessage('Error', 'Username is required', 'danger');
            return;
        }
        
        if (!role) {
            showMessage('Error', 'Role is required', 'danger');
            return;
        }
        
        // Password validation for create mode
        if (mode === 'create') {
            if (!password) {
                showMessage('Error', 'Password is required for new accounts', 'danger');
                return;
            }
            
            if (password !== confirmPassword) {
                showMessage('Error', 'Passwords do not match', 'danger');
                return;
            }
        }
        
        // Prepare data for submission
        let userData = {
            username: username,
            role: role,
            status: parseInt(status)
        };
        
        // Include password only for create mode
        if (mode === 'create') {
            userData.password = password;
        }
        
        // Determine API URL and method based on mode
        const isCreate = mode === 'create';
        let apiUrl = isCreate ? API_ENDPOINTS.CREATE_USER : API_ENDPOINTS.UPDATE_USER + userId;
        let method = isCreate ? 'POST' : 'PUT';
        
        console.log("API call:", { url: apiUrl, method: method });
        
        // Show loading state
        $('#saveAccountBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...');
        
        $.ajax({
            url: apiUrl,
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(userData),
            dataType: 'json',
            success: function(response) {
                console.log("Save success:", response);
                
                // Close modal first
                $('#accountModal').modal('hide');
                
                // Then show success message
                showSuccessToast(isCreate ? 'Account created successfully!' : 'Account updated successfully!');
                
                // Reload users to show updated data
                loadUsers();
            },
            error: function(xhr, status, error) {
                console.error("Save error:", { status, error, response: xhr.responseText });
                let errorMsg = getErrorMessage(xhr, error);
                
                if (xhr.responseText && xhr.responseText.includes("success")) {
                    console.log("Despite error status, operation seems successful");
                    
                    $('#accountModal').modal('hide');
                    
                    showSuccessToast(isCreate ? 'Account created successfully!' : 'Account updated successfully!');
                    
                    loadUsers();
                } else {
                    showMessage('Error', 'Operation failed: ' + errorMsg, 'danger');
                }
            },
            complete: function() {
                // Reset button state
                $('#saveAccountBtn').prop('disabled', false).html('Save');
            }
        });
    }
    
    // Helper function to extract error message from response
    function getErrorMessage(xhr, defaultError) {
        try {
            const response = JSON.parse(xhr.responseText);
            if (response && response.message) {
                return response.message;
            }
            if (response && response.error) {
                return response.error;
            }
        } catch (e) {
            // Response is not JSON
        }
        return xhr.statusText || defaultError || 'Unknown error';
    }
    
    // Function to show success toast specifically
    function showSuccessToast(message) {
        console.log("Showing success toast:", message);
        
        // Get the toast element
        const toast = document.getElementById('successToast');
        if (!toast) {
            console.error("Toast element not found");
            return;
        }
        
        // Make sure header is green/success
        const toastHeader = toast.querySelector('.toast-header');
        if (toastHeader) {
            toastHeader.className = 'toast-header bg-success text-white';
        }
        
        // Set message
        const toastBody = toast.querySelector('.toast-body');
        if (toastBody) {
            toastBody.textContent = message;
        }
        
        // Create and show toast
        const bsToast = new bootstrap.Toast(toast, {
            delay: 3000 // Auto-hide after 3 seconds
        });
        bsToast.show();
    }
    
    // Function to show toast message
    function showMessage(title, message, type) {
        console.log("Showing message:", { title, message, type });
        
        const toast = document.getElementById('successToast');
        if (!toast) {
            console.error("Toast element not found");
            return;
        }
        
        const toastHeader = toast.querySelector('.toast-header');
        const toastBody = toast.querySelector('.toast-body');
        
        // Update toast header background color based on message type
        toastHeader.className = `toast-header bg-${type} text-white`;
        
        // Update content
        toastHeader.querySelector('strong').textContent = title;
        toastBody.textContent = message;
        
        // Get Bootstrap Toast instance
        let bsToast = bootstrap.Toast.getInstance(toast);
        if (!bsToast) {
            // Create new toast if it doesn't exist
            bsToast = new bootstrap.Toast(toast, {
                delay: 3000  // Auto-hide after 3 seconds
            });
        }
        
        // Show the toast
        bsToast.show();
    }
    
    // Notify parent page that iframe content is loaded (if in iframe)
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
});