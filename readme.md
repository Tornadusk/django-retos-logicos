# Retos Lógico Matemáticos

Sistema web para resolver retos lógicos y matemáticos con sistema de puntuación y ranking.

## Características

- **Sistema de Retos**: Publicación y gestión de acertijos y problemas lógicos
- **Clasificación por Dificultad**: 4 niveles (Fácil, Medio, Difícil, Experto)
- **Sistema de Puntuación**: Puntos basados en dificultad y tiempo de respuesta
- **Ranking de Usuarios**: Clasificación competitiva entre usuarios
- **Dashboard Personal**: Estadísticas y progreso individual
- **Fotos de Perfil**: Sistema completo de avatares con fotos personalizadas y emojis predefinidos
- **Imágenes de Retos**: Los retos pueden tener imágenes personalizadas o iconos temáticos
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

0. **Preparar carpeta y terminal**
   - Windows:
     - Crea una carpeta genérica, por ejemplo: `C:\Proyectos`.
     - Abre CMD/PowerShell y muévete a esa carpeta:
       ```bash
       cd "C:\Proyectos"
       ```
     - Explicado simple: una "carpeta" es un lugar donde guardarás el proyecto. Abre el menú inicio, escribe "cmd" y presiona Enter. Se abrirá una ventana negra (la terminal). Escribe el comando de arriba tal cual y pulsa Enter. Si no existe la carpeta, créala antes en el Explorador.
     - Comprobar que estás dentro: escribe `dir` y pulsa Enter. Verás el listado de archivos de esa carpeta.
   - Linux/Mac:
     - Crea y entra a un directorio de trabajo estándar, por ejemplo `~/projects`:
       ```bash
       mkdir -p ~/projects && cd ~/projects
       ```
     - Explicado simple: abre la aplicación "Terminal". Copia y pega la línea de arriba y pulsa Enter. Crea (si no existe) y entra en una carpeta llamada `projects` dentro de tu carpeta personal.
     - Comprobar que estás dentro: escribe `ls` y pulsa Enter. Verás el listado de archivos de esa carpeta.

   - Si usas Ubuntu/Debian y no tienes Git/Python instalados, ejecútalo primero:
     ```bash
     sudo apt update
     sudo apt install -y git python3 python3-venv python3-pip
     ```

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Tornadusk/django-retos-logicos.git
   cd django-retos-logicos
   ```

   Si no tienes Git, tienes dos alternativas:

   - Alternativa A (sin Git): Descargar ZIP
     1) Abre el repo: https://github.com/Tornadusk/django-retos-logicos
     2) Botón "Code" → "Download ZIP"
     3) Descomprime el ZIP en tu carpeta de trabajo (Windows: C:\Proyectos, Linux/Mac: ~/projects)
     4) Abre la terminal y entra a la carpeta del proyecto descomprimido

   - Alternativa B (instalar Git y clonar)
     - Windows: instala "Git for Windows" y luego ejecuta:
       ```bash
       cd "C:\Proyectos"
       git clone https://github.com/Tornadusk/django-retos-logicos.git
       cd django-retos-logicos
       ```
     - macOS: instala Command Line Tools (xcode-select --install) o Homebrew; con Git disponible:
       ```bash
       cd ~/projects
       git clone https://github.com/Tornadusk/django-retos-logicos.git
       cd django-retos-logicos
       ```
     - Linux (Debian/Ubuntu):
       ```bash
       sudo apt update && sudo apt install -y git
       cd ~/projects
       git clone https://github.com/Tornadusk/django-retos-logicos.git
       cd django-retos-logicos
       ```

2. **Crear entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

   **Importante:** Este proyecto requiere Pillow para manejar imágenes de perfil. Si instalas manualmente:
   ```bash
   # Windows
   pip install Pillow

   # Linux/Mac
   pip3 install Pillow
   ```

   Alternativa rápida (mínima) si solo quieres poner a andar el servidor:
   ```bash
   # Windows
   pip install django Pillow

   # Linux/Mac
   pip3 install django Pillow
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

6. **Cargar datos de ejemplo (opcional – NO es una migración automática)**
   ```bash
   python manage.py loaddata fixtures/datos_ejemplo.json
   ```
   
   - Esto no se ejecuta con `migrate`. Es una fixture y debes cargarla manualmente con `loaddata` si quieres partir con información precargada.
   - Útil para tener retos/categorías/ordenamientos de ejemplo en un entorno nuevo.
   - Recomendado hacerlo sobre una base vacía (recién creada) para evitar duplicados. Si necesitas reiniciar, puedes usar `python manage.py flush` y volver a cargar la fixture.
   
   **Qué incluye la fixture**:
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

### Registro e inicio de sesión (flujo de usuario común)
- **Registro** (`http://127.0.0.1:8000/cuentas/registro/`):
  - Completa nombre, apellido, usuario, email y contraseña.
  - Al enviar, se crea el usuario y se inicia sesión automáticamente.
  - Se crea el `PerfilUsuario` de forma automática (señal post_save) y se actualiza el `Ranking`.
  - Redirección al `Dashboard`.
