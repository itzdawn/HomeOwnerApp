// ... existing code ...

function showUserForm(mode, userId = null) {
    // Get modal elements
    const modal = document.getElementById('userFormModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('userForm');
    const userIdInput = document.getElementById('userId');
    
    // Set modal title based on mode
    modalTitle.textContent = mode === 'add' ? 'Add User' : 'Edit User';
    
    // Clear the form
    form.reset();
    
    if (mode === 'add') {
        // For add mode, clear user ID
        userIdInput.value = '';
        // Set default status to active
        document.getElementById('formStatus').value = '0';
        
        // Show the password field as required
        const passwordInput = document.getElementById('formPassword');
        passwordInput.setAttribute('required', 'required');
        const passwordHint = passwordInput.nextElementSibling;
        passwordHint.style.display = 'none';
    } else if (mode === 'edit' && userId) {
        // For edit mode, set user ID
        userIdInput.value = userId;
        
        // Make password field optional
        const passwordInput = document.getElementById('formPassword');
        passwordInput.removeAttribute('required');
        const passwordHint = passwordInput.nextElementSibling;
        passwordHint.style.display = 'block';
        
        // In a real application, fetch user data and populate the form
        console.log(`Fetching user data for user ${userId}`);
        
        // For demonstration purposes, use mock data
        const mockUserData = {
            userId: userId,
            userName: userId === '1' ? 'admin' : 'user1',
            nickName: userId === '1' ? 'Administrator' : 'Normal User',
            email: userId === '1' ? 'admin@example.com' : 'user1@example.com',
            phonenumber: userId === '1' ? '15888888888' : '15888888889',
            status: '0', // Active
            roleId: userId === '1' ? '1' : '2' // Administrator or User
        };
        
        // Populate form with user data
        document.getElementById('formUsername').value = mockUserData.userName;
        document.getElementById('formNickname').value = mockUserData.nickName;
        document.getElementById('formEmail').value = mockUserData.email;
        document.getElementById('formPhone').value = mockUserData.phonenumber;
        document.getElementById('formStatus').value = mockUserData.status;
        document.getElementById('formRole').value = mockUserData.roleId;
    }
    
    // Show the modal
    modal.classList.add('show');
    
    // Set up event listeners for the modal
    setupModalEventListeners(modal, form, mode);
}

function setupModalEventListeners(modal, form, mode) {
    // Close button
    const closeButtons = modal.querySelectorAll('.close-modal, .btn-cancel');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            closeModal(modal);
        });
    });
    
    // Save button
    const saveButton = modal.querySelector('.btn-save');
    saveButton.addEventListener('click', function() {
        if (form.checkValidity()) {
            saveUser(form, mode);
        } else {
            // Trigger form validation
            const submitEvent = new Event('submit', {
                bubbles: true,
                cancelable: true
            });
            form.dispatchEvent(submitEvent);
        }
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal(modal);
        }
    });
    
    // Handle form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        saveUser(form, mode);
    });
}

function closeModal(modal) {
    modal.classList.remove('show');
    
    // Remove event listeners to avoid duplicates
    const closeButtons = modal.querySelectorAll('.close-modal, .btn-cancel');
    closeButtons.forEach(button => {
        button.replaceWith(button.cloneNode(true));
    });
    
    const saveButton = modal.querySelector('.btn-save');
    saveButton.replaceWith(saveButton.cloneNode(true));
    
    const form = modal.querySelector('form');
    form.replaceWith(form.cloneNode(true));
}

