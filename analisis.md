# Análisis del Proyecto ItinerAR - Listado de Mejoras (Actualizado)

## 📊 Resumen del Proyecto

**ItinerAR** es una aplicación web Flask para planificar itinerarios de viaje por Argentina. Permite crear, editar y compartir itinerarios con etapas/días y puntos de interés. Cuenta con 3 roles de usuario (Administrador, Planificador, Visitante) y un panel de datos con gráficos.

---

## 🔴 MEJORAS CRÍTICAS (Alta Prioridad)

### 1. **Validación de Fechas en Etapas**
- **Problema**: Las etapas pueden tener fechas anteriores a la fecha de inicio del itinerario
- **Impacto**: Inconsistencia de datos
- **Solución**:
  - Agregar validación backend en [`app/routes/etapas.py`](app/routes/etapas.py)
  - Validar que `fechaInicio` y `fechaFin` de etapas estén dentro del rango del itinerario
  - Implementar validación frontend en [`templates/etapas/formulario.html`](templates/etapas/formulario.html)

### 2. **Bug en Movimiento de Etapas**
- **Problema**: La funcionalidad de subir/bajar etapas funciona inconsistentemente
- **Impacto**: Experiencia de usuario confusa
- **Solución**:
  - Revisar lógica en [`app/routes/etapas.py`](app/routes/etapas.py) (funciones `subir()` y `bajar()`)
  - Implementar sistema de ordenamiento más robusto (usar campo `orden` en lugar de fechas)
  - Agregar tests unitarios

### 3. **Falta de Validación en Etapas**
- **Problema**: No se valida el campo `idLugarInteres` en la edición
- **Línea problemática**: [`app/routes/etapas.py`](app/routes/etapas.py) línea ~95
- **Solución**:
```python
# Falta esta línea:
id_lugar_interes = request.form.get('idLugarInteres', '').strip()
```

### 4. **Falta Validación de Campos Requeridos**
- **Problema**: No todos los campos están siendo validados en formularios
- **Impacto**: Datos incompletos o inválidos en base de datos
- **Solución**:
  - Validar que título, descripción y fechas sean obligatorios
  - Validar longitud mínima y máxima de textos
  - Implementar validaciones consistentes en todos los formularios

---

## 🟠 MEJORAS IMPORTANTES (Prioridad Media-Alta)

### 5. **Sistema de Registro de Usuarios**
- **Estado**: No existe funcionalidad de registro
- **Solución**:
  - Crear ruta `/auth/register` con validaciones
  - Crear template `templates/auth/register.html`
  - Validar email único, contraseña fuerte
  - Asignar rol por defecto: "Visitante"
  - Incluir confirmación de email (opcional)

### 6. **Perfil de Usuario**
- **Estado**: Botón "Mi Perfil" no funciona
- **Solución**:
  - Crear ruta `/auth/perfil` 
  - Crear template `templates/auth/perfil.html`
  - Permitir editar nombre, apellido, email
  - Opción de cambiar contraseña
  - Vista de itinerarios personales

