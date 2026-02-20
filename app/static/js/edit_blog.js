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

// New image preview
function previewNewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const previewSection = document.getElementById("new-image-preview");
        const previewImg = document.getElementById("new-preview-img");

        reader.onload = function (e) {
            if (previewImg && previewSection) {
                previewImg.src = e.target.result;
                previewSection.style.display = "block";
            }
        };

        reader.readAsDataURL(input.files[0]);
        
        // Uncheck "keep current image" when new image is selected
        const keepImage = document.getElementById("keep_image");
        if (keepImage) {
            keepImage.checked = false;
        }
    }
}

function changeNewImage() {
    document.getElementById("new_image").click();
    document.getElementById("new-image-preview").style.display = "none";
}

function removeNewImage() {
    document.getElementById("new_image").value = "";
    document.getElementById("new-image-preview").style.display = "none";
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

// ========== UPDATE CARD FUNCTIONS ==========
function showUpdateCard(blogId, blogTitle) {
    console.log("Show update card called for blog:", blogId);
    
    const updateCard = document.getElementById('updateConfirmCard');
    const updateForm = document.getElementById('updateBlogForm');
    const updateMessage = document.getElementById('updateBlogTitle');
    const lastUpdatedSpan = document.getElementById('lastUpdatedTime');
    
    // Get current form values
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const contentType = document.getElementById('content_type').value;
    const keepImage = document.getElementById('keep_image').checked;
    
    // Check if there's a new image selected
    const newImageInput = document.getElementById('new_image');
    const hasNewImage = newImageInput && newImageInput.files && newImageInput.files[0];
    
    console.log("Form values:", {title, content, contentType, keepImage, hasNewImage});
    
    if (updateCard && updateForm && updateMessage) {
        // Update form action
        updateForm.action = `/edit/${blogId}/`;
        
        // Set hidden input values
        const hiddenTitle = document.getElementById('hidden_title');
        const hiddenContent = document.getElementById('hidden_content');
        const hiddenContentType = document.getElementById('hidden_content_type');
        const hiddenKeepImage = document.getElementById('hidden_keep_image');
        
        if (hiddenTitle) hiddenTitle.value = title;
        if (hiddenContent) hiddenContent.value = content;
        if (hiddenContentType) hiddenContentType.value = contentType;
        
        // Handle keep image checkbox
        if (hiddenKeepImage) {
            if (hasNewImage) {
                // If there's a new image, we don't want to keep the old one
                hiddenKeepImage.value = 'off';
            } else {
                hiddenKeepImage.value = keepImage ? 'on' : 'off';
            }
        }
        
        // Handle file upload - we need to append the file to the form
        if (hasNewImage) {
            // Create a new FormData object
            const formData = new FormData(updateForm);
            
            // Append the file to the form data
            formData.append('new_image', newImageInput.files[0]);
            
            // Override the form submit to use FormData
            updateForm.onsubmit = function(e) {
                e.preventDefault();
                
                // Create a new FormData with all the data
                const submitFormData = new FormData();
                submitFormData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
                submitFormData.append('title', title);
                submitFormData.append('content', content);
                submitFormData.append('content_type', contentType);
                submitFormData.append('keep_image', keepImage ? 'on' : 'off');
                submitFormData.append('action', 'update');
                submitFormData.append('new_image', newImageInput.files[0]);
                
                // Submit via fetch
                fetch(`/edit/${blogId}/`, {
                    method: 'POST',
                    body: submitFormData
                })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
                
                return false;
            };
        } else {
            // Reset the onsubmit to default
            updateForm.onsubmit = null;
        }
        
        // Update the message with blog title
        updateMessage.innerHTML = `Are you sure you want to update "<strong>${blogTitle}</strong>"?`;
        
        // Update last updated time if element exists
        if (lastUpdatedSpan) {
            const now = new Date();
            lastUpdatedSpan.textContent = now.toLocaleString();
        }
        
        // Show the card
        updateCard.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    } else {
        console.error("Update card elements not found:", {
            updateCard: !!updateCard,
            updateForm: !!updateForm,
            updateMessage: !!updateMessage
        });
    }
}

function hideUpdateCard() {
    const updateCard = document.getElementById('updateConfirmCard');
    if (updateCard) {
        updateCard.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ========== TEXT FORMATTING FUNCTIONS ==========
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
    updateCharCount();
}

function insertHeading() {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    textarea.value = textarea.value.substring(0, start) + "\n## Heading\n" + textarea.value.substring(start);
    textarea.focus();
    updateCharCount();
}

function insertLink() {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    textarea.value = textarea.value.substring(0, start) + "[Link Text](https://example.com)" + textarea.value.substring(start);
    textarea.focus();
    updateCharCount();
}

function insertList(type) {
    const textarea = document.getElementById("content");
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    const listItem = type === "ul" ? "\n* List item" : "\n1. List item";
    textarea.value = textarea.value.substring(0, start) + listItem + textarea.value.substring(start);
    textarea.focus();
    updateCharCount();
}

// ========== GLOBAL CARD DISMISSAL HANDLERS ==========
window.addEventListener('click', function(event) {
    const alertCard = document.getElementById('imageSizeAlert');
    if (event.target === alertCard) hideImageAlert();
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        hideImageAlert();
    }
});

// ========== INITIALIZATION ==========
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
    
    // Add new image input listener
    const newImageInput = document.getElementById("new_image");
    if (newImageInput) {
        newImageInput.addEventListener('change', function() {
            previewNewImage(this);
        });
    }
    
    // Handle keep image checkbox
    const keepImageCheckbox = document.getElementById("keep_image");
    const newImageSection = document.querySelector('.image-upload-section');
    
    if (keepImageCheckbox && newImageSection) {
        keepImageCheckbox.addEventListener('change', function() {
            if (this.checked) {
                newImageSection.style.opacity = '0.5';
                newImageSection.style.pointerEvents = 'none';
                // Clear any selected new image
                document.getElementById("new_image").value = "";
                document.getElementById("new-image-preview").style.display = "none";
            } else {
                newImageSection.style.opacity = '1';
                newImageSection.style.pointerEvents = 'auto';
            }
        });
    }
    
    // Hide all cards on load
    hideImageAlert();
});