function saveUser(form, mode) {
    // Get form data
    const userId = document.getElementById('userId').value;
    const username = document.getElementById('formUsername').value;
    const nickname = document.getElementById('formNickname').value;
    const email = document.getElementById('formEmail').value;
    const phone = document.getElementById('formPhone').value;
    const status = document.getElementById('formStatus').value;
    const role = document.getElementById('formRole').value;
    const password = document.getElementById('formPassword').value;
    
    // Prepare user data object
    const userData = {
        userId: userId,
        userName: username,
        nickName: nickname,
        email: email,
        phonenumber: phone,
        status: status,
        roleId: role
    };
    
    // Only include password if provided
    if (password) {
        userData.password = password;
    }
    
    console.log(`Saving user in ${mode} mode:`, userData);
    
    // In a real application, send data to server
    // For demonstration purposes, just show a success message
    const action = mode === 'add' ? 'created' : 'updated';
    showMessage(`User ${username} ${action} successfully`, 'success');
    
    // Close the modal
    const modal = document.getElementById('userFormModal');
    closeModal(modal);
    
    // Refresh the user list
    if (mode === 'add') {
        // In a real application, you would fetch the updated list from the server
        // For demo, just add a new user to the table
        const newUserId = Date.now().toString().substring(6, 10);
        const newUser = {
            userId: newUserId,
            userName: username,
            nickName: nickname,
            phonenumber: phone,
            status: status,
            createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
        };
        
        const userList = [{...newUser}];
        updateUserTable(userList, true);
    } else {
        // Update the user in the existing table
        const tableRow = document.querySelector(`.data-table tbody tr:nth-child(${parseInt(userId)})`);
        if (tableRow) {
            tableRow.querySelector('td:nth-child(3)').textContent = username;
            tableRow.querySelector('td:nth-child(4)').textContent = nickname;
            tableRow.querySelector('td:nth-child(5)').textContent = phone;
            tableRow.querySelector('td:nth-child(6) input').checked = status === '0';
        }
    }
}

function updateUserTable(users, append = false) {
    const tableBody = document.querySelector('.data-table tbody');
    if (!tableBody) return;
    
    if (!append) {
        // Clear existing rows
        tableBody.innerHTML = '';
    }
    
    // Add new rows
    users.forEach(user => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td><input type="checkbox"></td>
            <td>${user.userId}</td>
            <td>${user.userName}</td>
            <td>${user.nickName}</td>
            <td>${user.phonenumber}</td>
            <td>
                <label class="status-toggle">
                    <input type="checkbox" ${user.status === '0' ? 'checked' : ''}>
                    <span class="toggle-slider"></span>
                </label>
            </td>
            <td>${user.createTime}</td>
            <td>
                <button class="op-btn edit"><i class="fas fa-edit"></i> Edit</button>
                <button class="op-btn delete"><i class="fas fa-trash"></i> Delete</button>
                <button class="op-btn more"><i class="fas fa-ellipsis-h"></i> More</button>
            </td>
        `;
        
        if (append) {
            tableBody.appendChild(row);
        } else {
            tableBody.innerHTML += row.outerHTML;
        }
    });
    
    // Re-attach event listeners to the new rows
    setupRowActionButtons();
    setupTableRowSelection();
}

function confirmDeleteUser(userId) {
    // Get the confirmation modal
    const modal = document.getElementById('confirmationModal');
    const message = document.getElementById('confirmationMessage');
    
    // Set the confirmation message
    message.textContent = `Are you sure you want to delete user with ID: ${userId}?`;
    
    // Show the modal
    modal.classList.add('show');
    
    // Set up event listeners
    const closeButtons = modal.querySelectorAll('.close-modal, .btn-cancel');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            closeModal(modal);
        });
    });
    
    // Confirm button
    const confirmButton = document.getElementById('confirmAction');
    confirmButton.addEventListener('click', function() {
        // Close the modal
        closeModal(modal);
        
        // In a real application, this would make an API call to delete the user
        console.log(`Deleting user ${userId}`);
        
        // For demo purposes, just show a success message and remove the row
        showMessage(`User ${userId} deleted successfully`, 'success');
        
        // Remove the row from the table
        const rows = document.querySelectorAll('.data-table tbody tr');
        rows.forEach(row => {
            const rowUserId = row.querySelector('td:nth-child(2)').textContent;
            if (rowUserId === userId) {
                row.remove();
            }
        });
    });
}

// ... existing code ...