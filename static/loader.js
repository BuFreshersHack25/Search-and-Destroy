 document.addEventListener('DOMContentLoaded', () => {
      // Fetch the SVG logo and inject it into the container
      const injectLoader = () => {
        fetch('static/loader.svg')
          .then(response => {
            // Check if the request was successful
            if (!response.ok) {
              throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.text();
          })
          .then(svg => {
            const loaderContainer = document.querySelector('.loader-container');
            if (loaderContainer) {
              loaderContainer.innerHTML = svg;
            }
          })
          .catch(error => {
            console.error('There was a problem fetching the logo:', error);
            // Optional: display a fallback or error message in the UI
            const loaderContainer = document.querySelector('.loader-container');
            if (loaderContainer) {
              loaderContainer.innerHTML = '<p style="color: var(--subtle-gray);">Loading...</p>';
            }
          });
        };
        injectLoader();
        window.injectLoader = injectLoader;
    });