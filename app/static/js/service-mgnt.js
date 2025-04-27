$(document).ready(function() {
    // Set modal title based on mode (create or edit)
    $(document).on('click', '#createServiceBtn', function() {
        $('#serviceModalLabel').text('Create Service');
        $('#editMode').val('create');
        $('#serviceForm')[0].reset();
        $('#modalServiceID').val('');
    });

    // When Edit button is clicked, populate form with data
    $(document).on('click', '.edit-btn', function() {
        $('#serviceModalLabel').text('Edit Service');
        $('#editMode').val('edit');
        
        // Populate form with data from selected row
        const id = $(this).data('id');
        const row = $(this).closest('tr');
        const name = row.find('td:eq(1)').text();
        const description = row.find('td:eq(2)').text();
        const price = row.find('td:eq(3)').text().replace('$', '');
        
        $('#modalServiceID').val(id);
        $('#modalServiceName').val(name);
        
        // In a real app, we would fetch the complete service data
        // For now, we'll set some mock data
        if (id === 'S001') {
            $('#modalCategory').val('regular');
            $('#modalDescription').val('Standard cleaning service for homes including dusting, vacuuming, and bathroom cleaning.');
            $('#modalPrice').val('80.00');
            $('#modalDuration').val('2');
            $('#modalAvailability').val('available');
        } else if (id === 'S002') {
            $('#modalCategory').val('deep');
            $('#modalDescription').val('Thorough cleaning of all areas including behind appliances, inside cabinets, and detailed bathroom cleaning.');
            $('#modalPrice').val('120.00');
            $('#modalDuration').val('4');
            $('#modalAvailability').val('available');
        } else if (id === 'S003') {
            $('#modalCategory').val('commercial');
            $('#modalDescription').val('Professional cleaning service for office spaces. Includes cleaning of workstations, meeting rooms, and common areas.');
            $('#modalPrice').val('95.00');
            $('#modalDuration').val('3');
            $('#modalAvailability').val('available');
        }
    });

    // When View button is clicked, populate modal with data
    $(document).on('click', '.view-btn', function() {
        const id = $(this).data('id');
        const row = $(this).closest('tr');
        const name = row.find('td:eq(1)').text();
        const description = row.find('td:eq(2)').text();
        const price = row.find('td:eq(3)').text().replace('$', '');
        const views = row.find('.metric-badge:first-child').text().trim().match(/\d+/)[0];
        const shortlists = row.find('.metric-badge:last-child').text().trim().match(/\d+/)[0];
        
        $('#viewServiceID').text(id);
        $('#viewServiceName').text(name);
        $('#viewDescription').text(description);
        $('#viewPrice').text(price);
        $('#viewViews').text(views);
        $('#viewShortlists').text(shortlists);
        
        // In a real app, we would fetch the complete service data
        // For now, we'll set some mock data
        if (id === 'S001') {
            $('#viewCategory').text('Regular Cleaning');
            $('#viewDuration').text('2');
            $('#viewAvailability').text('Available');
        } else if (id === 'S002') {
            $('#viewCategory').text('Deep Cleaning');
            $('#viewDuration').text('4');
            $('#viewAvailability').text('Available');
        } else if (id === 'S003') {
            $('#viewCategory').text('Commercial Cleaning');
            $('#viewDuration').text('3');
            $('#viewAvailability').text('Available');
        }
    });

    // Delete button click
    $('.delete-btn').click(function() {
        const id = $(this).data('id');
        const name = $(this).closest('tr').find('td:eq(1)').text();
        $('#deleteServiceName').text(name);
        $('#deleteServiceModal').data('id', id);
    });

    // When "Edit from view" button is clicked
    $(document).on('click', '.edit-from-view', function() {
        $('#viewServiceModal').modal('hide');
        const id = $('#viewServiceID').text();
        $('.edit-btn[data-id="'+id+'"]').click();
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

    // Handle save service
    $('#saveServiceBtn').click(function() {
        // Form validation
        const form = document.getElementById('serviceForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        // Get form data
        const mode = $('#editMode').val();
        const id = $('#modalServiceID').val();
        const name = $('#modalServiceName').val();
        const category = $('#modalCategory').val();
        const description = $('#modalDescription').val();
        const price = $('#modalPrice').val();
        const duration = $('#modalDuration').val();
        const availability = $('#modalAvailability').val();
        
        // In a real app, this is where we would send data to the backend API
        // For now, just show a success message
        $('#toastMessage').text(mode === 'create' ? 'Service created successfully!' : 'Service updated successfully!');
        const successToast = new bootstrap.Toast(document.getElementById('successToast'));
        successToast.show();
        
        // Close modal
        $('#serviceModal').modal('hide');
    });

    // Confirm delete service
    $('#confirmDeleteBtn').click(function() {
        const id = $('#deleteServiceModal').data('id');
        
        // In a real app, this is where we would send the delete request to the backend API
        // For now, just show a success message
        $('#toastMessage').text('Service deleted successfully!');
        const successToast = new bootstrap.Toast(document.getElementById('successToast'));
        successToast.show();
        
        // Close modal
        $('#deleteServiceModal').modal('hide');
    });
    
    // Notify parent page that iframe content is loaded
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
}); 