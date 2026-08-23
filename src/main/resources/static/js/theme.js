
// Immediately invoked function to set the theme on load
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
})();

window.toggleTheme = function() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const targetTheme = (currentTheme === 'light') ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', targetTheme);
    localStorage.setItem('theme', targetTheme);
    
    window.updateThemeToggleText();
};

window.updateThemeToggleText = function() {
    // Need to handle multiple buttons if they exist, but getElementById works if there's only one.
    // Let's use querySelectorAll just in case.
    const btns = document.querySelectorAll('#themeToggleBtn, .theme-toggle-btn');
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const text = currentTheme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
    
    btns.forEach(btn => {
        btn.innerHTML = text;
    });
};

document.addEventListener('DOMContentLoaded', () => {
    window.updateThemeToggleText();
});
