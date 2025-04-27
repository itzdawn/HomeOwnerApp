// 等待DOM完全加载
document.addEventListener('DOMContentLoaded', function() {
    // 导航菜单项点击事件
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // 移除所有激活状态
            navItems.forEach(nav => nav.classList.remove('active'));
            // 添加当前点击项的激活状态
            this.classList.add('active');
        });
    });

    // 头像点击展开用户菜单（可以根据需要添加）
    const avatar = document.querySelector('.avatar');
    if (avatar) {
        avatar.addEventListener('click', function() {
            // 这里可以添加显示用户菜单的逻辑
            console.log('Avatar clicked');
        });
    }

    // 搜索图标点击事件
    const searchIcon = document.querySelector('.search-tools .fa-search');
    if (searchIcon) {
        searchIcon.addEventListener('click', function() {
            // 这里可以添加显示搜索框的逻辑
            console.log('Search icon clicked');
        });
    }

    // 菜单切换按钮点击事件
    const menuToggle = document.querySelector('.menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            const sidebar = document.querySelector('.sidebar');
            const mainContent = document.querySelector('.main-content');
            
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
        });
    }

    // 响应式设计 - 处理侧边栏的折叠/展开
    const toggleSidebar = function() {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
        }
    };

    // 初始检查窗口大小
    toggleSidebar();

    // 当窗口大小改变时重新检查
    window.addEventListener('resize', toggleSidebar);
});