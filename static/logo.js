 document.addEventListener('DOMContentLoaded', () => {
      // Fetch the SVG logo and inject it into the container
      fetch('static/logo.svg')
        .then(response => {
          // Check if the request was successful
          if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
          }
          return response.text();
        })
        .then(svg => {
          const logoContainer = document.querySelector('.logo-container');
          if (logoContainer) {
            logoContainer.innerHTML = svg;
          }
        })
        .catch(error => {
          console.error('There was a problem fetching the logo:', error);
          // Optional: display a fallback or error message in the UI
          const logoContainer = document.querySelector('.logo-container');
          if (logoContainer) {
            logoContainer.innerHTML = '<p style="color: var(--subtle-gray);">Logo could not be loaded.</p>';
          }
        });
    });