function initializeTheme() {
    // Get saved preferences or use defaults
    const theme = localStorage.getItem('theme') || 'light';
    const color = localStorage.getItem('themeColor') || 'blue';
    
    // Apply theme
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('data-color', color);
}

function setTheme(theme) {
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
}

function setThemeColor(color) {
    localStorage.setItem('themeColor', color);
    document.documentElement.setAttribute('data-color', color);
}

// Initialize theme when DOM loads
document.addEventListener('DOMContentLoaded', initializeTheme);
