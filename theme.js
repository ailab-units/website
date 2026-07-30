(function(){
  const root = document.documentElement;
  const stored = localStorage.getItem('ailab-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = stored || (prefersDark ? 'dark' : 'light');
  if (initial === 'dark') root.setAttribute('data-theme', 'dark');

  window.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    const setIcon = () => {
      btn.textContent = root.getAttribute('data-theme') === 'dark' ? '☀' : '●';
    };
    setIcon();
    btn.addEventListener('click', () => {
      const isDark = root.getAttribute('data-theme') === 'dark';
      if (isDark) {
        root.removeAttribute('data-theme');
        localStorage.setItem('ailab-theme', 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('ailab-theme', 'dark');
      }
      setIcon();
    });
  });
})();
