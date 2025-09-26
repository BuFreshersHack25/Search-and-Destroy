document.addEventListener('DOMContentLoaded', () => {
    // Select the HTML elements
    const menuBtn = document.getElementById('menuBtn');
    const navOverlay = document.getElementById('navOverlay');
    const closeNavBtn = document.getElementById('closeNavBtn');

    // Check if all elements exist to prevent errors
    if (!menuBtn || !navOverlay || !closeNavBtn) {
        console.error("Navbar JS Error: One or more required elements (menuBtn, navOverlay, closeNavBtn) were not found.");
        return;
    }

    // Function to show the navigation
    const showNav = () => {
        navOverlay.classList.add('is-visible');
    };

    // Function to hide the navigation
    const hideNav = () => {
        navOverlay.classList.remove('is-visible');
    };

    // Attach the functions to the button click events
    menuBtn.addEventListener('click', showNav);
    closeNavBtn.addEventListener('click', hideNav);
});