- **Inicio de sesión** (`http://127.0.0.1:8000/cuentas/login/`):
  - Puedes ingresar con **usuario o email** y contraseña.
  - Muestra mensaje de bienvenida y redirige a `LOGIN_REDIRECT_URL` (Dashboard).
- **Perfil** (`/cuentas/perfil/`):
  - Permite editar nombre, apellido y email del usuario autenticado.
  - Muestra estadísticas (puntuación, retos completados, nivel, fecha registro) y accesos rápidos.
- **Cambio de contraseña** (`/cuentas/cambiar_password/`):
  - Usuarios normales cambian la contraseña desde aquí.
  - Si eres admin (`is_staff`), el cambio se realiza desde el panel de administración (se redirige ahí).
- **Cerrar sesión**: disponible en la barra superior (formulario POST protegido con CSRF en `base/base.html`).

### Para Administradores:
1. **Admin panel**: http://127.0.0.1:8000/admin/
2. **Gestionar retos** desde el panel de administración
3. **Configurar ordenamiento** global en "Configuraciones de Ordenamiento"
4. **Establecer prioridades** individuales en cada reto
5. **Ver estadísticas** del sistema en "Ver Estadísticas"
6. **Generar reportes** en "Ver Reportes"

## Guía del Panel de Administración

### Consejos rápidos de navegación
- En varias listas, puedes hacer clic en determinadas columnas para ir directo a la edición del registro:
  - Users → columna **Username**.
  - Juego → Intentos → columna **Usuario**.
  - Juego → Rankings → columna **Posición**.
  - Retos → Categorías → columna **Nombre**.
  - Retos → Retos → columna **Título**.
- Acciones masivas (Actions): marca los checkboxes, elige la acción en el selector (por ejemplo, "Cambiar número de intentos"), y pulsa **Go**. Verás un indicador tipo "Go 1 of 12 selected" antes de confirmar y aplicar.

### Cuentas (Cuentas → Users y Perfiles de Usuario)
- **Users (CustomUser)**: 
  - **Modelo personalizado**: Usa `cuentas.User` (CustomUser) en lugar del modelo estándar de Django.
  - **Vista de lista**: muestra columnas con puntuación y nivel (desde el perfil) y un botón `Ver` por usuario.
  - **Botón "Ver"**: abre una vista de solo lectura del usuario y su perfil (sin campos editables). Desde ahí puedes ir a `Edit user` si tienes permisos.
  - **Protección de auto-borrado**: el usuario autenticado no puede eliminarse a sí mismo.
  - **Eliminación masiva**: existe la acción personalizada "Eliminar usuarios seleccionados (excluye al usuario actual)", que omite tu propio usuario.
  - **Crear usuario (admin)**: http://127.0.0.1:8000/admin/cuentas/user/add/
  - **Botones de Guardado (Add user y Change user)**:
    - `Save` (Add user): crea el usuario y redirige a la página de edición del usuario recién creado (`.../change/`).
    - `Save and continue editing` (Add user): crea el usuario y también te deja en `.../change/` (mismo destino que `Save` en el alta; comportamiento estándar de Django).
    - `Save and continue editing` (Change user): guarda los cambios y permanece en la misma página de edición para seguir editando.
    - `Save and add another` (Add user): guarda el usuario actual y te abre de inmediato un nuevo formulario en blanco para crear otro usuario.

- **Perfiles de Usuario**:
  - **Lectura principalmente**: el listado es informativo, sin acciones masivas de puntuación.
  - **Altas**: los perfiles se crean automáticamente cuando se crea un usuario. No se permite crear perfiles duplicados.
  - **Edición**: los campos de estadísticas (`puntuacion_total`, `retos_completados`, `fecha_registro`) son de solo lectura. La gestión principal de usuarios se hace desde `Users`.

### Juego (Intentos y Rankings)
- **Intentos**:
  - Vista de lista de intentos de usuarios por reto.
  - Disponible enlace "Add" para registrar intentos manuales si fuese necesario (generalmente no se usa en operación normal porque los intentos se generan desde el front).
  - Búsqueda/filtrado por usuario y reto según configuración del admin.
- **Rankings**:
  - Vista de lista de posiciones, puntuación y retos completados.
  - Solo lectura total (sin Add/Change/Delete en el admin).
  - Acción manual: recálculo de ranking con descripción contextual al pasar el mouse.

### Retos
- **Campo nuevo `ejemplo_entrada`**: guía de formato para la respuesta del usuario (no revela la solución).
- **Botones de autocompletado** en el admin para `ejemplo_entrada` (por ejemplo: "Añadir básicos", "Solo mayúscula", "Solo minúscula").
- **Efectos en puntuaciones**: al borrar un `Reto`, se recalculan automáticamente las puntuaciones y el ranking de los usuarios afectados (señales `pre_delete`/`post_delete`).

