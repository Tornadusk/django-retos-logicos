# Retos Lógico Matemáticos

Sistema web para resolver retos lógicos y matemáticos con sistema de puntuación y ranking.

## Características

- **Sistema de Retos**: Publicación y gestión de acertijos y problemas lógicos
- **Clasificación por Dificultad**: 4 niveles (Fácil, Medio, Difícil, Experto)
- **Sistema de Puntuación**: Puntos basados en dificultad y tiempo de respuesta
- **Ranking de Usuarios**: Clasificación competitiva entre usuarios
- **Dashboard Personal**: Estadísticas y progreso individual
- **Admin Panel**: Gestión completa de retos y usuarios

## Estructura del Proyecto

```
RetosLógicoMatemáticos/
├── retos/           # App principal - vistas de home, dashboard, lista de retos
├── juego/           # Lógica de puntuación, intentos y ranking
├── cuentas/         # Login/registro y perfil de usuario
├── proyect/         # Configuración del proyecto Django
└── fixtures/        # Datos de ejemplo
```

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd RetosLógicoMatemáticos
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Cargar datos de ejemplo (opcional)**
   ```bash
   python manage.py loaddata fixtures/datos_ejemplo.json
   ```
   
   **Nota**: Los datos de ejemplo incluyen:
   - 6 categorías de retos (Lógica, Matemáticas, Secuencias, etc.)
   - 12 retos con diferentes dificultades
   - 3 configuraciones de ordenamiento
   - Datos para probar todas las funcionalidades

7. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## Uso

### Para Usuarios:
1. **Acceder al sitio**: http://127.0.0.1:8000/
2. **Registrar usuario** y comenzar a resolver retos
3. **Usar filtros** en la lista de retos para encontrar retos específicos
4. **Cambiar ordenamiento** usando el selector "Ordenar por"
5. **Ver estadísticas** en el dashboard personal

### Para Administradores:
1. **Admin panel**: http://127.0.0.1:8000/admin/
2. **Gestionar retos** desde el panel de administración
3. **Configurar ordenamiento** global en "Configuraciones de Ordenamiento"
4. **Establecer prioridades** individuales en cada reto
5. **Ver estadísticas** del sistema en "Ver Estadísticas"
6. **Generar reportes** en "Ver Reportes"

### Configuración del Sistema de Ordenamiento:

#### Como Admin:
1. **Ir a**: Admin → Configuraciones de Ordenamiento
2. **Crear/Editar** configuración activa
3. **Elegir orden por defecto**: fecha, dificultad, puntos, prioridad, popularidad, aleatorio
4. **Configurar paginación**: número de retos por página
5. **Activar configuración**: solo una puede estar activa

#### Configurar retos individuales:
1. **Ir a**: Admin → Retos
2. **Editar reto** específico
3. **Establecer prioridad**: número mayor = más arriba
4. **Marcar aleatorio**: para mostrar en orden aleatorio
5. **Guardar cambios**

#### Como Usuario:
1. **Ir a**: Lista de Retos
2. **Usar filtros**: dificultad, categoría, búsqueda
3. **Cambiar ordenamiento**: selector "Ordenar por"
4. **Ver indicadores**: badges de prioridad y aleatorio

## Modelo de Datos

### Entidades Principales:
- **Usuario**: Perfil extendido con puntuación y estadísticas
- **Reto**: Acertijos con dificultad, categoría y puntos
- **Intento**: Respuestas de usuarios con puntuación
- **Ranking**: Clasificación de usuarios por puntuación
- **Categoría**: Clasificación de retos por tipo
- **ConfiguracionOrdenamiento**: Control del orden de visualización

### Relaciones:
- Usuario 1:N Intento
- Reto 1:N Intento
- Categoría 1:N Reto
- Usuario 1:1 PerfilUsuario

## Sistema de Ordenamiento

### Características:
- **Ordenamiento configurable**: El admin puede elegir cómo se muestran los retos
- **Prioridad individual**: Cada reto puede tener una prioridad específica
- **Modo aleatorio**: Retos que se muestran en orden aleatorio
- **Filtros de usuario**: Los usuarios pueden cambiar el ordenamiento

### Opciones de ordenamiento:
- **Por fecha**: Más recientes primero
- **Por dificultad**: Fácil → Medio → Difícil → Experto
- **Por puntos**: Más puntos primero
- **Por prioridad**: Según configuración del admin
- **Por popularidad**: Más intentos primero
- **Aleatorio**: Orden completamente aleatorio

## Fixtures (Datos de Ejemplo)

### ¿Qué son las fixtures?
Las fixtures son archivos que contienen datos de ejemplo para poblar la base de datos. Son útiles para:
- Probar el sistema sin crear datos manualmente
- Configurar el sistema con información básica
- Tener datos consistentes entre desarrolladores

### Comandos para fixtures:

#### Cargar datos de ejemplo:
```bash
python manage.py loaddata fixtures/datos_ejemplo.json
```

#### Crear nuevas fixtures:
```bash
python manage.py dumpdata retos > fixtures/retos_completos.json
python manage.py dumpdata juego > fixtures/juego_completo.json
python manage.py dumpdata cuentas > fixtures/cuentas_completo.json
```

#### Limpiar y recargar datos:
```bash
python manage.py flush
python manage.py loaddata fixtures/datos_ejemplo.json
```

#### Exportar datos específicos:
```bash
python manage.py dumpdata retos.reto --indent 2 > fixtures/retos_exportados.json
python manage.py dumpdata retos.categoria --indent 2 > fixtures/categorias_exportadas.json
```

