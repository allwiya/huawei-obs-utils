# 👨‍💻 Guía del Operador - Windows

## 👤 Perfil del Operador

**Nivel de Acceso**: STANDARD (Nivel 2)  
**Responsabilidades**: Gestión diaria de archivos, operaciones de archivo y restauración  
**Riesgo**: Medio  

## 🚀 Inicio Rápido

### Requisitos Previos
- Windows 10/11
- Python 3.8 o superior
- Acceso a credenciales de Huawei Cloud OBS
- Contraseña de operador proporcionada por el administrador

### Primera Configuración
```cmd
# Abrir Command Prompt o PowerShell
cd C:\obs-utils

# Verificar instalación
python obs_utils_improved.py --version

# Configurar credenciales (primera vez)
python obs_utils_improved.py --create-config
```

## 📋 Operaciones Diarias

### 🔍 Operaciones de Consulta (Sin contraseña requerida)

#### Listar Objetos
```cmd
# Listar todos los objetos en un bucket
python obs_utils_improved.py --operation list --bucket mi-bucket

# Listar con filtro por prefijo
python obs_utils_improved.py --operation list --bucket mi-bucket --prefix "reportes/"

# Listar con límite de resultados
python obs_utils_improved.py --operation list --bucket mi-bucket --max-keys 100
```

#### Buscar Archivos
```cmd
# Buscar archivos por nombre
python obs_utils_improved.py --operation search --search-text "backup"

# Buscar en bucket específico
python obs_utils_improved.py --operation search --bucket mi-bucket --search-text "2025"

# Buscar con filtros avanzados
python obs_utils_improved.py --operation search --search-text "reporte" --file-type "pdf"
```

#### Descargar Archivos
```cmd
# Descargar archivo específico
python obs_utils_improved.py --operation download --bucket mi-bucket --key "reportes/reporte_2025.pdf"

# Descargar múltiples archivos con prefijo
python obs_utils_improved.py --operation download --bucket mi-bucket --prefix "reportes/" --local-path "C:\Descargas"

# Descargar con verificación de integridad
python obs_utils_improved.py --operation download --bucket mi-bucket --key "archivo.zip" --verify-checksum
```

### 🗄️ Operaciones de Archivo (Requiere contraseña de operador)

#### Archivar a Almacenamiento COLD
```cmd
# Archivar archivos antiguos (más económico)
python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "archivos-2024/"

# Archivar con filtro de fecha
python obs_utils_improved.py --operation archive --bucket mi-bucket --older-than "90 days"

# Archivar archivos específicos
python obs_utils_improved.py --operation archive --bucket mi-bucket --file-list "lista_archivos.txt"
```

#### Mover a Almacenamiento WARM
```cmd
# Mover a almacenamiento de acceso infrecuente
python obs_utils_improved.py --operation warm --bucket mi-bucket --prefix "documentos-antiguos/"

# Mover archivos por tamaño
python obs_utils_improved.py --operation warm --bucket mi-bucket --larger-than "100MB"
```

#### Restaurar Archivos Archivados
```cmd
# Restaurar archivos desde COLD storage
python obs_utils_improved.py --operation restore --bucket mi-bucket --prefix "archivos-2024/"

# Restaurar con prioridad expedita (más costoso pero más rápido)
python obs_utils_improved.py --operation restore --bucket mi-bucket --key "archivo_urgente.pdf" --tier expedited

# Restaurar con prioridad estándar
python obs_utils_improved.py --operation restore --bucket mi-bucket --prefix "reportes/" --tier standard
```

## 🖥️ Modo Interactivo

### Iniciar Modo Interactivo
```cmd
# Modo interactivo completo
python obs_utils_improved.py

# Modo interactivo con bucket predeterminado
python obs_utils_improved.py --bucket mi-bucket-principal
```

### Navegación en Modo Interactivo
```
=== OBS Utils - Modo Interactivo ===

Seleccione una operación:
1. 📋 Listar objetos
2. 🔍 Buscar archivos
3. ⬇️  Descargar archivos
4. 🗄️  Archivar a COLD storage
5. 🔄 Restaurar archivos
6. 📊 Ver estadísticas
7. ⚙️  Configuración
8. ❌ Salir

Ingrese su opción (1-8): 
```

## 📊 Monitoreo y Reportes

### Ver Estadísticas de Uso
```cmd
# Estadísticas generales del bucket
python obs_utils_improved.py --operation stats --bucket mi-bucket

# Estadísticas por clase de almacenamiento
python obs_utils_improved.py --operation storage-stats --bucket mi-bucket

# Reporte de costos estimados
python obs_utils_improved.py --operation cost-report --bucket mi-bucket --period monthly
```

### Generar Reportes
```cmd
# Reporte de actividad diaria
python obs_utils_improved.py --generate-report --type daily --output "reporte_diario.pdf"

# Reporte de archivos archivados
python obs_utils_improved.py --generate-report --type archived --bucket mi-bucket

# Reporte de uso de almacenamiento
python obs_utils_improved.py --generate-report --type storage-usage --format excel
```

## 🔧 Configuración Personal

### Configurar Preferencias
```cmd
# Configurar bucket predeterminado
python obs_utils_improved.py --set-default-bucket mi-bucket-principal

# Configurar directorio de descarga predeterminado
python obs_utils_improved.py --set-download-path "C:\MisDescargas"

# Configurar formato de fecha preferido
python obs_utils_improved.py --set-date-format "DD/MM/YYYY"
```

