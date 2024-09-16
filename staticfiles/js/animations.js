// animations.js

// Vue.js Initialization
new Vue({
    el: '#app',
});

// GSAP Animation for Jigsaw Puzzle Effect
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.animated-card');
    
    // Create a timeline for hover animation for better control
    const hoverTimeline = gsap.timeline({ paused: true });

    cards.forEach(card => {
        // Mouse enter event for individual card
        card.addEventListener('mouseenter', () => {
            // Reset the timeline in case it's mid-animation
            hoverTimeline.clear();

            // Animate all cards to scale down, except the hovered one
            hoverTimeline.to(cards, {
                scale: 0.9,
                duration: 0.3,
                ease: 'power2.out',
                stagger: {
                    amount: 0.1, // slight delay for each card for a staggered effect
                    onComplete: () => {
                        // Animate the hovered card to scale up
                        gsap.to(card, { 
                            scale: 1.2,
                            duration: 0.4,
                            ease: 'power2.out',
                            zIndex: 10,
                            boxShadow: '0px 10px 20px rgba(0,0,0,0.2)',
                            rotation: '3deg',
                        });
                    }
                }
            });
        });

        // Mouse leave event to reset the animation
        card.addEventListener('mouseleave', () => {
            // Reset the hover card
            gsap.to(card, {
                scale: 1,
                duration: 0.4,
                ease: 'power2.out',
                zIndex: 1,
                boxShadow: 'none',
                rotation: '0deg',
            });

            // Reset all cards to original scale
            gsap.to(cards, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out',
                stagger: 0.05
            });
        });
    });
});
