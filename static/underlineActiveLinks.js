// Get the current page URL
var currentPage = window.location.pathname;
// Get all navigation links
var navLinks = document.querySelectorAll(".navlink");
// Loop through each link and check if it matches the current page
navLinks.forEach(function (link) {
    // Use the link's href attribute to match with the current page
    if (link.getAttribute("href") === currentPage) {
        // Add the 'active' class to the matching link
        link.classList.add("active");
    }
});
