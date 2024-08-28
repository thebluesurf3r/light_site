// animations.js

// Vue.js Initialization
new Vue({
    el: '#app',
});

// GSAP Animation for Jigsaw Puzzle Effect
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.animated-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(cards, { 
                scale: 0.9,
                duration: 0.3,
                ease: 'power2.out',
                onComplete: () => {
                    gsap.to(card, { 
                        scale: 1.2,
                        duration: 0.3,
                        ease: 'power2.out',
                        zIndex: 10,
                    });
                }
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(cards, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out',
            });
        });
    });
});
