new Vue({
    el: '#app',
    data() {
        return {
            activeCard: null,
        };
    },
    methods: {
        animateCard(cardElement) {
            if (this.activeCard) {
                // Reset previously active card
                this.resetAnimation(this.activeCard);
            }
            this.activeCard = cardElement;

            // Animate the card
            gsap.to(cardElement, {
                scale: 1.05,
                duration: 0.3,
                ease: 'power2.out',
                zIndex: 10,
                transformOrigin: 'center left',
                position: 'absolute',
                top: 0,
                left: 0,
                width: '80%',
                height: '80%',
                margin: 'auto',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
                onComplete: () => {
                    gsap.to(cardElement, {
                        x: (window.innerWidth - cardElement.offsetWidth) / 2 - cardElement.getBoundingClientRect().left,
                        y: (window.innerHeight - cardElement.offsetHeight) / 2 - cardElement.getBoundingClientRect().top,
                        duration: 0.3,
                        ease: 'power2.out'
                    });
                }
            });
        },
        resetAnimation(cardElement) {
            gsap.to(cardElement, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out',
                zIndex: 1,
                position: 'relative',
                top: 'auto',
                left: 'auto',
                width: 'auto',
                height: 'auto',
                margin: '0',
                boxShadow: 'none',
                x: 0,
                y: 0
            });
        }
    },
    mounted() {
        const cards = document.querySelectorAll('.animated-card');

        cards.forEach(card => {
            card.addEventListener('mouseenter', () => this.animateCard(card));
            card.addEventListener('mouseleave', () => this.resetAnimation(card));
        });
    }
});
