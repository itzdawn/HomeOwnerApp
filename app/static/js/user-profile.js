$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Sample user data for search functionality (mock data)
    const mockUsers = [
        { id: "UA001", username: "admin_user", role: "Administrator" },
        { id: "UA002", username: "john_doe", role: "Cleaner" },
        { id: "UA003", username: "jane_smith", role: "Home Owner" },
        { id: "UA004", username: "platform_manager", role: "Platform Manager" },
        { id: "UA005", username: "cleaner1", role: "Cleaner" },
        { id: "UA006", username: "homeowner1", role: "Home Owner" },
        { id: "UA007", username: "cleaner2", role: "Cleaner" },
        { id: "UA008", username: "homeowner2", role: "Home Owner" },
        { id: "UA009", username: "support_staff", role: "Support Staff" },
        { id: "UA010", username: "manager1", role: "Platform Manager" }
    ];

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
        
        // Filter users based on search term
        const filteredUsers = mockUsers.filter(user => {
            return user.username.toLowerCase().includes(searchTerm) || 
                   user.id.toLowerCase().includes(searchTerm);
        }).slice(0, 10); // Limit to 10 results
        
        // Display results
        if (filteredUsers.length > 0) {
            filteredUsers.forEach(user => {
                const resultItem = $('<div class="user-search-item"></div>')
                    .text(`${user.id} - ${user.username} (${user.role})`)
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
    });
    
    // Hide search results when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.user-search-container').length) {
            $('#userSearchResults').removeClass('show');
        }
    });

    // View button click
    $('.view-btn').click(function() {
        const id = $(this).data('id');
        $('#viewProfileID').text(id);
        
        // In a real application, you would load the profile data here
        // For now, we'll just show some sample data
        if (id === 'UA001') {
            $('#viewFullName').text('Admin User');
            $('#viewEmail').text('admin@example.com');
            $('#viewPhone').text('+1 (123) 456-7890');
            $('#viewAddress').text('1000 Admin Blvd, Admin City, AC 10000');
        } else if (id === 'UA002') {
            $('#viewFullName').text('John Doe');
            $('#viewEmail').text('john.doe@example.com');
            $('#viewPhone').text('+1 (555) 234-5678');
            $('#viewAddress').text('123 Main St, Anytown, AT 12345');
        } else if (id === 'UA003') {
            $('#viewFullName').text('Jane Smith');
            $('#viewEmail').text('jane.smith@example.com');
            $('#viewPhone').text('+1 (555) 345-6789');
            $('#viewAddress').text('456 Oak Ave, Somewhere, SW 67890');
        }
    });

    // Edit button click
    $('.edit-btn').click(function() {
        const id = $(this).data('id');
        $('#profileId').val(id);
        $('#modalUserId').val(id);
        $('#profileModalLabel').text('Edit Profile');
        
        // Hide user search section in edit mode
        $('#userSearchSection').hide();
        
        // In a real application, you would load the profile data for editing here
        if (id === 'UA002') {
            $('#modalFullName').val('John Doe');
            $('#modalEmail').val('john.doe@example.com');
            $('#modalPhone').val('+1 (555) 234-5678');
            $('#modalAddress').val('123 Main St, Anytown, AT 12345');
        } else if (id === 'UA003') {
            $('#modalFullName').val('Jane Smith');
            $('#modalEmail').val('jane.smith@example.com');
            $('#modalPhone').val('+1 (555) 345-6789');
            $('#modalAddress').val('456 Oak Ave, Somewhere, SW 67890');
        }
    });

    // Delete button click
    $('.delete-btn').click(function() {
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
        // In a real application, this would submit the search form
        // For now, just show a message
        alert('Search functionality would be implemented here');
    });

    // Reset button click
    $('#resetBtn').click(function() {
        $('#searchForm')[0].reset();
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
        if (!phoneRegex.test(phoneNumber)) {
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
        
        // In a real application, you would save the profile data here
        // For now, show a success message
        $('#toastMessage').text('Profile saved successfully!');
        const successToast = new bootstrap.Toast(document.getElementById('successToast'));
        successToast.show();
        
        // Close modal
        $('#profileModal').modal('hide');
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
        
        // In a real application, you would delete the profile here
        // For now, show a success message
        $('#toastMessage').text('Profile ' + id + ' deleted successfully!');
        const successToast = new bootstrap.Toast(document.getElementById('successToast'));
        successToast.show();
        
        // Close modal
        $('#deleteProfileModal').modal('hide');
    });
    
    // Notify parent page that iframe content is loaded
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 