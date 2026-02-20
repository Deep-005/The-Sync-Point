document.addEventListener('DOMContentLoaded', function() {
    const statusButtons = document.querySelectorAll('.status-btn');
    const blogCards = document.querySelectorAll('.blog-card');
    const blogsCount = document.querySelector('.blogs-count');
    
    // Function to filter blogs by status
    function filterBlogs(status) {
        let visibleCount = 0;
        
        blogCards.forEach(card => {
            if (status === 'all' || card.dataset.status === status) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Update blogs count display
        if (blogsCount) {
            blogsCount.textContent = `${visibleCount} post${visibleCount !== 1 ? 's' : ''}`;
        }
        
        // Show/hide no blogs message
        const noBlogsElement = document.querySelector('.no-blogs');
        if (visibleCount === 0 && noBlogsElement) {
            noBlogsElement.style.display = 'block';
        } else if (noBlogsElement) {
            noBlogsElement.style.display = 'none';
        }
        
        // Update active button
        statusButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.status === status) {
                btn.classList.add('active');
            }
        });
    }
    
    // Add click event listeners to status buttons
    statusButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterBlogs(this.dataset.status);
        });
    });
});

// ========== DELETE CARD FUNCTIONS ==========
function showDeleteCard(blogId, blogTitle) {
    const deleteCard = document.getElementById('deleteConfirmCard');
    const deleteForm = document.getElementById('deleteBlogForm');
    const deleteMessage = document.getElementById('deleteBlogTitle');
    
    if (deleteCard && deleteForm && deleteMessage) {
        deleteForm.action = `/delete/${blogId}/`;
        deleteMessage.innerHTML = `Are you sure you want to delete "<strong>${blogTitle}</strong>"?`;
        deleteCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hideDeleteCard() {
    const deleteCard = document.getElementById('deleteConfirmCard');
    if (deleteCard) {
        deleteCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========== PUBLISH CARD FUNCTIONS ==========
function showPublishCard(blogId, blogTitle) {
    const publishCard = document.getElementById('publishConfirmCard');
    const publishForm = document.getElementById('publishBlogForm');
    const publishMessage = document.getElementById('publishBlogTitle');
    
    if (publishCard && publishForm && publishMessage) {
        publishForm.action = `/publish/${blogId}/`;
        publishMessage.innerHTML = `Are you ready to publish "<strong>${blogTitle}</strong>" to the world?`;
        publishCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hidePublishCard() {
    const publishCard = document.getElementById('publishConfirmCard');
    if (publishCard) {
        publishCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========== ARCHIVE CARD FUNCTIONS ==========
function showArchiveCard(blogId, blogTitle) {
    const archiveCard = document.getElementById('archiveConfirmCard');
    const archiveForm = document.getElementById('archiveBlogForm');
    const archiveMessage = document.getElementById('archiveBlogTitle');
    
    if (archiveCard && archiveForm && archiveMessage) {
        archiveForm.action = `/archive/${blogId}/`;
        archiveMessage.innerHTML = `Are you sure you want to archive "<strong>${blogTitle}</strong>"?`;
        archiveCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hideArchiveCard() {
    const archiveCard = document.getElementById('archiveConfirmCard');
    if (archiveCard) {
        archiveCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========== GLOBAL CARD DISMISSAL HANDLERS ==========
window.addEventListener('click', function(event) {
    const deleteCard = document.getElementById('deleteConfirmCard');
    if (event.target === deleteCard) hideDeleteCard();
    
    const publishCard = document.getElementById('publishConfirmCard');
    if (event.target === publishCard) hidePublishCard();
    
    const archiveCard = document.getElementById('archiveConfirmCard');
    if (event.target === archiveCard) hideArchiveCard();
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        hideDeleteCard();
        hidePublishCard();
        hideArchiveCard();
    }
});

// ========== ACCOUNT DELETION ==========
function confirmDeleteAccount() {
    if (confirm("Are you absolutely sure you want to delete your account? All your blogs and data will be permanently deleted. This action cannot be undone.")) {
        window.location.href = "#"; // Replace with actual delete account URL
    }
}