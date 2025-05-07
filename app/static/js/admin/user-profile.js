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
        $('tbody').html('<tr><td colspan="4" class="text-center">Loading...</td></tr>');
        
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
                    $('tbody').html('<tr><td colspan="4" class="text-center">Server error, retrying in ' + (retryDelay/1000) + ' seconds...</td></tr>');
                    
                    // Retry after delay
                    setTimeout(function() {
                        loadProfiles(retryCount + 1);
                    }, retryDelay);
                } else {
                    // Give up after 3 retries or for other error types
                    $('tbody').html('<tr><td colspan="4" class="text-center text-danger">' + 
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
            $('tbody').html('<tr><td colspan="4" class="text-center">No profiles found</td></tr>');
            return;
        }
        
        // Populate table with profile data
        data.forEach(function(profile) {
            let row = `
                <tr>
                    <td class="text-center">${profile.name || '-'}</td>
                    <td>${profile.description || '-'}</td>
                    <td class="text-center">
                        <span class="badge ${profile.status === 1 ? 'bg-success' : 'bg-grey'}">
                            ${profile.status === 1 ? 'Active' : 'Suspended'}
                        </span>
                    </td>
                    <td class="text-center">
                        <div class="operation-buttons">
                            <button class="btn btn-sm btn-outline-secondary view-btn" data-id="${profile.id}" data-bs-toggle="modal" data-bs-target="#viewProfileModal">
                                <i class="bi bi-eye"></i> View
                            </button>
                            <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${profile.id}" data-bs-toggle="modal" data-bs-target="#profileModal">
                                <i class="bi bi-pencil"></i> Edit
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
    $('#userSearch').on('input', function () {
        const searchTerm = $(this).val().trim();
        const resultsContainer = $('#userSearchResults');
        resultsContainer.empty();
    
        if (searchTerm.length < 1) {
            resultsContainer.removeClass('show');
            return;
        }
    
        let queryParams = [];
        if (!isNaN(searchTerm)) {
            queryParams.push('profile_id=' + encodeURIComponent(searchTerm));
        } else {
            queryParams.push('name=' + encodeURIComponent(searchTerm));
        }
    
        $.ajax({
            url: API_ENDPOINTS.GET_PROFILES + '?' + queryParams.join('&'),
            type: 'GET',
            dataType: 'json',
            success: function (profiles) {
                if (profiles.length) {
                    profiles.forEach(profile => {
                        const item = $('<div class="user-search-item"></div>')
                            .text(`${profile.id} - ${profile.name}`)
                            .data('profile', profile)
                            .on('click', function () {
                                const selected = $(this).data('profile');
                                $('#modalUserId').val(selected.id); // depends on your actual field
                                $('#userSearch').val(`${selected.id} - ${selected.name}`);
                                resultsContainer.removeClass('show');
                            });
                        resultsContainer.append(item);
                    });
                    resultsContainer.addClass('show');
                } else {
                    resultsContainer.html('<div class="user-search-item">No results</div>').addClass('show');
                }
            },
            error: function () {
                resultsContainer.html('<div class="user-search-item text-danger">Error</div>').addClass('show');
            }
        });
    });
    
    // Function to format profile name for display
    function formatProfileName(profile) {
        switch(profile) {
            case 'Admin': return 'Administrator';
            case 'Cleaner': return 'Cleaner';
            case 'HomeOwner': return 'Home Owner';
            case 'PlatformManagement': return 'Platform Management';
            default: return profile;
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
        $('#viewName').text('Loading...');
        $('#viewDescription').text('Loading...');
        $('#viewStatus').text('Loading...');
        
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
                    $('#viewName').text(profile.name || '-');
                    $('#viewDescription').text(profile.description || '-');
                    $('#viewStatus').text(profile.status === 1 ? 'Active' : 'Suspended');
                } else if (mode === 'edit') {
                    // Populate edit form with profile data
                    $('#modalName').val(profile.name || '');
                    $('#modalDescription').val(profile.description || '');
                    $('#modalStatus').val(profile.status || 1);
                }
            },
            error: function(xhr, status, error) {
                alert('Error loading profile details: ' + error);
                console.error("Error loading profile details:", error);
            }
        });
    }

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
        const profileId = $('#searchProfileId').val().trim();
        const name = $('#name').val();
        // Build query string
        let queryParams = [];
        if (profileId) queryParams.push('profile_id=' + encodeURIComponent(profileId));
        if (name) queryParams.push('name=' + encodeURIComponent(name));
        
        // Make API call with search parameters
        $.ajax({
            url: API_ENDPOINTS.GET_PROFILES + (queryParams.length > 0 ? '?' + queryParams.join('&') : ''),
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                displayProfiles(data);
            },
            error: function(xhr, status, error) {
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
        const name = $('#modalName').val();
        const description = $('#modalDescription').val();
        const status = $('#modalStatus').val();
        
        // Prepare data for submission
        let profileData = {
            name: name,
            description: description,
            status: parseInt(status)
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