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