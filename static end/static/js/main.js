// Theme Management
const ThemeManager = {
    init() {
        this.toggleBtn = document.getElementById('theme-toggle');
        this.icon = this.toggleBtn?.querySelector('i');
        this.html = document.documentElement;
        
        // Check local storage or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            this.setTheme('dark');
        } else {
            this.setTheme('light');
        }

        // Event Listeners
        this.toggleBtn?.addEventListener('click', () => this.toggleTheme());
    },

    setTheme(theme) {
        if (theme === 'dark') {
            this.html.setAttribute('data-theme', 'dark');
            this.icon?.classList.remove('bi-moon-fill');
            this.icon?.classList.add('bi-sun-fill');
            localStorage.setItem('theme', 'dark');
        } else {
            this.html.removeAttribute('data-theme');
            this.icon?.classList.remove('bi-sun-fill');
            this.icon?.classList.add('bi-moon-fill');
            localStorage.setItem('theme', 'light');
        }
    },

    toggleTheme() {
        const currentTheme = this.html.getAttribute('data-theme');
        this.setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
});
