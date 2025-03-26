document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    AOS.init({
        duration: 800,
        once: true
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Enhanced smooth scroll with offset for footer
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            const navHeight = document.querySelector('.navbar').offsetHeight;
            
            // Special handling for footer to ensure it scrolls fully into view
            const offset = targetId === '#footer' ? 0 : navHeight;
            
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });

            // Close mobile menu if open
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    });

    // Animated counter for stats
    const stats = document.querySelectorAll('.stat-number');
    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateValue(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    stats.forEach(stat => observer.observe(stat));

    // Enhanced counter animation
    function animateValue(obj) {
        const end = parseInt(obj.getAttribute('data-target'));
        const duration = 2000;
        const start = 0;
        let startTimestamp = null;

        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = Math.floor(progress * end);
            
            obj.textContent = current.toLocaleString();
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.textContent = end.toLocaleString();
            }
        };

        window.requestAnimationFrame(step);
    }

    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        hero.style.backgroundPosition = `center ${scrolled * 0.5}px`;
    });

    // Services carousel smooth scroll
    const carousel = document.querySelector('.services-carousel');
    let isDown = false;
    let startX;
    let scrollLeft;

    carousel.addEventListener('mousedown', (e) => {
        isDown = true;
        carousel.classList.add('active');
        startX = e.pageX - carousel.offsetLeft;
        scrollLeft = carousel.scrollLeft;
    });

    carousel.addEventListener('mouseleave', () => {
        isDown = false;
        carousel.classList.remove('active');
    });

    carousel.addEventListener('mouseup', () => {
        isDown = false;
        carousel.classList.remove('active');
    });

    carousel.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 2;
        carousel.scrollLeft = scrollLeft - walk;
    });

    // FAQ accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        item.addEventListener('click', () => {
            const answer = item.querySelector('.faq-answer');
            const isOpen = answer.style.maxHeight;

            // Close all other answers
            document.querySelectorAll('.faq-answer').forEach(a => {
                a.style.maxHeight = null;
                a.parentElement.classList.remove('active');
            });

            if (!isOpen) {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                item.classList.add('active');
            }
        });
    });

    // Initialize Swiper sliders
    const servicesSlider = new Swiper('.services-slider', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            },
        },
    });

    // Enhanced scroll animations
    const scrollElements = document.querySelectorAll('.scroll-animate');

    const elementInView = (el, percentageScroll = 100) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= 
            ((window.innerHeight || document.documentElement.clientHeight) * (percentageScroll/100))
        );
    };

    const displayScrollElement = (element) => {
        element.classList.add('scrolled');
    };

    const hideScrollElement = (element) => {
        element.classList.remove('scrolled');
    };

    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 100)) {
                displayScrollElement(el);
            } else {
                hideScrollElement(el);
            }
        });
    };

    window.addEventListener('scroll', () => {
        handleScrollAnimation();
    });

    // Enhanced FAQ functionality
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            const faqItem = question.parentElement;
            const isOpen = faqItem.classList.contains('active');
            
            // Close all other FAQs
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
                const icon = item.querySelector('.faq-icon i');
                icon.className = 'fas fa-plus';
            });
            
            // Toggle current FAQ
            if (!isOpen) {
                faqItem.classList.add('active');
                const icon = faqItem.querySelector('.faq-icon i');
                icon.className = 'fas fa-times';
                
                // Smooth scroll if not in view
                const rect = faqItem.getBoundingClientRect();
                if (rect.bottom > window.innerHeight) {
                    faqItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });

    // Enhanced FAQ functionality with smooth animations
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            const faqItem = question.parentElement;
            const answer = faqItem.querySelector('.faq-answer');
            const icon = question.querySelector('.faq-icon i');
            const isOpen = faqItem.classList.contains('active');

            // Close all other FAQs
            document.querySelectorAll('.faq-item').forEach(item => {
                if (item !== faqItem && item.classList.contains('active')) {
                    item.classList.remove('active');
                    const otherIcon = item.querySelector('.faq-icon i');
                    const otherAnswer = item.querySelector('.faq-answer');
                    otherIcon.className = 'fas fa-plus';
                    otherAnswer.style.maxHeight = null;
                }
            });

            // Toggle current FAQ
            if (!isOpen) {
                faqItem.classList.add('active');
                icon.className = 'fas fa-minus';
                answer.style.maxHeight = answer.scrollHeight + "px";
            } else {
                faqItem.classList.remove('active');
                icon.className = 'fas fa-plus';
                answer.style.maxHeight = null;
            }
        });
    });

    // Enhanced animations for elements
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.fade-up');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            
            if (elementTop < window.innerHeight - 100 && elementBottom > 0) {
                element.classList.add('visible');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    window.addEventListener('load', animateOnScroll);

    // Add smooth parallax effect
    const parallaxElements = document.querySelectorAll('.parallax');
    window.addEventListener('scroll', () => {
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(window.pageYOffset * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
});
