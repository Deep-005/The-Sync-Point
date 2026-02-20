// Character counter for title
const titleInput = document.getElementById("title");
const titleCounter = document.getElementById("title-counter");

if (titleInput && titleCounter) {
    titleInput.addEventListener("input", function () {
        titleCounter.textContent = this.value.length;
    });
}

// Character counter for content
function updateCharCount() {
    const content = document.getElementById("content");
    const charCount = document.getElementById("char-count");
    const counter = document.getElementById("content-counter");

    if (content && charCount && counter) {
        const length = content.value.length;
        charCount.textContent = length;

        if (length > 5000) {
            content.value = content.value.substring(0, 5000);
            charCount.textContent = 5000;
            counter.classList.add("limit");
        } else if (length > 4500) {
            counter.classList.add("limit");
        } else {
            counter.classList.remove("limit");
        }
    }
}

// Image preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const previewSection = document.getElementById("image-preview");
        const previewImg = document.getElementById("preview-img");

        reader.onload = function (e) {
            if (previewImg && previewSection) {
                previewImg.src = e.target.result;
                previewSection.style.display = "block";
            }
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function changeImage() {
    document.getElementById("image").click();
    document.getElementById("image-preview").style.display = "none";
}

function removeImage() {
    document.getElementById("image").value = "";
    document.getElementById("image-preview").style.display = "none";
}

// Show image size alert card
function showImageSizeAlert(fileSize) {
    const alertCard = document.getElementById('imageSizeAlert');
    if (alertCard) {
        const messageElement = alertCard.querySelector('.alert-message');
        if (messageElement) {
            messageElement.innerHTML = `The image you uploaded (<strong>${fileSize}MB</strong>) exceeds the <strong>5MB size limit</strong>. Please optimize your image or choose a smaller file.`;
        }
        alertCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

// Hide image size alert card
function hideImageAlert() {
    const alertCard = document.getElementById('imageSizeAlert');
    if (alertCard) {
        alertCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close alert when clicking outside
window.onclick = function(event) {
    const alertCard = document.getElementById('imageSizeAlert');
    if (event.target === alertCard) {
        hideImageAlert();
    }
}

// Validate image before form submission
function validateImageBeforeSubmit(event) {
    const fileInput = document.getElementById("image");
    const action = event.submitter ? event.submitter.value : null;
    
    // validate image size before submitting for publish or publish-draft actions
    if (action === 'publish' || action === 'publish-draft') {
        if (fileInput && fileInput.files && fileInput.files[0]) {
            const fileSize = fileInput.files[0].size / 1024 / 1024; // MB
            
            if (fileSize > 5) {
                event.preventDefault();
                showImageSizeAlert(fileSize.toFixed(2));
                return false;
            }
        } else if (fileInput && !fileInput.files[0]) {
            event.preventDefault();
            alert('Please select a featured image for your blog.');
            return false;
        }
    }
    
    return true;
}

// Simple text formatting functions
function formatText(format) {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);

    let formattedText = "";
    if (format === "bold") {
        formattedText = `**${selectedText}**`;
    } else if (format === "italic") {
        formattedText = `*${selectedText}*`;
    }

    textarea.value = textarea.value.substring(0, start) + formattedText + textarea.value.substring(end);
    textarea.focus();
}

function insertHeading() {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    textarea.value = textarea.value.substring(0, start) + "\n## Heading\n" + textarea.value.substring(start);
    textarea.focus();
}

function insertLink() {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    textarea.value = textarea.value.substring(0, start) + "[Link Text](https://example.com)" + textarea.value.substring(start);
    textarea.focus();
}

function insertList(type) {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    const listItem = type === "ul" ? "\n* List item" : "\n1. List item";
    textarea.value = textarea.value.substring(0, start) + listItem + textarea.value.substring(start);
    textarea.focus();
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
    // Initialize title counter
    if (titleInput && titleCounter) {
        titleCounter.textContent = titleInput.value.length;
    }
    
    // Initialize content counter
    updateCharCount();
    
    // Add input event listener for content
    const content = document.getElementById("content");
    if (content) {
        content.addEventListener("input", updateCharCount);
    }
    
    // Add form submit validation
    const form = document.querySelector('.write-blog-form');
    if (form) {
        form.addEventListener('submit', validateImageBeforeSubmit);
    }
    
    // Hide alert on load
    hideImageAlert();
});