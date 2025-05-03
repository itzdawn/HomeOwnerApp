$(document).ready(function() {
    // Set modal title based on mode (create or edit)
    $(document).on('click', '#createAccountBtn', function() {
        $('#accountModalLabel').text('Create Account');
        $('#editMode').val('create');
        $('#accountForm')[0].reset();
        $('.password-fields').show();
    });

    // When Edit button is clicked, populate form with data
    $(document).on('click', '.edit-btn', function() {
        $('#accountModalLabel').text('Edit Account');
        $('#editMode').val('edit');
        
        // Populate form with data from selected row
        const id = $(this).data('id');
        const username = $(this).closest('tr').find('td:eq(1)').text().replace(' System', ''); // Remove "System" badge text if present
        const role = $(this).closest('tr').find('td:eq(2)').text().trim();
        const status = $(this).closest('tr').find('td:eq(3)').text().trim();
        
        $('#modalAccountID').val(id);
        $('#modalUsername').val(username);
        $('#modalUserRole').val(getRoleValue(role));
        $('#modalStatus').val(status.toLowerCase());
        
        // Hide password fields in edit mode
        $('.password-fields').hide();
    });

    // Helper function to get role value for the select dropdown
    function getRoleValue(roleText) {
        switch(roleText) {
            case 'Administrator': return 'admin';
            case 'Cleaner': return 'cleaner';
            case 'Home Owner': return 'homeowner';
            case 'Platform Manager': return 'platform';
            default: return '';
        }
    }

    // When Edit from view button is clicked
    $(document).on('click', '.edit-from-view', function() {
        $('#viewAccountModal').modal('hide');
        const id = $('#viewAccountID').text();
        
        // Find and click the edit button for this account
        $('.edit-btn[data-id="'+id+'"]').click();
    });

    // When View button is clicked, populate modal with data
    $(document).on('click', '.view-btn', function() {
        const id = $(this).data('id');
        const row = $(this).closest('tr');
        const username = row.find('td:eq(1)').text().replace(' System', ''); // Remove "System" badge text if present
        const role = row.find('td:eq(2)').text().trim();
        const status = row.find('td:eq(3)').text().trim();
        
        $('#viewAccountID').text(id);
        $('#viewUsername').text(username);
        $('#viewRole').text(role);
        $('#viewStatus').text(status);
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

    // Handle save account (create or update)
    $('#saveAccountBtn').click(function() {
        // Form validation
        const form = document.getElementById('accountForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        // Get form data
        const mode = $('#editMode').val();
        const id = $('#modalAccountID').val();
        const username = $('#modalUsername').val();
        const password = $('#modalPassword').val();
        const confirmPassword = $('#modalConfirmPassword').val();
        const role = $('#modalUserRole').val();
        const status = $('#modalStatus').val();
        
        // Password validation for create mode
        if (mode === 'create' && password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        // In a real app, this is where we would send data to the backend API
        // For now, just show a success message
        $('#toastMessage').text(mode === 'create' ? 'Account created successfully!' : 'Account updated successfully!');
        const successToast = new bootstrap.Toast(document.getElementById('successToast'));
        successToast.show();
        
        // Close modal
        $('#accountModal').modal('hide');
    });
    
    // Notify parent page that iframe content is loaded
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 