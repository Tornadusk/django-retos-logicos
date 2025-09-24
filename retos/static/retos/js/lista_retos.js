/**
 * JavaScript para la lista de retos - VERSIÓN 2
 * Maneja el filtrado y la limpieza de filtros
 */

console.log('=== CARGANDO LISTA RETOS JS V2 ===');

// Función para limpiar filtros - VERSIÓN SIMPLE
function limpiarFiltros() {
    console.log('=== LIMPIANDO FILTROS V2 ===');
    
    // Redirigir directamente a la URL limpia
    const currentOrigin = window.location.origin;
    const retosUrl = currentOrigin + '/retos/';
    
    console.log('URL actual:', window.location.href);
    console.log('URL destino:', retosUrl);
    
    // Usar replace para no crear entrada en el historial
    window.location.replace(retosUrl);
}

// Event listeners cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOM CARGADO - V2 ===');
    
    // Verificar que los botones existen
    const btnLimpiar = document.getElementById('btn-limpiar');
    const btnLimpiarTodos = document.getElementById('btn-limpiar-todos');
    
    console.log('Botón limpiar encontrado:', !!btnLimpiar);
    console.log('Botón limpiar todos encontrado:', !!btnLimpiarTodos);
    
    // NO agregar event listeners adicionales
    // Los botones ya tienen onclick="limpiarFiltros()"
});

// Función para mostrar/ocultar filtros avanzados
function toggleFiltrosAvanzados() {
    const filtrosAvanzados = document.getElementById('filtros-avanzados');
    if (filtrosAvanzados) {
        filtrosAvanzados.style.display = filtrosAvanzados.style.display === 'none' ? 'block' : 'none';
    }
}
