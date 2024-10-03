// static/dir_scan_vis/js/animations.js

// Smoothly fade in the search result count when the search is performed
document.addEventListener("DOMContentLoaded", () => {
    const resultCountSection = document.querySelector('.result-count-section');
    const searchForm = document.querySelector('.search-section form');

    searchForm.addEventListener('submit', () => {
        resultCountSection.style.opacity = 0; // Fade out
        setTimeout(() => {
            resultCountSection.style.opacity = 1; // Fade in
            resultCountSection.style.transition = 'opacity 0.5s ease-in-out';
        }, 500);
    });
});