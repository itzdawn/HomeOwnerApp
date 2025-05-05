$(document).ready(function() {
    // Load profiles data on page load
    loadProfiles();
    
    // Function to initialize tooltips
    function initializeTooltips() {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        });
    }
    
    // Initialize tooltips
    initializeTooltips();

    // Function to load profiles data from API
    function loadProfiles(retryCount = 0) {
        // Show loading indicator
        $('tbody').html('<tr><td colspan="6" class="text-center">Loading...</td></tr>');
        
        // Make API call to get profiles
        $.ajax({
            url: API_ENDPOINTS.GET_PROFILES,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                console.log("Profiles data received:", data);
                displayProfiles(data);
            },
            error: function(xhr, status, error) {
                let errorDetails = '';
                try {
                    const response = JSON.parse(xhr.responseText);
                    errorDetails = response.message || error;
                } catch (e) {
                    errorDetails = error || 'Unknown error occurred';
                }
                
                console.error("Error loading profiles:", error);
                console.error("Status:", status);
                console.error("Response:", xhr.responseText);
                console.error("API Endpoint used:", API_ENDPOINTS.GET_PROFILES);
                
                // Add retry logic for server errors (status code 500) or if server is restarting
                if ((xhr.status === 500 || xhr.status === 0) && retryCount < 3) {
                    const retryDelay = 2000; // 2 seconds
                    $('tbody').html('<tr><td colspan="6" class="text-center">Server error, retrying in ' + (retryDelay/1000) + ' seconds...</td></tr>');
                    
                    // Retry after delay
                    setTimeout(function() {
                        loadProfiles(retryCount + 1);
                    }, retryDelay);
                } else {
                    // Give up after 3 retries or for other error types
                    $('tbody').html('<tr><td colspan="6" class="text-center text-danger">' + 
                        '<i class="bi bi-exclamation-triangle me-2"></i>Error loading profiles: ' + errorDetails + '<br>' +
                        '<small>Check server logs for more details: User.getUserById method is missing</small>' +
                        (retryCount > 0 ? '<br><button class="btn btn-sm btn-outline-primary mt-2 retry-btn">Try Again</button>' : '') +
                        '</td></tr>');
                        
                    // Add click handler for retry button
                    $('.retry-btn').click(function() {
                        loadProfiles(0); // Reset retry count
                    });
                }
            }
        });
    }
    
    // Function to display profiles in the table
    function displayProfiles(data) {
        // Clear loading indicator
        $('tbody').empty();
        
        // Update total count
        $('#total-count').text(data.length);
        
        // Check if any data returned
        if (data.length === 0) {
            $('tbody').html('<tr><td colspan="5" class="text-center">No profiles found</td></tr>');
            return;
        }
        
        // Populate table with profile data
        data.forEach(function(profile) {
            let row = `
                <tr>
                    <td class="text-center">${profile.user_id || '-'}</td>
                    <td>${profile.full_name || '-'}</td>
                    <td>${profile.phone || '-'}</td>
                    <td>${profile.address || '-'}</td>
                    <td class="text-center">
                        <div class="operation-buttons">
                            <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${profile.id}" data-bs-toggle="modal" data-bs-target="#viewProfileModal">
                                <i class="bi bi-eye"></i> View
                            </button>
                            <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${profile.id}" data-bs-toggle="modal" data-bs-target="#profileModal">
                                <i class="bi bi-pencil"></i> Edit
                            </button>
                            <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${profile.id}" data-bs-toggle="modal" data-bs-target="#deleteProfileModal">
                                <i class="bi bi-trash"></i> Delete
                            </button>
                        </div>
                    </td>
                </tr>
            `;
            $('tbody').append(row);
        });
        
        // Initialize tooltips
        initializeTooltips();
    }
    
    // User search functionality
    $('#userSearch').on('input', function() {
        const searchTerm = $(this).val().trim().toLowerCase();
        const resultsContainer = $('#userSearchResults');
        
        // Clear previous results
        resultsContainer.empty();
        
        // Hide results if search term is less than 2 characters
        if (searchTerm.length < 2) {
            resultsContainer.removeClass('show');
            return;
        }
        
        // Make API call to search users
        $.ajax({
            url: API_ENDPOINTS.GET_USERS + '?username=' + encodeURIComponent(searchTerm),
            type: 'GET',
            dataType: 'json',
            success: function(users) {
                // Display results
                if (users.length > 0) {
                    users.forEach(user => {
                        const resultItem = $('<div class="user-search-item"></div>')
                            .text(`${user.id} - ${user.username} (${formatRoleName(user.role)})`)
                            .data('user', user)
                            .on('click', function() {
                                // Set user ID when an item is selected
                                const selectedUser = $(this).data('user');
                                $('#modalUserId').val(selectedUser.id);
                                $('#userSearch').val(`${selectedUser.id} - ${selectedUser.username}`);
                                resultsContainer.removeClass('show');
                            });
                        resultsContainer.append(resultItem);
                    });
                    resultsContainer.addClass('show');
                } else {
                    resultsContainer.append('<div class="user-search-item">No users found</div>');
                    resultsContainer.addClass('show');
                }
            },
            error: function(xhr, status, error) {
                resultsContainer.append('<div class="user-search-item text-danger">Error searching users</div>');
                resultsContainer.addClass('show');
                console.error("Error searching users:", error);
            }
        });
    });
    
    // Function to format role name for display
    function formatRoleName(role) {
        switch(role) {
            case 'Admin': return 'Administrator';
            case 'Cleaner': return 'Cleaner';
            case 'HomeOwner': return 'Home Owner';
            case 'PlatformManagement': return 'Platform Management';
            default: return role;
        }
    }
    
    // Hide search results when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.user-search-container').length) {
            $('#userSearchResults').removeClass('show');
        }
    });

    // View button click
    $(document).on('click', '.view-btn', function() {
        const id = $(this).data('id');
        
        // Show loading state
        $('#viewProfileID').text('Loading...');
        $('#viewFullName').text('Loading...');
        $('#viewEmail').text('Loading...');
        $('#viewPhone').text('Loading...');
        $('#viewAddress').text('Loading...');
        
        // Load profile data from API
        loadProfileDetails(id, 'view');
    });

    // Edit button click
    $(document).on('click', '.edit-btn', function() {
        const id = $(this).data('id');
        
        // Show loading state
        $('#profileId').val(id);
        $('#profileModalLabel').text('Edit Profile');
        
        // Hide user search section in edit mode
        $('#userSearchSection').hide();
        
        // Load profile data for editing
        loadProfileDetails(id, 'edit');
    });
    
    // Function to load profile details
    function loadProfileDetails(id, mode) {
        $.ajax({
            url: API_ENDPOINTS.GET_PROFILES + '/' + id,
            type: 'GET',
            dataType: 'json',
            success: function(profile) {
                if (mode === 'view') {
                    // Populate view modal with profile data
                    $('#viewProfileID').text(profile.id);
                    $('#viewFullName').text(profile.full_name || '-');
                    $('#viewPhone').text(profile.phone || '-');
                    $('#viewAddress').text(profile.address || '-');
                    $('#viewUserId').text(profile.user_id || '-');
                } else if (mode === 'edit') {
                    // Populate edit form with profile data
                    $('#modalFullName').val(profile.full_name || '');
                    $('#modalPhone').val(profile.phone || '');
                    $('#modalAddress').val(profile.address || '');
                    $('#modalUserId').val(profile.user_id || '');
                    
                    // If there's a user associated, also show their username
                    if (profile.user_id) {
                        $.ajax({
                            url: API_ENDPOINTS.GET_USERS + '/' + profile.user_id,
                            type: 'GET',
                            dataType: 'json',
                            success: function(user) {
                                $('#userSearch').val(`${user.id} - ${user.username}`);
                            },
                            error: function(xhr, status, error) {
                                console.error("Error loading user details:", error);
                            }
                        });
                    }
                }
            },
            error: function(xhr, status, error) {
                alert('Error loading profile details: ' + error);
                console.error("Error loading profile details:", error);
            }
        });
    }

    // Delete button click
    $(document).on('click', '.delete-btn', function() {
        const id = $(this).data('id');
        $('#deleteProfileID').text(id);
    });

    // Create new profile button click
    $('#createProfileBtn').click(function() {
        $('#profileForm').trigger('reset');
        $('#profileId').val('');
        $('#modalUserId').val('');
        $('#profileModalLabel').text('New Profile');
        
        // Show user search section in create mode
        $('#userSearchSection').show();
    });

    // Search button click
    $('#searchBtn').click(function() {
        // Get search parameters
        const profileId = $('#profileID').val();
        const fullName = $('#fullName').val();
        const userId = $('#userId').val();
        
        // Build query string
        let queryParams = [];
        if (profileId) queryParams.push('profile_id=' + encodeURIComponent(profileId));
        if (fullName) queryParams.push('full_name=' + encodeURIComponent(fullName));
        if (userId) queryParams.push('user_id=' + encodeURIComponent(userId));
        
        // Make API call with search parameters
        $.ajax({
            url: API_ENDPOINTS.GET_PROFILES + (queryParams.length > 0 ? '?' + queryParams.join('&') : ''),
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                displayProfiles(data);
            },
            error: function(xhr, status, error) {
                // Display error message
                $('tbody').html('<tr><td colspan="5" class="text-center text-danger">Error searching profiles: ' + error + '</td></tr>');
                console.error("Error searching profiles:", error);
            }
        });
    });

    // Reset button click
    $('#resetBtn').click(function() {
        $('#searchForm')[0].reset();
        loadProfiles(); // Reload all profiles
    });

    // Form validation function
    function validateProfileForm() {
        const form = document.getElementById('profileForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return false;
        }
        
        // Additional validation for phone number format
        const phoneRegex = /^\+?[0-9\s\(\)\-]{10,20}$/;
        const phoneNumber = $('#modalPhone').val();
        if (phoneNumber && !phoneRegex.test(phoneNumber)) {
            alert('Please enter a valid phone number');
            $('#modalPhone').focus();
            return false;
        }
        
        return true;
    }

    // Save profile button click
    $('#saveProfileBtn').click(function() {
        // Validate the form
        if (!validateProfileForm()) {
            return;
        }
        
        // Get form data
        const profileId = $('#profileId').val();
        const fullName = $('#modalFullName').val();
        const phone = $('#modalPhone').val();
        const address = $('#modalAddress').val();
        const userId = $('#modalUserId').val();
        
        // Prepare data for submission
        let profileData = {
            full_name: fullName,
            phone: phone,
            address: address,
            user_id: userId
        };
        
        // Determine if this is create or update
        const isCreate = !profileId;
        const apiUrl = isCreate ? API_ENDPOINTS.CREATE_PROFILE : API_ENDPOINTS.UPDATE_PROFILE + profileId;
        const method = isCreate ? 'POST' : 'PUT';
        
        // Make API call
        $.ajax({
            url: apiUrl,
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(profileData),
            dataType: 'json',
            success: function(response) {
                // Show success message
                showSuccessToast(isCreate ? 'Profile created successfully!' : 'Profile updated successfully!');
                
                // Close modal
                $('#profileModal').modal('hide');
                
                // Reload profiles data
                loadProfiles();
            },
            error: function(xhr, status, error) {
                let errorMsg = '';
                try {
                    // Try to parse error response
                    const response = JSON.parse(xhr.responseText);
                    errorMsg = response.message || 'Error occurred';
                } catch (e) {
                    errorMsg = error;
                }
                alert('Operation failed: ' + errorMsg);
                console.error("API error:", errorMsg);
            }
        });
    });

    // Edit from view button click
    $('.edit-from-view').click(function() {
        $('#viewProfileModal').modal('hide');
        const id = $('#viewProfileID').text();
        
        // Trigger edit modal with the same ID
        $('.edit-btn[data-id="' + id + '"]').click();
    });

    // Confirm delete button click
    $('#confirmDeleteBtn').click(function() {
        const id = $('#deleteProfileID').text();
        
        // Make API call to delete profile
        $.ajax({
            url: API_ENDPOINTS.DELETE_PROFILE + id,
            type: 'DELETE',
            success: function(response) {
                // Show success message
                showSuccessToast('Profile deleted successfully!');
                
                // Close modal
                $('#deleteProfileModal').modal('hide');
                
                // Reload profiles data
                loadProfiles();
            },
            error: function(xhr, status, error) {
                let errorMsg = '';
                try {
                    // Try to parse error response
                    const response = JSON.parse(xhr.responseText);
                    errorMsg = response.message || 'Error occurred';
                } catch (e) {
                    errorMsg = error;
                }
                alert('Delete operation failed: ' + errorMsg);
                console.error("API error:", errorMsg);
            }
        });
    });
    
    // Function to show success toast
    function showSuccessToast(message) {
        $('#toastMessage').text(message);
        const successToast = new bootstrap.Toast(document.getElementById('successToast'));
        successToast.show();
    }
    
    // Notify parent page that iframe content is loaded
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 