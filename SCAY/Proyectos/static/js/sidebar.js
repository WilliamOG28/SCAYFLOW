// Sidebar toggle and active state logic

document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.querySelector('.menu-toggle');
    const links = sidebar.querySelectorAll('a');

    // Toggle sidebar collapsed/expanded
    menuToggle.addEventListener('click', function () {
        const isMobile = window.innerWidth <= 700;
        if (isMobile) {
            sidebar.classList.toggle('open');
        } else {
            sidebar.classList.toggle('collapsed');
        }
    });

    // Active state for sidebar links
    links.forEach(link => {
    link.addEventListener('click', function (e) {
    // Solo prevenir el default si el href es '#'
    if (this.getAttribute('href') === '#') {
    e.preventDefault();
    }
    links.forEach(l => l.classList.remove('selected'));
    this.classList.add('selected');
    });
    });

    // Cierra el sidebar en móvil al hacer click fuera
    document.addEventListener('click', function (e) {
        if (window.innerWidth <= 700 && sidebar.classList.contains('open')) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    });
});
