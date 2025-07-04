 // Función para aplicar el modo según preferencia guardada
  function applyTheme(isDark) {
    if (isDark) {
      document.body.classList.add('dark-mode');
      document.getElementById('darkModeSwitch').checked = true;
      document.getElementById('darkModeLabel').textContent = '☀️';
    } else {
      document.body.classList.remove('dark-mode');
      document.getElementById('darkModeSwitch').checked = false;
      document.getElementById('darkModeLabel').textContent = '🌙';
    }
  }

  // Al cargar la página, aplica el tema guardado
  document.addEventListener('DOMContentLoaded', function() {
    const isDark = localStorage.getItem('darkMode') === 'true';
    applyTheme(isDark);

    document.getElementById('darkModeSwitch').addEventListener('change', function() {
      const isChecked = this.checked;
      localStorage.setItem('darkMode', isChecked);
      applyTheme(isChecked);
    });
  });