Vue.config.compatConfig = {
    MODE: 3, // Enable compatibility mode with Vue 3
    GLOBAL_MOUNT: true, // Allow usage of `new Vue()` in Vue 3
    GLOBAL_EXTEND: true, // Enable compatibility for global Vue.extend()
    GLOBAL_PROTOTYPE: true // Enable compatibility for Vue.prototype
};

import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';

// Import Bootstrap and BootstrapVue CSS files
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

// Install BootstrapVue
Vue.use(BootstrapVue);

new Vue({
    el: '#app',
    data() {
        return {
            activeCard: null,
            activeHero: null, // Track the active hero element
            value: 50,        // Value for the progress bar
            max: 100          // Max value for the progress bar
        };
    },
    methods: {
        randomValue() {
            this.value = Math.floor(Math.random() * this.max); // Randomize progress bar value
        },
        animateCard(cardElement) {
            if (this.activeCard) {
                this.resetAnimation(this.activeCard);
            }
            this.activeCard = cardElement;
            const isMobile = window.innerWidth <= 768;
            gsap.to(cardElement, {
                scale: isMobile ? 1.02 : 1.05,
                duration: 0.1,
                ease: 'power2.out',
                zIndex: 2,
                position: 'absolute',
                top: 0,
                left: 0,
                width: isMobile ? '90%' : '80%',
                height: isMobile ? '90%' : '80%',
                margin: 'auto',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
                onComplete: () => {
                    gsap.to(cardElement, {
                        x: (window.innerWidth - cardElement.offsetWidth) / 2 - cardElement.getBoundingClientRect().left,
                        y: (window.innerHeight - cardElement.offsetHeight) / 2 - cardElement.getBoundingClientRect().top,
                        duration: 0.2,
                        ease: 'power2.out'
                    });
                }
            });
        },
        resetAnimation(cardElement) {
            gsap.to(cardElement, {
                scale: 1,
                duration: 0.1,
                ease: 'power2.out',
                zIndex: 1,
                position: 'absolute',
                top: 'auto',
                left: 'auto',
                width: 'auto',
                height: 'auto',
                margin: '0',
                boxShadow: 'none',
                x: 0,
                y: 0
            });
        },
        animateHero(heroElement) {
            if (this.activeHero) {
                this.resetHeroAnimation(this.activeHero);
            }
            this.activeHero = heroElement;
            gsap.to(heroElement, {
                scale: 1.02,
                duration: 0.1,
                ease: 'power2.out',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.5)',
                backgroundColor: '#343a40',
            });
        },
        resetHeroAnimation(heroElement) {
            gsap.to(heroElement, {
                scale: 1,
                duration: 0.1,
                ease: 'power2.out',
                boxShadow: 'none',
                backgroundColor: '#212529',
            });
        }
    },
    mounted() {
        const cards = document.querySelectorAll('.animated-card');
        const hero = document.querySelector('.hero');

        cards.forEach(card => {
            card.addEventListener('mouseenter', () => this.animateCard(card));
            card.addEventListener('mouseleave', () => this.resetAnimation(card));
        });

        if (hero) {
            hero.addEventListener('mouseenter', () => this.animateHero(hero));
            hero.addEventListener('mouseleave', () => this.resetHeroAnimation(hero));
        }
    }
});