### Configurar Notificaciones
```cmd
# Habilitar notificaciones por email
python obs_utils_improved.py --configure-notifications --email mi.email@empresa.com

# Configurar notificaciones para operaciones completadas
python obs_utils_improved.py --enable-completion-notifications

# Configurar alertas de errores
python obs_utils_improved.py --enable-error-alerts
```

## 📁 Gestión de Archivos por Lotes

### Crear Listas de Archivos
```cmd
# Crear lista de archivos para procesar
python obs_utils_improved.py --create-file-list --bucket mi-bucket --prefix "reportes/" --output "lista_reportes.txt"

# Filtrar archivos por fecha
python obs_utils_improved.py --create-file-list --bucket mi-bucket --newer-than "30 days" --output "archivos_recientes.txt"

# Filtrar archivos por tamaño
python obs_utils_improved.py --create-file-list --bucket mi-bucket --smaller-than "10MB" --output "archivos_pequeños.txt"
```

### Operaciones por Lotes
```cmd
# Procesar lista de archivos para archivar
python obs_utils_improved.py --batch-archive --file-list "lista_archivos.txt"

# Descargar múltiples archivos desde lista
python obs_utils_improved.py --batch-download --file-list "lista_descargas.txt" --local-path "C:\Descargas"

# Restaurar múltiples archivos
python obs_utils_improved.py --batch-restore --file-list "lista_restaurar.txt"
```

## 🚨 Manejo de Errores Comunes

### Error: "Contraseña Requerida"
```cmd
# Verificar nivel de seguridad requerido
python obs_utils_improved.py --check-operation-level --operation archive

# Solicitar elevación de privilegios
python obs_utils_improved.py --request-elevation --operation archive
```

### Error: "Archivo No Encontrado"
```cmd
# Verificar existencia del archivo
python obs_utils_improved.py --check-object --bucket mi-bucket --key "archivo.pdf"

# Buscar archivos similares
python obs_utils_improved.py --search-similar --bucket mi-bucket --key "archivo.pdf"
```

### Error: "Sesión Expirada"
```cmd
# Renovar sesión
python obs_utils_improved.py --renew-session

# Verificar estado de la sesión
python obs_utils_improved.py --session-status
```

## 📋 Lista de Verificación Diaria

### Al Iniciar el Día
- [ ] Verificar conexión a OBS
- [ ] Revisar notificaciones pendientes
- [ ] Comprobar estado de operaciones en curso
- [ ] Verificar espacio de almacenamiento disponible

### Durante el Trabajo
- [ ] Documentar operaciones importantes
- [ ] Verificar integridad de descargas importantes
- [ ] Monitorear progreso de operaciones por lotes
- [ ] Reportar cualquier error o anomalía

### Al Finalizar el Día
- [ ] Verificar que todas las operaciones se completaron
- [ ] Generar reporte de actividad diaria
- [ ] Cerrar sesión de forma segura
- [ ] Documentar pendientes para el día siguiente

## 🔍 Comandos de Ayuda

### Ayuda General
```cmd
# Ayuda completa
python obs_utils_improved.py --help

# Ayuda para operación específica
python obs_utils_improved.py --help --operation archive

# Listar todas las operaciones disponibles
python obs_utils_improved.py --list-operations
```

### Ejemplos Prácticos
```cmd
# Ver ejemplos de uso
python obs_utils_improved.py --examples

# Ver ejemplos para operación específica
python obs_utils_improved.py --examples --operation restore

# Tutorial interactivo
python obs_utils_improved.py --tutorial
```

## 📞 Soporte

### Contactos de Soporte
- **Soporte Técnico**: support@ccvass.com
- **Administrador del Sistema**: admin@empresa.com
- **Documentación**: [Guía Completa](README.md)

### Información para Reportar Problemas
Cuando reporte un problema, incluya:
1. **Comando ejecutado**: Comando completo que causó el error
2. **Mensaje de error**: Mensaje de error completo
3. **Contexto**: Qué estaba intentando hacer
4. **Archivos de log**: Ubicados en `logs/obs_utils.log`

### Recursos Adicionales
- [Inicio Rápido Windows](INICIO_RAPIDO_WINDOWS.md)
- [Guía de Seguridad](SECURITY.md)
- [Solución de Problemas](docs/es/SOLUCION_PROBLEMAS.md)
- [Preguntas Frecuentes](docs/es/FAQ.md)

## 💡 Consejos y Mejores Prácticas

### Optimización de Rendimiento
- Use operaciones por lotes para múltiples archivos
- Configure un directorio de descarga local rápido (SSD)
- Programe operaciones de archivo durante horas de menor uso
- Use filtros específicos para reducir el tiempo de búsqueda

### Gestión de Costos
- Archive archivos antiguos a COLD storage para reducir costos
- Use WARM storage para archivos de acceso infrecuente
- Monitoree regularmente el uso de almacenamiento
- Elimine archivos duplicados o innecesarios (requiere permisos de supervisor)

### Seguridad
- Nunca comparta su contraseña de operador
- Cierre sesión al finalizar el trabajo
- Reporte actividad sospechosa inmediatamente
- Mantenga actualizada su información de contacto

---

**Desarrollado por**: CCVASS - Lima, Perú 🇵🇪  
**Contacto**: contact@ccvass.com  
**Versión**: 2.0.0  
**Última Actualización**: Julio 2025
