// Blog Preview JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog preview page loaded');
    
    // Smooth scroll for anchor links in content
    document.querySelectorAll('.preview-content a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// ========== DELETE CARD FUNCTIONS ==========

// Function to show delete confirmation card
function showDeleteCard(blogId, blogTitle) {
    const deleteCard = document.getElementById('deleteConfirmCard');
    const deleteForm = document.getElementById('deleteBlogForm');
    const deleteMessage = document.getElementById('deleteBlogTitle');
    
    if (deleteCard && deleteForm && deleteMessage) {
        // Update the form action with the blog ID
        deleteForm.action = `/delete/${blogId}/`;
        
        // Update the message with blog title
        deleteMessage.innerHTML = `Are you sure you want to delete "<strong>${blogTitle}</strong>"?`;
        
        // Show the card
        deleteCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

// Function to hide delete confirmation card
function hideDeleteCard() {
    const deleteCard = document.getElementById('deleteConfirmCard');
    if (deleteCard) {
        deleteCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========== PUBLISH CARD FUNCTIONS ==========

// Function to show publish confirmation card
function showPublishCard(blogId, blogTitle) {
    const publishCard = document.getElementById('publishConfirmCard');
    const publishForm = document.getElementById('publishBlogForm');
    const publishMessage = document.getElementById('publishBlogTitle');
    
    if (publishCard && publishForm && publishMessage) {
        // Update the form action with the blog ID
        publishForm.action = `/publish/${blogId}/`;
        
        // Update the message with blog title
        publishMessage.innerHTML = `Are you ready to publish "<strong>${blogTitle}</strong>" to the world?`;
        
        // Show the card
        publishCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

// Function to hide publish confirmation card
function hidePublishCard() {
    const publishCard = document.getElementById('publishConfirmCard');
    if (publishCard) {
        publishCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========== CARD DISMISSAL HANDLERS ==========

// Close delete card when clicking outside
window.addEventListener('click', function(event) {
    const deleteCard = document.getElementById('deleteConfirmCard');
    if (event.target === deleteCard) {
        hideDeleteCard();
    }
    
    const publishCard = document.getElementById('publishConfirmCard');
    if (event.target === publishCard) {
        hidePublishCard();
    }
});

// Close cards with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        hideDeleteCard();
        hidePublishCard();
    }
});