// Carousel functionality with auto-scroll only
document.addEventListener("DOMContentLoaded", function () {
  const carouselWrapper = document.querySelector(".carousel-wrapper");
  const slides = document.querySelectorAll(".carousel-slide");
  const dots = document.querySelectorAll(".indicator-dot");

  let currentSlide = 0;
  const totalSlides = slides.length;
  let autoSlideInterval;

  // Initialize carousel
  updateCarousel();

  // Start auto-scrolling
  startAutoScroll();

  // Function to navigate to a specific slide
  function navigateToSlide(slideIndex) {
    // Handle slide boundaries
    if (slideIndex < 0) {
      slideIndex = totalSlides - 1;
    } else if (slideIndex >= totalSlides) {
      slideIndex = 0;
    }

    currentSlide = slideIndex;
    updateCarousel();
  }

  // Function to update the carousel display
  function updateCarousel() {
    // Move the carousel wrapper
    carouselWrapper.style.transform = `translateX(-${currentSlide * 100}%)`;

    // Update indicators
    dots.forEach((dot, index) => {
      if (index === currentSlide) {
        dot.classList.add("active");
      } else {
        dot.classList.remove("active");
      }
    });
  }

  // Function to start auto-scrolling
  function startAutoScroll() {
    // Clear any existing interval first
    if (autoSlideInterval) {
      clearInterval(autoSlideInterval);
    }

    // Set up new interval for auto-scrolling every 8 seconds
    autoSlideInterval = setInterval(() => {
      navigateToSlide(currentSlide + 1);
    }, 8000);
  }

  // Function to pause auto-scrolling
  function pauseAutoScroll() {
    if (autoSlideInterval) {
      clearInterval(autoSlideInterval);
      autoSlideInterval = null;
    }
  }

  // Pause auto-scroll on hover for better user experience
  carouselWrapper.addEventListener("mouseenter", pauseAutoScroll);

  // Resume auto-scroll when mouse leaves
  carouselWrapper.addEventListener("mouseleave", startAutoScroll);

  //Allow clicking on dots for navigation
  dots.forEach((dot, index) => {
    dot.addEventListener("click", function () {
      navigateToSlide(index);
      // Restart auto-scroll timer after manual navigation
      startAutoScroll();
    });
  });
});

// Handle scroll: Change categories to blueish-bg and buttons to white after scroll
window.addEventListener("scroll", function () {
  const scrollTop = window.scrollY;
  const documentHeight = document.body.scrollHeight - window.innerHeight;
  const scrollPercent = (scrollTop / documentHeight) * 100;

  // Use querySelector to get the single .categories container
  const categories = document.querySelector(".categories");
  const category_btns = document.querySelectorAll(".category-btn");

  if (scrollPercent > 1.5) {
    // Add a class instead of directly manipulating styles
    categories.classList.add("scrolled");

    category_btns.forEach((btn) => {
      btn.classList.add("scrolled");
    });
  } else {
    // Remove the class
    categories.classList.remove("scrolled");

    category_btns.forEach((btn) => {
      btn.classList.remove("scrolled");
    });
  }
});

// background sync with manual scrolling
document.addEventListener("DOMContentLoaded", function () {
  const slides = document.querySelectorAll(".carousel-slide");
  const spotlightSection = document.querySelector(".spotlight");

  // Set up Intersection Observer to detect visible slide
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target.querySelector("img");
          if (img) {
            spotlightSection.style.backgroundImage = `url('${img.src}')`;
          }
        }
      });
    },
    {
      threshold: 0.5, // Trigger when 50% of slide is visible
    },
  );

  // Observe each slide
  slides.forEach((slide) => {
    observer.observe(slide);
  });

  // Set initial background
  const firstImg = slides[0].querySelector("img");
  if (firstImg) {
    spotlightSection.style.backgroundImage = `url('${firstImg.src}')`;
  }
});



// Editor's Picks Navigation Arrows Functionality
document.addEventListener("DOMContentLoaded", function () {
  const editorPosts = document.querySelector(".blog-posts");
  const leftArrow = document.querySelector(".left-right .fa-arrow-left");
  const rightArrow = document.querySelector(".left-right .fa-arrow-right");

  if (editorPosts && leftArrow && rightArrow) {
    // Calculate scroll amount (about 80% of container width)
    const scrollAmount = editorPosts.clientWidth * 0.8;

    leftArrow.addEventListener("click", function () {
      editorPosts.scrollBy({
        left: -scrollAmount,
        behavior: "smooth",
      });
    });

    rightArrow.addEventListener("click", function () {
      editorPosts.scrollBy({
        left: scrollAmount,
        behavior: "smooth",
      });
    });
  }
});


// Featured posts Navigation Arrows Functionality
document.addEventListener("DOMContentLoaded", function () {
  const featured = document.getElementById("blog-posts-featured");
  const leftArrow = document.getElementById("featured-prev");
  const rightArrow = document.getElementById("featured-next");

  if (featured && leftArrow && rightArrow) {
    // Calculate scroll amount (about 80% of container width)
    const scrollAmount = featured.clientWidth * 0.8;

    leftArrow.addEventListener("click", function () {
      featured.scrollBy({
        left: -scrollAmount,
        behavior: "smooth",
      });
    });

    rightArrow.addEventListener("click", function () {
      featured.scrollBy({
        left: scrollAmount,
        behavior: "smooth",
      });
    });
  }
});



// About Section Animation and Functionality
document.addEventListener("DOMContentLoaded", function () {
  const aboutContainer = document.querySelector(".about-container");

  // Scroll reveal animation
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          aboutContainer.classList.add("visible");
        }
      });
    },
    { threshold: 0.2 },
  );

  if (aboutContainer) {
    observer.observe(aboutContainer);
  }
});


document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("promoModal");
  const closeBtn = document.querySelector(".promo-modal-close");
  const modalContent = document.querySelector(".promo-modal-content");

  // Function to check if we're on homepage
  function isHomepage() {
    const path = window.location.pathname;
    const homePaths = ["/", "/home", "/index", ""];
    return homePaths.includes(path);
  }

  // Function to show modal
  function showModal() {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";

    // Mark as shown in session storage
    sessionStorage.setItem("promoModalShown", "true");
  }

  // Function to close modal
  function closeModal() {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
    document.documentElement.style.overflow = "auto";
  }

  // Function to handle escape key
  function handleEscapeKey(e) {
    if (e.key === "Escape" && modal.style.display === "flex") {
      closeModal();
      document.removeEventListener("keydown", handleEscapeKey);
    }
  }

  // Function to handle click outside
  function handleOutsideClick(e) {
    if (
      e.target === modal ||
      e.target.classList.contains("promo-modal-overlay")
    ) {
      closeModal();
      modal.removeEventListener("click", handleOutsideClick);
    }
  }

  // Check conditions and show modal
  if (isHomepage()) {
    const modalShown = sessionStorage.getItem("promoModalShown");

    if (!modalShown) {
      // Show after 3 seconds
      setTimeout(showModal, 3000);

      // Setup event listeners after modal is shown
      setTimeout(function () {
        if (modal.style.display === "flex") {
          // Escape key listener
          document.addEventListener("keydown", handleEscapeKey);

          // Click outside listener
          modal.addEventListener("click", handleOutsideClick);
        }
      }, 5000);
    }
  }

  // Close button event listener
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      closeModal();
      // Clean up event listeners
      document.removeEventListener("keydown", handleEscapeKey);
      modal.removeEventListener("click", handleOutsideClick);
    });
  }

  // Prevent modal content click from closing modal
  if (modalContent) {
    modalContent.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  }
});
