document.addEventListener("DOMContentLoaded", function() {
    // Ensure that the Vue app is fully mounted before adding the 'visible' class
    const app = document.getElementById('app');

    if (app) {
        // Wait for Vue instance to be fully mounted before applying 'visible' class
        new Vue({
            el: '#app',
            mounted() {
                // Add the 'visible' class once the Vue app is ready
                document.body.classList.add('visible');
            }
        });
    } else {
        // If Vue instance isn't needed, apply 'visible' class after DOMContentLoaded
        document.body.classList.add('visible');
    }
});

// Show the loader when the page is about to unload
window.addEventListener("beforeunload", function () {
    document.getElementById("loader").style.display = "flex";
});

// Hide the loader when the page has fully loaded
window.addEventListener("load", function () {
    document.getElementById("loader").style.display = "none";
});

// Show the loader when internal links are clicked
const links = document.querySelectorAll("a");
links.forEach(link => {
    link.addEventListener("click", function (e) {
        document.getElementById("loader").style.display = "flex";
    });
});
