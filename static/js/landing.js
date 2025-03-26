document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animation library
    AOS.init({
        duration: 1000,
        once: true
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Enhanced Navbar scroll behavior
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // Add loading animation for images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            img.classList.add('loaded');
        });
    });

    // Enhanced FAQ functionality
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            const faqItem = question.parentElement;
            const answer = faqItem.querySelector('.faq-answer');
            const icon = question.querySelector('.faq-icon i');
            
            // Close all other FAQ items
            document.querySelectorAll('.faq-item.active').forEach(activeItem => {
                if (activeItem !== faqItem) {
                    activeItem.classList.remove('active');
                    activeItem.querySelector('.faq-answer').style.maxHeight = '0';
                    activeItem.querySelector('.faq-icon i').className = 'fas fa-plus';
                }
            });
            
            // Toggle current FAQ item
            faqItem.classList.toggle('active');
            if (faqItem.classList.contains('active')) {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                icon.className = 'fas fa-minus';
            } else {
                answer.style.maxHeight = '0';
                icon.className = 'fas fa-plus';
            }
        });
    });
});
