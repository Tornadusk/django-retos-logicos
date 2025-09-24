(function() {
  function ready(fn) {
    if (document.readyState !== 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  ready(function() {
    var textarea = document.getElementById('id_ejemplo_entrada');
    if (!textarea) return;

    // Crear contenedor de botones
    var container = document.createElement('div');
    container.style.margin = '6px 0 12px 0';

    function addButton(label, content) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'button';
      btn.style.marginRight = '6px';
      btn.textContent = label;
      btn.addEventListener('click', function() {
        var sep = textarea.value && !textarea.value.endsWith('\n') ? '\n' : '';
        textarea.value = textarea.value + sep + content;
      });
      container.appendChild(btn);
    }

    addButton('Añadir básicos', 'Mayúscula\nMinúscula\nJunto separado');
    addButton('Solo mayúscula', 'Mayúscula');
    addButton('Solo minúscula', 'Minúscula');

    // Insertar el contenedor antes del textarea
    textarea.parentNode.insertBefore(container, textarea);
  });
})();


