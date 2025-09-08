/**
 * JavaScript para la lista de retos
 * Maneja el filtrado automático y la limpieza de filtros
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-filtrar cuando cambien los selects
    const dificultadSelect = document.getElementById('dificultad');
    const categoriaSelect = document.getElementById('categoria');
    const ordenSelect = document.getElementById('orden');
    
    function autoFiltrar() {
        // Crear un pequeño delay para evitar múltiples requests
        setTimeout(() => {
            document.querySelector('form').submit();
        }, 300);
    }
    
    if (dificultadSelect) {
        dificultadSelect.addEventListener('change', autoFiltrar);
    }
    
    if (categoriaSelect) {
        categoriaSelect.addEventListener('change', autoFiltrar);
    }
    
    if (ordenSelect) {
        ordenSelect.addEventListener('change', autoFiltrar);
    }
    
    // Para el campo de búsqueda, usar debounce
    const busquedaInput = document.getElementById('busqueda');
    let busquedaTimeout;
    
    if (busquedaInput) {
        busquedaInput.addEventListener('input', function() {
            clearTimeout(busquedaTimeout);
            busquedaTimeout = setTimeout(() => {
                document.querySelector('form').submit();
            }, 1000); // Esperar 1 segundo después de que el usuario deje de escribir
        });
    }
});

// Función para limpiar filtros
function limpiarFiltros() {
    document.getElementById('busqueda').value = '';
    document.getElementById('dificultad').value = '';
    document.getElementById('categoria').value = '';
    document.getElementById('orden').value = 'fecha';
    document.querySelector('form').submit();
}

// Función para mostrar/ocultar filtros avanzados
function toggleFiltrosAvanzados() {
    const filtrosAvanzados = document.getElementById('filtros-avanzados');
    if (filtrosAvanzados) {
        filtrosAvanzados.style.display = filtrosAvanzados.style.display === 'none' ? 'block' : 'none';
    }
}