### Contenido de datos_ejemplo.json:
- **6 categorías**: Lógica Básica, Matemáticas, Secuencias, Geometría, Problemas de Palabras, Optimización
- **12 retos**: Con diferentes dificultades y configuraciones de ordenamiento
- **3 configuraciones**: De ordenamiento (Principal, Aleatorio, Por Dificultad)
- **Datos de prueba**: Para probar todas las funcionalidades del sistema

## Archivos Estáticos

### Estructura de archivos estáticos:
```
retos/static/retos/
├── css/
│   ├── retos.css          # Estilos generales de la app retos
│   └── dificultad.css     # Colores específicos para badges de dificultad
└── js/
    └── lista_retos.js     # Filtros automáticos y funcionalidad JavaScript

juego/static/juego/
└── css/
    └── juego.css          # Estilos para la app juego

cuentas/static/cuentas/
└── css/
    └── cuentas.css        # Estilos para la app cuentas
```

### Características de los archivos estáticos:
- **CSS modular**: Cada app tiene sus propios estilos
- **JavaScript organizado**: Lógica separada en archivos específicos
- **Colores consistentes**: Sistema de colores unificado para dificultades
- **Responsive**: Diseño adaptable a diferentes tamaños de pantalla

## Tecnologías

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5, Font Awesome
- **Base de datos**: SQLite (desarrollo)
- **Python**: 3.8+
- **JavaScript**: Filtros automáticos y interactividad
- **CSS**: Estilos personalizados para badges y dificultades

## Interfaz de Usuario

### Características Visuales:
- **Badges de Categoría**: Colores distintivos para cada tipo de reto
- **Badges de Dificultad**: 
  - 🟢 **Fácil**: Verde (#28a745)
  - 🟡 **Medio**: Amarillo (#ffc107) 
  - 🟠 **Difícil**: Naranja (#fd7e14)
  - 🔴 **Experto**: Rojo (#dc3545)
- **Badges de Puntos**: Azul con icono de estrella
- **Indicadores Especiales**: 
  - ⭐ **Prioridad**: Badge amarillo para retos prioritarios
  - 🔀 **Aleatorio**: Badge verde para retos aleatorios

### Filtros Automáticos:
- **Sin botones**: Los filtros se aplican automáticamente
- **Búsqueda inteligente**: Filtra 1 segundo después de escribir
- **Indicadores visuales**: Muestra qué filtros están activos
- **Limpieza fácil**: Botón para resetear todos los filtros

## Funcionalidades

### Para Usuarios:
- Registro e inicio de sesión
- Dashboard personal con estadísticas
- Lista de retos con filtros automáticos
- Sistema de puntuación
- Ranking global
- **Filtros automáticos**: Los filtros se aplican automáticamente al cambiar valores
- **Badges visuales**: Categoría, dificultad y puntos claramente identificados
- **Colores por dificultad**: Verde (Fácil), Amarillo (Medio), Naranja (Difícil), Rojo (Experto)

### Para Administradores:
- Gestión completa de retos
- Administración de usuarios
- Estadísticas del sistema
- Panel de control Django

## Estructura de Apps

### retos/
- `home()`: Página principal
- `dashboard()`: Panel del usuario
- `ListaRetosView`: Lista con filtros
- `DetalleRetoView`: Vista detallada del reto
- `intentar_reto()`: Procesar respuestas

### juego/
- `RankingView`: Clasificación de usuarios
- `mis_estadisticas()`: Estadísticas personales
- `progreso_global()`: Estadísticas generales

### cuentas/
- `registro()`: Registro de usuarios
- `perfil()`: Gestión de perfil
- `cambiar_password()`: Cambio de contraseña

## Comandos Útiles

### Desarrollo:
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Limpiar base de datos
python manage.py flush
```

### Fixtures:
```bash
# Cargar datos de ejemplo
python manage.py loaddata fixtures/datos_ejemplo.json

# Exportar datos actuales
python manage.py dumpdata --indent 2 > fixtures/backup_completo.json

# Exportar solo retos
python manage.py dumpdata retos --indent 2 > fixtures/retos_backup.json

# Exportar solo usuarios
python manage.py dumpdata auth.User --indent 2 > fixtures/usuarios_backup.json
```

### Troubleshooting:
```bash
# Si hay errores de migración
python manage.py migrate --fake-initial

# Si hay problemas con fixtures
python manage.py flush
python manage.py loaddata fixtures/datos_ejemplo.json

# Verificar estado de la base de datos
python manage.py showmigrations

# Resetear base de datos completamente
rm db.sqlite3
python manage.py migrate
python manage.py loaddata fixtures/datos_ejemplo.json
```

## Mejoras Implementadas

### Sistema de Ordenamiento:
- ✅ **Configuración global**: Admin puede elegir orden por defecto
- ✅ **Prioridad individual**: Cada reto puede tener prioridad específica
- ✅ **Modo aleatorio**: Retos que se muestran aleatoriamente
- ✅ **Filtros automáticos**: Sin necesidad de presionar botones

### Interfaz Visual:
- ✅ **Badges de dificultad**: Colores específicos por nivel
- ✅ **Iconos descriptivos**: Señales, estrellas, aleatorio
- ✅ **Espaciado mejorado**: Mejor organización visual
- ✅ **Indicadores activos**: Muestra filtros aplicados

### Archivos Estáticos:
- ✅ **JavaScript modular**: `lista_retos.js` para filtros
- ✅ **CSS específico**: `dificultad.css` para colores
- ✅ **Organización**: Cada app con sus archivos estáticos
- ✅ **Mantenibilidad**: Código separado y organizado

## Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
