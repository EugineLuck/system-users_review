const themeToggleLink = document.getElementById('themeToggle');
    const body = document.body;

    function toggleTheme() {
        const currentTheme = localStorage.getItem('Theme') || 'auto';
        if (currentTheme === 'light') {
            body.classList.remove('bg-light', 'text-dark');
            body.classList.add('bg-dark', 'text-light');
            localStorage.setItem('Theme', 'dark');
            themeToggleLink.textContent = '(Theme: dark)';
        } else if (currentTheme === 'dark') {
            body.classList.remove('bg-dark', 'text-light');
            body.classList.add('bg-light', 'text-dark');
            localStorage.setItem('Theme', 'light');
            themeToggleLink.textContent = '(Theme: light)';
        } else {
            body.classList.remove('bg-light', 'text-dark', 'bg-dark', 'text-light');
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                body.classList.add('bg-dark', 'text-light');
                localStorage.setItem('Theme', 'dark');
            } else {
                body.classList.add('bg-light', 'text-dark');
                localStorage.setItem('Theme', 'light');
            }
            themeToggleLink.textContent = '(Theme: auto)';
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        const savedTheme = localStorage.getItem('Theme') || 'auto';
        if (savedTheme === 'light') {
            body.classList.add('bg-light', 'text-dark');
            themeToggleLink.textContent = '(Theme: light)';
        } else if (savedTheme === 'dark') {
            body.classList.add('bg-dark', 'text-light');
            themeToggleLink.textContent = '(Theme: dark)';
        } else {
            toggleTheme();
        }
    });

    themeToggleLink.addEventListener('click', function(event) {
        event.preventDefault();
        toggleTheme();
    });

    document.getElementById('currentYear').textContent = new Date().getFullYear();
    $(document).ready(function() {
        $('#menu-toggle').click(function(e) {
            e.preventDefault();
            $('#wrapper').toggleClass('toggled');
        });
    });