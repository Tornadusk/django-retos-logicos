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

7. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## Uso

1. **Acceder al sitio**: http://127.0.0.1:8000/
2. **Admin panel**: http://127.0.0.1:8000/admin/
3. **Registrar usuario** y comenzar a resolver retos
4. **Gestionar retos** desde el panel de administración

## Modelo de Datos

### Entidades Principales:
- **Usuario**: Perfil extendido con puntuación y estadísticas
- **Reto**: Acertijos con dificultad, categoría y puntos
- **Intento**: Respuestas de usuarios con puntuación
- **Ranking**: Clasificación de usuarios por puntuación

### Relaciones:
- Usuario 1:N Intento
- Reto 1:N Intento
- Categoría 1:N Reto

## Tecnologías

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5, Font Awesome
- **Base de datos**: SQLite (desarrollo)
- **Python**: 3.8+

## Funcionalidades

### Para Usuarios:
- Registro e inicio de sesión
- Dashboard personal con estadísticas
- Lista de retos con filtros
- Sistema de puntuación
- Ranking global

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

## Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