### Ranking
- **Solo lectura total**: no se puede añadir/editar/eliminar entradas manualmente.
- **Acción manual disponible**: "Recalcula posiciones y puntajes de todos los usuarios en el ranking." para forzar un recálculo cuando lo necesites.

### Reglas automáticas de actualización
- Al borrar un `Intento`, el perfil del usuario y el `Ranking` se recalculan automáticamente.
- Al borrar un `Reto`, se recalculan los perfiles de usuarios afectados y luego el `Ranking`.

### Datos de ejemplo (fixtures)
- Si quieres ver el panel con datos precargados (categorías, retos, configuraciones), carga la fixture:
  ```bash
  python manage.py loaddata fixtures/datos_ejemplo.json
  ```
  Recomendado sobre una base vacía (o tras `python manage.py flush`). Esto no es una migración y no se ejecuta con `migrate`.

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
3. **Establecer prioridad**: Admin → Retos → editar → sección "Orden y Visibilidad" → campo `orden_prioridad` (número mayor = más arriba). Para ver el efecto, usa el selector "Ordenar por → Prioridad" en la lista de retos o fija el orden por defecto en Admin → Configuraciones de Ordenamiento.
4. **Marcar aleatorio**: Admin → Retos → editar → sección "Orden y Visibilidad" → activar `mostrar_aleatorio` (incluye el reto cuando el orden sea aleatorio y la configuración lo permita).
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

## Sistema de Fotos de Perfil

### Características:
- **Foto personalizada**: Los usuarios pueden subir su propia foto de perfil
- **Avatares predefinidos**: 8 opciones de emojis para elegir
- **Sin foto**: Opción de no tener foto (usa 👤 por defecto)
- **Eliminación**: Los usuarios pueden quitar su foto cuando quieran

### Opciones de avatar:
- 👨 Hombre
- 👩 Mujer  
- 👨‍💼 Profesional
- 👩‍💼 Profesional
- 👨‍🎓 Estudiante
- 👩‍🎓 Estudiante
- 👨‍💻 Desarrollador
- 👩‍💻 Desarrolladora

### Funcionalidades:
- **Validación de archivos**: Solo imágenes (JPG, PNG, GIF) máximo 5MB
- **Vista previa**: Los usuarios pueden ver cómo se verá su avatar antes de guardar
- **Integración completa**: La foto se muestra en navbar, perfil y toda la aplicación
- **Responsive**: Se adapta a diferentes tamaños de pantalla

### URLs relacionadas:
- **Editar foto**: `http://127.0.0.1:8000/cuentas/perfil/editar/`
- **Ver perfil**: `http://127.0.0.1:8000/cuentas/perfil/`

## Sistema de Imágenes para Retos

### Características:
- **Imagen personalizada**: Los administradores pueden subir imágenes relacionadas con cada reto
- **Iconos predefinidos**: 12 opciones de emojis temáticos para elegir
- **Sin imagen**: Si no hay imagen ni icono, se usa 🧩 por defecto
- **Eliminación**: Los administradores pueden quitar la imagen cuando quieran

### Opciones de iconos:
- 🧩 Puzzle
- 🔢 Números
- 🧮 Cálculo
- 🎯 Objetivo
- 💡 Idea
- 🎲 Dados
- 📊 Gráficos
- 🔍 Búsqueda
- ⚡ Rápido
- 🏆 Premio
- 🎨 Arte
- 🌐 Global

### Funcionalidades:
- **Validación de archivos**: Solo imágenes (JPG, PNG, GIF) máximo 5MB
- **Vista previa en admin**: Los administradores pueden ver la imagen en el panel de administración
- **Integración completa**: La imagen se muestra en lista de retos, detalle del reto y dashboard
- **Responsive**: Se adapta a diferentes tamaños de pantalla

### URLs relacionadas:
- **Panel admin**: `http://127.0.0.1:8000/admin/retos/reto/`
- **Lista de retos**: `http://127.0.0.1:8000/retos/`

## Fixtures (Datos de Ejemplo)

### ¿Qué son las fixtures?
Las fixtures son archivos que contienen datos de ejemplo para poblar la base de datos. A diferencia de las **migraciones**, no se aplican automáticamente con `migrate`. Debes cargarlas explícitamente con `loaddata`. Son útiles para:
- Probar el sistema sin crear datos manualmente
- Configurar el sistema con información básica
- Tener datos consistentes entre desarrolladores

### Comandos para fixtures:

#### Cargar datos de ejemplo:
```bash
python manage.py loaddata fixtures/datos_ejemplo.json
```
> Nota: Esto añade registros de ejemplo (categorías, retos, configuraciones). Si ya tenías datos, podrías duplicar entradas; en ese caso reinicia con `python manage.py flush` antes de cargar.

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
