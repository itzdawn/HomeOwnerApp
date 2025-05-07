$(document).ready(function() {
    initializePage();

    function initializePage() {
        console.log("Initializing user account page");
        loadUsers();
        initializeFormValidation();
        initializeEventHandlers();
    }

    function initializeFormValidation() {
        const accountForm = document.getElementById('accountForm');
        if (accountForm) {
            accountForm.addEventListener('submit', function(event) {
                event.preventDefault();
                event.stopPropagation();
            }, false);
        }
    }

    function initializeEventHandlers() {
        $('#createAccountBtn').click(function() {
            resetForm('create');
        });

        $(document).on('click', '.edit-btn', function() {
            const userId = $(this).data('id');
            loadUserDetails(userId);
        });

        $(document).on('click', '.view-btn', function() {
            const userId = $(this).data('id');
            loadUserDetailsForView(userId);
        });

        $('#saveAccountBtn').click(function() {
            saveAccount();
        });

        $('#searchBtn').click(function() {
            searchUsers();
        });

        $('#resetBtn').click(function() {
            $('#searchForm')[0].reset();
            loadUsers();
        });

        $('#editFromViewBtn').click(function() {
            const userId = $('#viewAccountID').text();
            if (userId && userId !== 'Loading...') {
                $('#viewAccountModal').modal('hide');
                loadUserDetails(userId);
            }
        });
    }

    function resetForm(mode) {
        if (mode === 'create') {
            $('#accountModalLabel').text('Create Account');
            $('#editMode').val('create');
            $('#userId').val('');
            $('#accountForm')[0].reset();
            $('.password-fields').show();
            $('#modalPassword').prop('required', true);
            $('#modalConfirmPassword').prop('required', true);
            $('#modalUsername').prop('readonly', false);
        }
    }

    function loadUserDetails(userId) {
        $.ajax({
            url: API_ENDPOINTS.GET_USERS + '/' + userId,
            type: 'GET',
            dataType: 'json',
            success: function(user) {
                $('#accountModalLabel').text('Edit Account');
                $('#editMode').val('edit');
                $('#userId').val(user.id);
                $('#modalAccountID').val(user.id);
                $('#modalUsername').val(user.username).prop('readonly', true);
                $('#modalUserProfile').val(user.profile);
                $('#modalStatus').val(user.status);
                $('.password-fields').hide();
                $('#modalPassword').prop('required', false).val('');
                $('#modalConfirmPassword').prop('required', false).val('');
                $('#accountModal').modal('show');
            },
            error: function(xhr, status, error) {
                showMessage('Error', 'Failed to load user details: ' + getErrorMessage(xhr, error), 'danger');
            }
        });
    }

    function loadUserDetailsForView(userId) {
        $('#viewAccountID').text('Loading...');
        $('#viewUsername').text('Loading...');
        $('#viewProfile').text('Loading...');
        $('#viewStatus').text('Loading...');

        $.ajax({
            url: API_ENDPOINTS.GET_USERS + '/' + userId,
            type: 'GET',
            dataType: 'json',
            success: function(user) {
                let profileLabel = formatProfileName(user.profile);
                let statusText = user.status === 1 ? 'Active' : 'Inactive';

                $('#viewAccountID').text(user.id);
                $('#viewUsername').text(user.username);
                $('#viewProfile').text(profileLabel);
                $('#viewStatus').text(statusText);
            },
            error: function(xhr, status, error) {
                $('#viewUsername').text('Error loading data');
                $('#viewAccountID').text('-');
                $('#viewProfile').text('-');
                $('#viewStatus').text('-');
                showMessage('Error', 'Failed to load user details: ' + getErrorMessage(xhr, error), 'danger');
            }
        });
    }

    function loadUsers() {
        $('tbody').html('<tr><td colspan="5" class="text-center">Loading...</td></tr>');

        $.ajax({
            url: API_ENDPOINTS.GET_USERS,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('tbody').empty();
                $('#total-count').text(data.length);

                if (data.length === 0) {
                    $('tbody').html('<tr><td colspan="5" class="text-center">No users found</td></tr>');
                    return;
                }

                data.forEach(function(user) {
                    let profileLabel = formatProfileName(user.profile);
                    let statusBadge = user.status === 1 ? 
                        '<span class="badge rounded-pill bg-success">Active</span>' : 
                        '<span class="badge rounded-pill bg-secondary">Suspended</span>';
                    let adminBadge = user.profile === 'Admin' ? ' <span class="badge bg-danger">Admin</span>' : '';

                    $('tbody').append(`
                        <tr>
                            <td class="text-center">${user.id}</td>
                            <td>${user.username}${adminBadge}</td>
                            <td class="text-center">${profileLabel}</td>
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
                        </tr>`);
                });
            },
            error: function(xhr, status, error) {
                $('tbody').html('<tr><td colspan="5" class="text-center text-danger">' +
                    '<i class="bi bi-exclamation-triangle me-2"></i>Error loading users: ' + getErrorMessage(xhr, error) + '</td></tr>');
            }
        });
    }

    function searchUsers() {
        const userId = $('#userID').val().trim();
        const username = $('#username').val().trim();
        const profile = $('#profile').val();

        let queryParams = {};
        if (userId) queryParams.userId = userId;
        if (username) queryParams.username = username;
        if (profile) queryParams.profile = profile;

        $('tbody').html('<tr><td colspan="5" class="text-center">Searching...</td></tr>');

        $.ajax({
            url: API_ENDPOINTS.GET_USERS,
            type: 'GET',
            data: queryParams,
            dataType: 'json',
            success: function(data) {
                $('tbody').empty();
                $('#total-count').text(data.length);

                if (data.length === 0) {
                    $('tbody').html('<tr><td colspan="5" class="text-center">No users found</td></tr>');
                    return;
                }

                data.forEach(function(user) {
                    let profileLabel = formatProfileName(user.profile);
                    let statusBadge = user.status === 1 ? 
                        '<span class="badge rounded-pill bg-success">Active</span>' : 
                        '<span class="badge rounded-pill bg-secondary">Inactive</span>';
                    let adminBadge = user.profile === 'Admin' ? ' <span class="badge bg-danger">System</span>' : '';

                    $('tbody').append(`
                        <tr>
                            <td class="text-center">${user.id}</td>
                            <td>${user.username}${adminBadge}</td>
                            <td class="text-center">${profileLabel}</td>
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
                        </tr>`);
                });
            },
            error: function(xhr, status, error) {
                $('tbody').html('<tr><td colspan="5" class="text-center text-danger">' +
                    '<i class="bi bi-exclamation-triangle me-2"></i>Error searching users: ' + getErrorMessage(xhr, error) + '</td></tr>');
            }
        });
    }

    function saveAccount() {
        const form = document.getElementById('accountForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const mode = $('#editMode').val();
        const userId = $('#userId').val();
        const username = $('#modalUsername').val().trim();
        const password = $('#modalPassword').val();
        const confirmPassword = $('#modalConfirmPassword').val();
        const profile = $('#modalUserProfile').val();
        const status = $('#modalStatus').val();

        if (!username) return showMessage('Error', 'Username is required', 'danger');
        if (!profile) return showMessage('Error', 'Profile is required', 'danger');

        if (mode === 'create') {
            if (!password) return showMessage('Error', 'Password is required for new accounts', 'danger');
            if (password !== confirmPassword) return showMessage('Error', 'Passwords do not match', 'danger');
        }

        let userData = {
            username: username,
            profile: profile,
            status: parseInt(status)
        };

        if (mode === 'create') userData.password = password;

        let apiUrl = mode === 'create' ? API_ENDPOINTS.CREATE_USER : API_ENDPOINTS.UPDATE_USER + userId;
        let method = mode === 'create' ? 'POST' : 'PUT';

        $('#saveAccountBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" profile="status" aria-hidden="true"></span> Saving...');

        $.ajax({
            url: apiUrl,
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(userData),
            dataType: 'json',
            success: function(response) {
                $('#accountModal').modal('hide');
                showSuccessToast(mode === 'create' ? 'Account created successfully!' : 'Account updated successfully!');
                loadUsers();
            },
            error: function(xhr, status, error) {
                showMessage('Error', 'Operation failed: ' + getErrorMessage(xhr, error), 'danger');
            },
            complete: function() {
                $('#saveAccountBtn').prop('disabled', false).html('Save');
            }
        });
    }

    function getErrorMessage(xhr, defaultError) {
        try {
            const response = JSON.parse(xhr.responseText);
            if (response?.message) return response.message;
            if (response?.error) return response.error;
        } catch (e) {}
        return xhr.statusText || defaultError || 'Unknown error';
    }

    function showSuccessToast(message) {
        const toast = document.getElementById('successToast');
        if (!toast) return;
        const toastHeader = toast.querySelector('.toast-header');
        if (toastHeader) toastHeader.className = 'toast-header bg-success text-white';
        const toastBody = toast.querySelector('.toast-body');
        if (toastBody) toastBody.textContent = message;
        const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();
    }

    function showMessage(title, message, type) {
        const toast = document.getElementById('successToast');
        if (!toast) return;
        const toastHeader = toast.querySelector('.toast-header');
        const toastBody = toast.querySelector('.toast-body');
        toastHeader.className = `toast-header bg-${type} text-white`;
        toastHeader.querySelector('strong').textContent = title;
        toastBody.textContent = message;
        let bsToast = bootstrap.Toast.getInstance(toast);
        if (!bsToast) bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();
    }

    function formatProfileName(profile) {
        switch (profile) {
            case 'Admin': return 'Administrator';
            case 'Cleaner': return 'Cleaner';
            case 'HomeOwner': return 'Home Owner';
            case 'PlatformManagement': return 'Platform Management';
            default: return profile;
        }
    }

    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'iframeLoaded', height: document.body.scrollHeight }, '*');
    }
});