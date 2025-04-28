// Layout related JavaScript functions
$(document).ready(function() {
    // Sidebar toggle functionality - this is the only unique function needed here
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