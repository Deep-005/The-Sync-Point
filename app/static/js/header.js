// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMobileMenuBtn = document.getElementById('closeMobileMenu');
    const mobileMenuContainer = document.getElementById('mobileMenuContainer');
    const body = document.body;
    
    // Open mobile menu
    if (mobileMenuBtn && mobileMenuContainer) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenuContainer.classList.add('active');
            body.style.overflow = 'hidden'; // Prevent scrolling
            
            // Change icon
            const icon = mobileMenuBtn.querySelector('i');
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        });
    }
    
    // Close mobile menu
    if (closeMobileMenuBtn && mobileMenuContainer) {
        closeMobileMenuBtn.addEventListener('click', function() {
            mobileMenuContainer.classList.remove('active');
            body.style.overflow = ''; // Restore scrolling
            
            // Change icon back
            const icon = mobileMenuBtn.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        });
    }
    
    // Close menu when clicking outside
    if (mobileMenuContainer) {
        mobileMenuContainer.addEventListener('click', function(e) {
            if (e.target === mobileMenuContainer) {
                mobileMenuContainer.classList.remove('active');
                body.style.overflow = '';
                
                // Change icon back
                const icon = mobileMenuBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
    
    // Close menu on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenuContainer.classList.contains('active')) {
            mobileMenuContainer.classList.remove('active');
            body.style.overflow = '';
            
            // Change icon back
            const icon = mobileMenuBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
    
    // Search form submission enhancement
    const searchForms = document.querySelectorAll('.search-box, .mobile-search-box');
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[type="search"]');
            if (searchInput && searchInput.value.trim() === '') {
                e.preventDefault();
                searchInput.focus();
                // Add shake animation for empty search
                searchInput.style.animation = 'shake 0.5s';
                setTimeout(() => {
                    searchInput.style.animation = '';
                }, 500);
            }
        });
    });
    
    // Category button click handlers
    const categoryButtons = document.querySelectorAll('.category-btn, .mobile-category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            console.log('Category selected:', category);
            // Add your category filtering logic here
        });
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        // Close mobile menu when resizing to larger screens
        if (window.innerWidth > 768 && mobileMenuContainer) {
            if (mobileMenuContainer.classList.contains('active')) {
                mobileMenuContainer.classList.remove('active');
                body.style.overflow = '';
                
                // Change icon back
                const icon = mobileMenuBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        }
    });
});