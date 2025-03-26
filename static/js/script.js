function initializeSettings() {
    document.querySelectorAll('.color-circle').forEach(circle => {
        circle.addEventListener('click', function() {
            document.querySelectorAll('.color-circle').forEach(c => {
                c.classList.remove('selected');
            });
            this.classList.add('selected');
            // Apply theme immediately on click
            const selectedColor = this.getAttribute('data-color');
            applyTheme(selectedColor);
            localStorage.setItem('themeColor', selectedColor); // Store in local storage
        });
    });

    document.querySelector('.btn-save').addEventListener('click', function() {
        const darkMode = document.getElementById('darkModeToggle').checked;
        const selectedColor = document.querySelector('.color-circle.selected').getAttribute('data-color');
        const showNsfw = document.getElementById('showNsfw').checked;
        const language = document.querySelector('.language-dropdown').value;

        const preferences = {
            darkMode: darkMode,
            themeColor: selectedColor,
            showNsfw: showNsfw,
            language: language
        };

        fetch('/save_preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preferences)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Settings saved successfully!');
                localStorage.setItem('themeColor', selectedColor); // Store in local storage
                applyTheme(selectedColor); // Apply the theme after saving
            } else {
                alert('Error saving settings: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error saving settings!');
        });
    });

    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.checked = localStorage.getItem('darkMode') === 'true';
    
    darkModeToggle.addEventListener('change', function() {
        const isDark = this.checked;
        applyDarkMode(isDark);
        // Store in localStorage immediately
        localStorage.setItem('darkMode', isDark);
    });

    // Language dropdown
    const languageDropdown = document.querySelector('.language-dropdown');
    languageDropdown.addEventListener('change', function() {
        changeLanguage(this.value);
    });
}

function applyDarkMode(isDark) {
    if (isDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.style.backgroundColor = '#121a29';
    } else {
        document.documentElement.removeAttribute('data-theme');
        document.body.style.backgroundColor = '#f4f5f7';
    }
    localStorage.setItem('darkMode', isDark);
}

function changeLanguage(lang) {
    localStorage.setItem('language', lang);
    fetch('/change_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ language: lang })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.reload();
        }
    });
}

function applyTheme(themeColor) {
    const colors = {
        'blue': { main: '#007bff', hover: '#0056b3' },
        'green': { main: '#28a745', hover: '#1e7e34' },
        'purple': { main: '#8540f5', hover: '#6629d1' },
        'orange': { main: '#fd7e14', hover: '#dc6502' },
        'red': { main: '#dc3545', hover: '#bd2130' },
        'custom': { main: '#7f7fff', hover: '#6666cc' }
    };

    const selectedColors = colors[themeColor] || colors['blue'];
    document.documentElement.style.setProperty('--theme-color', selectedColors.main);
    document.documentElement.style.setProperty('--theme-hover', selectedColors.hover);
    
    // Store the selected color
    localStorage.setItem('themeColor', themeColor);
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.settings-card')) {
        initializeSettings();
    }
    // Apply theme on load
    const storedColor = localStorage.getItem('themeColor');
    if (storedColor) {
        applyTheme(storedColor);
        // Ensure the correct color circle is marked as selected
        document.querySelectorAll('.color-circle').forEach(circle => {
            circle.classList.remove('selected');
            if (circle.getAttribute('data-color') === storedColor) {
                circle.classList.add('selected');
            }
        });
    }

    // Initialize dark mode from localStorage or server preference
    const savedDarkMode = localStorage.getItem('darkMode') === 'true' || 
                         (document.documentElement.getAttribute('data-theme') === 'dark');
    if (document.getElementById('darkModeToggle')) {
        document.getElementById('darkModeToggle').checked = savedDarkMode;
        applyDarkMode(savedDarkMode);
    }

    // Initialize language
    const savedLanguage = localStorage.getItem('language') || 'en';
    document.querySelector('.language-dropdown').value = savedLanguage;
});