### 7. **Datos CSV Incompletos**
- **Problema**: Los archivos CSV en [`data/`](data/) son de prueba e incompletos
- **Solución**:
  - Descargar datasets reales de [datos.gob.ar](https://datos.gob.ar)
  - O completar y validar los CSV existentes
  - Crear script de validación de datos
  - **Archivos afectados**:
    - `data/parques_nacionales.csv`
    - `data/alojamientos.csv`
    - `data/fiestas_eventos.csv`
    - `data/rangos_edad.csv`
    - `data/turismo_receptivo.csv`
    - Falta: Provincias y Ciudades completos

### 8. **Falta Base de Datos de Provincias y Ciudades**
- **Problema**: Solo hay datos de prueba en [`init_db.py`](init_db.py)
- **Solución**:
  - Crear `data/provincias_ciudades.csv` completo con todas las provincias y ciudades
  - Script para cargar provincias y ciudades argentinas
  - O crear archivo JSON con estructura jerárquica provincia → ciudades
  - Validar que los datos sean consistentes

### 9. **Formato de Fechas**
- **Problema**: Las fechas están en formato ISO (YYYY-MM-DD) pero deberían mostrarse DD/MM/AAAA
- **Solución**:
  - Crear filtro Jinja2 para formateo de fechas: `{{ fecha | format_date }}`
  - Mantener BD en ISO pero mostrar formateado en templates
  - Aplicar a todas las vistas que muestren fechas

### 10. **Manejo de Errores Inconsistente**
- **Problema**: No hay logging de errores, manejo inconsistente de excepciones
- **Solución**:
  - Implementar logging con módulo `logging`
  - Crear archivo `app/utils/logger.py`
  - Crear clase personalizada para excepciones
  - Registrar errores en archivo `logs/app.log`
  - Mostrar mensajes amigables al usuario

---

## 🟡 MEJORAS IMPORTANTES (Prioridad Media)

### 11. **Seguridad: Contraseñas por Defecto**
- **Problema**: `DEFAULT_PASSWORD` en [`.env`](.env) es débil ("password123")
- **Solución**:
  - Generar contraseñas aleatorias fuertes para usuarios de prueba
  - Crear validador de contraseña fuerte en registro (min 8 caracteres, mayús, números)
  - Documentar requisitos de seguridad

### 12. **Falta de Paginación**
- **Problema**: Las vistas de lugares e itinerarios cargan todos los registros
- **Solución**:
  - Implementar paginación con `flask_paginate`
  - Límite de 20-50 items por página
  - Afecta: rutas en [`app/routes/itinerarios.py`](app/routes/itinerarios.py) y [`app/routes/lugares.py`](app/routes/lugares.py)
  - Agregar controles de navegación

### 13. **Tests Unitarios y de Integración**
- **Estado**: No existen tests
- **Solución**:
  - Crear directorio `tests/` con estructura:
    - `tests/test_modelos.py`
    - `tests/test_rutas.py`
    - `tests/test_utilidades.py`
    - `tests/conftest.py` (fixtures)
  - Usar `pytest`
  - Cobertura mínima 70%

### 14. **Falta Documentación de API**
- **Problema**: Endpoints no documentados
- **Solución**:
  - Agregar docstrings a todos los endpoints
  - Crear archivo `API.md` con documentación
  - Considerar Swagger/OpenAPI (via `flask_restx` o `flasgger`)
  - Documentar parámetros, respuestas, códigos de error

### 15. **Consistencia en Nombres de Variables**
- **Problema**: Mix de camelCase (`idUsuario`, `idLugar`) y snake_case (`user_id`)
- **Solución**:
  - Estandarizar a snake_case en Python
  - Mantener camelCase solo en base de datos/JSON
  - Refactorizar gradualmente
  - Crear documento de convenciones de código

### 16. **Validación en Frontend Débil**
- **Problema**: Poca validación JavaScript antes de enviar
- **Solución**:
  - Mejorar validaciones HTML5 en formularios
  - Agregar JavaScript para verificar:
    - Longitud de caracteres
    - Formato de email
    - Fechas válidas
  - Feedback visual en tiempo real

### 17. **Seguridad CSRF**
- **Problema**: Implementación de CSRF parece incompleta
- **Solución**:
  - Verificar tokens CSRF en todos los formularios
  - Usar [`Flask-WTF`](https://flask-wtf.readthedocs.io/) para manejo robusto
  - Asegurar que todos los `<form>` tengan `{{ csrf_token() }}`

### 18. **Falta de Búsqueda y Filtros Avanzados**
- **Problema**: Búsqueda de itinerarios muy básica
- **Solución**:
  - Agregar filtros: por fecha, provincia, cantidad etapas, autor
  - Búsqueda full-text en descripción y título
  - Interfaz de filtros mejorada
  - Considerar Elasticsearch para búsqueda muy avanzada

### 19. **Falta de Exportación de Itinerarios**
- **Problema**: No hay opción de descargar/exportar
- **Solución**:
  - Exportar a PDF (usando `weasyprint` o `reportlab`)
  - Exportar a iCalendar (`.ics`) para importar a calendarios
  - Exportar a JSON
  - Agregar botones en vista de itinerario

### 20. **Imágenes y Recursos Visuales**
- **Problema**: Falta imagen alusiva en home, sin fotos de lugares
- **Solución**:
  - Agregar imagen turismo en [`templates/index.html`](templates/index.html)
  - Agregar fotos de lugares de interés (vía API, Unsplash o uploads)
  - Usar CDN para optimizar carga
  - Optimizar peso de imágenes

---

## 🔵 MEJORAS OPCIONALES (Prioridad Baja)

### 21. **Comentarios en Itinerarios**
- Agregar sistema de comentarios/reseñas en itinerarios públicos

### 22. **Valoraciones (Stars)**
- Sistema de valoración 5 estrellas para itinerarios

### 23. **Favoritos**
- Permitir marcar itinerarios como favoritos
- Vista de itinerarios guardados

### 24. **Compartir en Redes**
- Botones para compartir itinerarios en redes sociales

### 25. **Mapas Interactivos**
- Integrar Leaflet o Google Maps para visualizar etapas geográficamente

### 26. **Notificaciones**
- Sistema de notificaciones por email o in-app para cambios

### 27. **Modo Oscuro**
- Tema oscuro/claro switcheable con persistencia

### 28. **Histórico de Cambios**
- Auditoría de cambios en itinerarios

### 29. **Colaboración en Tiempo Real**
- Múltiples usuarios editando mismo itinerario simultáneamente

### 30. **Mobile App**
- Versión nativa iOS/Android o PWA (Progressive Web App)

---

## 📋 TABLA DE PRIORIDADES

| # | Mejora | Prioridad | Esfuerzo | Impacto |
|---|--------|-----------|----------|---------|
| 1 | Validación de fechas | 🔴 Crítica | Bajo | Alto |
| 2 | Fix movimiento etapas | 🔴 Crítica | Medio | Alto |
| 3 | Fix validación etapas | 🔴 Crítica | Bajo | Alto |
| 4 | Validación campos | 🔴 Crítica | Medio | Alto |
| 5 | Sistema registro | 🟠 Alta | Medio | Alto |
| 6 | Perfil usuario | 🟠 Alta | Bajo | Medio |
| 7 | Datos CSV reales | 🟠 Alta | Alto | Alto |
| 8 | DB provincias/ciudades | 🟠 Alta | Medio | Alto |
| 9 | Formato fechas DD/MM | 🟠 Alta | Bajo | Medio |
| 10 | Logging y errores | 🟠 Alta | Medio | Medio |
| 11 | Seguridad contraseñas | 🟡 Media | Bajo | Alto |
| 12 | Paginación | 🟡 Media | Medio | Bajo |
| 13 | Tests | 🟡 Media | Alto | Alto |
| 14 | Documentación API | 🟡 Media | Medio | Medio |
| 15 | Consistencia nombres | 🟡 Media | Alto | Bajo |
| 16 | Validación Frontend | 🟡 Media | Medio | Medio |
| 17 | Seguridad CSRF | 🟡 Media | Bajo | Alto |
| 18 | Búsqueda avanzada | 🟡 Media | Alto | Medio |
| 19 | Exportación | 🟡 Media | Medio | Medio |
| 20 | Imágenes/visuales | 🟡 Media | Medio | Bajo |

---

## 🎯 Plan de Acción Recomendado

### **Fase 1: Bugs Críticos**
- [] #1 - Validación de fechas en etapas
- [] #2 - Fix movimiento etapas
- [] #3 - Fix validación campos etapas
- [] #4 - Validación campos requeridos

### **Fase 2: Features Esenciales**
- [] #5 - Sistema de registro
- [] #6 - Perfil de usuario
- [] #9 - Formato de fechas DD/MM
- [] #10 - Logging y manejo de errores

### **Fase 3: Datos y Búsqueda**
- [] #8 - Base de datos provincias/ciudades
- [] #7 - Datos CSV completados
- [] #18 - Búsqueda y filtros avanzados

### **Fase 4: Calidad y Seguridad**
- [] #11 - Validación de contraseñas
- [] #17 - Seguridad CSRF mejorada
- [] #13 - Tests unitarios
- [] #15 - Consistencia de nombres

### **Fase 5: Polish y Features Opcionales**
- [] #12 - Paginación
- [] #14 - Documentación API
- [] #19 - Exportación
- [] #20 - Imágenes/visuales
- [] Features opcionales según prioridad