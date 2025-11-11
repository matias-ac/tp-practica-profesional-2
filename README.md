# ItinerAR - Planificador Colaborativo de Itinerarios

Un sitio web donde los usuarios pueden crear y gestionar sus propios itinerarios de viaje por Argentina.

## Descripción del Proyecto

"ItinerAR" es una aplicación web colaborativa para planificar itinerarios de viaje por Argentina. Los usuarios pueden:

- Consultar información de datasets públicos (Parques Nacionales, Alojamientos, Fiestas Nacionales)
- Crear nuevos itinerarios y agregar etapas/días con puntos de interés
- Modificar itinerarios, cambiar orden de etapas, editar notas
- Eliminar etapas o itinerarios completos

## Tipos de Usuarios

- **Administrador**: Acceso completo (crear, editar, borrar, ver todo).
- **Planificador**: Puede crear y gestionar sus propios itinerarios y etapas.
- **Visitante**: Solo puede ver itinerarios públicos y panel con gráficos informativos.

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: SQLite con SQLAlchemy
- **Autenticación**: Flask-Login
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Análisis de Datos**: Pandas
- **Gráficos**: Chart.js

## Instalación y Configuración

### Paso 1: Clonar o navegar al proyecto

```bash
cd <ruta-del-proyecto>
```

### Paso 2: Crear entorno virtual de Python

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y cambiar la SECRET_KEY (opcional, hay una por defecto)
# Puedes generar una clave secreta con:
# python -c "import secrets; print(secrets.token_hex(32))"
```

### Paso 5: Inicializar la base de datos

```bash
python init_db.py
```

Este script:

- Crea todas las tablas en la base de datos
- Crea los roles (Administrador, Planificador, Visitante)
- Crea usuarios de prueba:
  - **Admin**: `admin@itinerar.com` / definir el valor de `DEFAULT_PASSWORD` en el archivo `.env`
  - **Planificador**: `planificador@itinerar.com` / definir el valor de `DEFAULT_PASSWORD` en el archivo `.env`
  - **Visitante**: `visitante@itinerar.com` / definir el valor de `DEFAULT_PASSWORD` en el archivo `.env`
- Crea algunas provincias y ciudades de ejemplo
- Crea un itinerario de ejemplo

### Paso 6: Ejecutar la aplicación

```bash
python app.py
```

O usando Flask CLI:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

La aplicación estará disponible en: `http://localhost:5001`

O especificando el puerto:

```bash
flask run --port 8000 --debug
```

La aplicación estará disponible en: `http://localhost:8000`

## Modelo de Datos

El proyecto utiliza las siguientes entidades principales:

- **Usuario**: Usuarios del sistema con roles (Administrador, Planificador, Visitante)
- **Rol**: Roles de usuario
- **Itinerario**: Planes de viaje creados por usuarios
- **Etapa**: Días/etapas dentro de un itinerario
- **Ciudad**: Ciudades de Argentina
- **Provincia**: Provincias de Argentina
- **Aeropuerto**: Aeropuertos asociados a ciudades
- **ParqueNacional**: Parques nacionales asociados a provincias
