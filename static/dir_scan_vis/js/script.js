// static/dir_scan_vis/js/script.js

// Function to resize the Dash app iframe to be fully scaled
function resizeIframe() {
    const iframe = document.querySelector('#dash-app iframe');
    if (iframe) {
        iframe.style.width = '100%'; // Ensure full width
        iframe.style.height = window.innerHeight * 0.75 + 'px'; // Adjust height to 75% of the viewport height
    }
}

// Event listener to resize the iframe on window resize
window.addEventListener('resize', resizeIframe);

// Initial call to resize the iframe
document.addEventListener("DOMContentLoaded", resizeIframe);
