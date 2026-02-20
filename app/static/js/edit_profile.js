// ========== IMAGE PREVIEW AND VALIDATION ==========
function previewImage(input) {
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const reader = new FileReader();
    const preview = document.querySelector(".current-avatar img");
    const fileNameDisplay = document.getElementById('file-name-display');

    // Validate file size (5MB max)
    const fileSize = file.size / 1024 / 1024; // MB
    if (fileSize > 5) {
      // Show custom alert card
      showImageAlert(fileSize.toFixed(2));
      input.value = ""; // Clear the input
      if (fileNameDisplay) {
        fileNameDisplay.innerHTML = '';
      }
      return;
    }

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      showImageTypeAlert();
      input.value = "";
      if (fileNameDisplay) {
        fileNameDisplay.innerHTML = '';
      }
      return;
    }

    reader.onload = function (e) {
      preview.src = e.target.result;
    };

    reader.readAsDataURL(file);
    
    // Show file name
    if (fileNameDisplay) {
      fileNameDisplay.innerHTML = `<i class="fas fa-check-circle" style="color: #28a745;"></i> Selected: ${file.name} (${fileSize.toFixed(2)} MB)`;
    }
    
    console.log(`Selected file: ${file.name} (${fileSize.toFixed(2)} MB)`);
  }
}

// ========== IMAGE ALERT CARD FUNCTIONS ==========
function showImageAlert(fileSize) {
  const alertCard = document.getElementById('imageSizeAlert');
  const alertMessage = document.getElementById('imageAlertMessage');
  
  if (alertCard && alertMessage) {
    alertMessage.innerHTML = `The image you uploaded (<strong>${fileSize}MB</strong>) exceeds the <strong>5MB size limit</strong>. Please optimize your image or choose a smaller file.`;
    alertCard.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function showImageTypeAlert() {
  const alertCard = document.getElementById('imageSizeAlert');
  const alertMessage = document.getElementById('imageAlertMessage');
  const suggestions = document.querySelector('.alert-suggestions ul');
  
  if (alertCard && alertMessage) {
    alertMessage.innerHTML = `The file type is not supported. Please upload a valid image file.`;
    
    // Update suggestions for type error
    if (suggestions) {
      suggestions.innerHTML = `
        <li><i class="fas fa-check"></i> Supported formats: JPG, PNG, GIF, WebP</li>
        <li><i class="fas fa-check"></i> Maximum file size: 5MB</li>
        <li><i class="fas fa-check"></i> Square images work best for profile pictures</li>
      `;
    }
    
    alertCard.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function hideImageAlert() {
  const alertCard = document.getElementById('imageSizeAlert');
  if (alertCard) {
    alertCard.style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Restore original suggestions
    const suggestions = document.querySelector('.alert-suggestions ul');
    if (suggestions) {
      suggestions.innerHTML = `
        <li><i class="fas fa-check"></i> Use image compression tools like TinyPNG</li>
        <li><i class="fas fa-check"></i> Resize to 500x500px recommended dimensions</li>
        <li><i class="fas fa-check"></i> Convert to JPEG for smaller file size</li>
        <li><i class="fas fa-check"></i> Square images work best for profile pictures</li>
      `;
    }
  }
}

// ========== BIO CHARACTER COUNTER ==========
const bioTextarea = document.getElementById("bio");
const bioCounter = document.getElementById("bio-counter");

if (bioTextarea && bioCounter) {
  bioTextarea.addEventListener("input", function () {
    const maxLength = 500;
    const currentLength = this.value.length;
    
    bioCounter.textContent = currentLength;
    
    if (currentLength > maxLength) {
      this.value = this.value.substring(0, maxLength);
      bioCounter.textContent = maxLength;
    }
    
    // Change color when approaching limit
    if (currentLength > 450) {
      bioCounter.style.color = '#ff7e5f';
      bioCounter.style.fontWeight = '600';
    } else {
      bioCounter.style.color = '';
      bioCounter.style.fontWeight = '';
    }
  });
}

// ========== SAVE CONFIRMATION CARD FUNCTIONS ==========
function showSaveCard() {
  console.log("Show save card called");
  const saveCard = document.getElementById('saveConfirmCard');
  
  if (saveCard) {
    saveCard.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    console.log("Save card displayed");
  } else {
    console.error("Save card element not found!");
  }
}

function hideSaveCard() {
  const saveCard = document.getElementById('saveConfirmCard');
  if (saveCard) {
    saveCard.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
}

function submitForm() {
  console.log("Submitting form");
  const form = document.getElementById('editProfileForm');
  if (form) {
    // Check if a new image is selected and validate size one more time
    const fileInput = document.getElementById('profile_picture');
    if (fileInput && fileInput.files && fileInput.files[0]) {
      const fileSize = fileInput.files[0].size / 1024 / 1024;
      if (fileSize > 5) {
        showImageAlert(fileSize.toFixed(2));
        hideSaveCard();
        return;
      }
    }
    form.submit();
  } else {
    console.error("Form not found!");
  }
}

// ========== GLOBAL CARD DISMISSAL HANDLERS ==========
window.addEventListener('click', function(event) {
  const alertCard = document.getElementById('imageSizeAlert');
  if (event.target === alertCard) hideImageAlert();
  
  const saveCard = document.getElementById('saveConfirmCard');
  if (event.target === saveCard) hideSaveCard();
});

document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    hideImageAlert();
    hideSaveCard();
  }
});

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM loaded - initializing edit profile page");
  
  // Initialize bio counter if bio exists
  if (bioTextarea && bioCounter) {
    bioCounter.textContent = bioTextarea.value.length;
  }
  
  // Hide all cards on load
  hideImageAlert();
  hideSaveCard();
  
  // Verify that save card exists
  const saveCard = document.getElementById('saveConfirmCard');
  if (saveCard) {
    console.log("Save card found in DOM");
  } else {
    console.error("Save card NOT found in DOM - check HTML");
  }
});