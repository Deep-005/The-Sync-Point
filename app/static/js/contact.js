

// ------------------- Popup functionality ---------------------------
function showSuccessPopupContact() {
    const successPopup = document.getElementById('successPopupContact');
    successPopup.classList.add('active');
    document.body.style.overflow = 'hidden'; 
}

function showFailurePopupContact() {
    const failurePopup = document.getElementById('failurePopupContact');
    failurePopup.classList.add('active');
    document.body.style.overflow = 'hidden'; 
}

function hidePopups() {
    const successPopup = document.getElementById('successPopupContact');
    const failurePopup = document.getElementById('failurePopupContact');
    
    successPopup.classList.remove('active');
    failurePopup.classList.remove('active');
    document.body.style.overflow = ''; 
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Close buttons
    const successCloseBtn = document.getElementById('successCloseBtnContact');
    const failureCloseBtn = document.getElementById('failureCloseBtnContact');
    
    if (successCloseBtn) {
        successCloseBtn.addEventListener('click', hidePopups);
    }
    
    if (failureCloseBtn) {
        failureCloseBtn.addEventListener('click', hidePopups);
    }
    
    // Close popup when clicking outside content
    const popupOverlays = document.querySelectorAll('.popup-overlay');
    popupOverlays.forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                hidePopups();
            }
        });
    });
    
    // Close popup with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hidePopups();
        }
    });
});

// Make functions globally available
window.showSuccessPopup = showSuccessPopup;
window.showFailurePopup = showFailurePopup;
window.hidePopups = hidePopups;