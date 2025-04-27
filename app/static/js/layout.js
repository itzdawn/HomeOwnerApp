// Layout related JavaScript functions
$(document).ready(function() {
    // Load Sidebar content
    $("#sidebar-content").load("../Layout/SidebarIndex.html");
    
    // Load Navbar content
    $("#navbar-content").load("../Layout/NavbarIndex.html");
    
    // Tab switching logic
    $('#contentTabs button').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
        
        // Update breadcrumb
        const tabText = $(this).text();
        $('#current-section').text(tabText);
    });

    // Handle sidebar menu item clicks
    $(document).on('click', '.sidebar-menu-item', function(e) {
        e.preventDefault();
        
        // Update active class
        $('.sidebar-menu-item').removeClass('active');
        $(this).addClass('active');
        
        const target = $(this).data('target');
        
        // Activate corresponding tab
        if (target === 'user-accounts') {
            $('#user-accounts-tab').tab('show');
            $('#current-section').text('User Accounts');
        } else if (target === 'user-profiles') {
            $('#user-profiles-tab').tab('show');
            $('#current-section').text('User Profiles');
        }
    });
    
    // Sidebar toggle functionality
    $(document).on('click', '#sidebarCollapse', function() {
        $('#sidebar').toggleClass('active');
        
        // Update main content margin
        if ($('#sidebar').hasClass('active')) {
            $('.main-content').css('margin-left', '80px');
        } else {
            $('.main-content').css('margin-left', '240px'); 
        }
    });
}); 