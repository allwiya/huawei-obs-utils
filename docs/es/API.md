# Referencia API

Este documento proporciona información detallada sobre la API de OBS Utils y la interfaz de línea de comandos.

## Interfaz de Línea de Comandos

### Sintaxis Básica
```bash
python obs_utils_improved.py [OPCIONES] [OPCIONES_OPERACION]
```

### Opciones Globales

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--help` | Mostrar mensaje de ayuda | `--help` |
| `--version` | Mostrar información de versión | `--version` |
| `--config-file` | Especificar archivo de configuración | `--config-file config.json` |
| `--log-level` | Establecer nivel de logging | `--log-level DEBUG` |
| `--test-config` | Probar configuración | `--test-config` |

### Opciones de Configuración

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--create-config` | Crear archivo de configuración básico | `--create-config` |
| `--setup-secure-config` | Configurar configuración encriptada | `--setup-secure-config` |
| `--change-password` | Cambiar contraseña de encriptación | `--change-password` |

### Opciones de Operación

#### Operación List (Listar)
```bash
python obs_utils_improved.py --operation list [OPCIONES]
```

| Opción | Descripción | Por Defecto | Ejemplo |
|--------|-------------|-------------|---------|
| `--bucket` | Nombre del bucket | Requerido | `--bucket mi-bucket` |
| `--prefix` | Filtro de prefijo de objeto | Ninguno | `--prefix "carpeta/"` |
| `--max-keys` | Máximo de objetos a listar | 1000 | `--max-keys 500` |

#### Operación Archive (Archivar)
```bash
python obs_utils_improved.py --operation archive [OPCIONES]
```

| Opción | Descripción | Por Defecto | Ejemplo |
|--------|-------------|-------------|---------|
| `--bucket` | Nombre del bucket | Requerido | `--bucket mi-bucket` |
| `--prefix` | Filtro de prefijo de objeto | Ninguno | `--prefix "archivos-antiguos/"` |
| `--days-old` | Archivar archivos más antiguos que N días | 30 | `--days-old 90` |
| `--dry-run` | Mostrar qué se archivaría | False | `--dry-run` |

#### Operación Warm (Tibio)
```bash
python obs_utils_improved.py --operation warm [OPCIONES]
```

| Opción | Descripción | Por Defecto | Ejemplo |
|--------|-------------|-------------|---------|
| `--bucket` | Nombre del bucket | Requerido | `--bucket mi-bucket` |
| `--prefix` | Filtro de prefijo de objeto | Ninguno | `--prefix "infrecuente/"` |
| `--dry-run` | Mostrar qué se movería | False | `--dry-run` |

#### Operación Restore (Restaurar)
```bash
python obs_utils_improved.py --operation restore [OPCIONES]
```

| Opción | Descripción | Por Defecto | Ejemplo |
|--------|-------------|-------------|---------|
| `--bucket` | Nombre del bucket | Requerido | `--bucket mi-bucket` |
| `--prefix` | Filtro de prefijo de objeto | Ninguno | `--prefix "archivados/"` |
| `--days` | Duración de restauración en días | 1 | `--days 7` |

#### Operación Download (Descargar)
```bash
python obs_utils_improved.py --operation download [OPCIONES]
```

| Opción | Descripción | Por Defecto | Ejemplo |
|--------|-------------|-------------|---------|
| `--bucket` | Nombre del bucket | Requerido | `--bucket mi-bucket` |
| `--prefix` | Filtro de prefijo de objeto | Ninguno | `--prefix "reportes/"` |
| `--local-path` | Directorio local de descarga | `./downloads` | `--local-path /tmp/obs` |
| `--overwrite` | Sobrescribir archivos existentes | False | `--overwrite` |

#### Operación Search (Buscar)
```bash
python obs_utils_improved.py --operation search [OPCIONES]
```

| Opción | Descripción | Por Defecto | Ejemplo |
|--------|-------------|-------------|---------|
| `--search-text` | Texto a buscar en nombres de objeto | Requerido | `--search-text "backup"` |
| `--bucket` | Bucket específico para buscar | Todos los buckets | `--bucket mi-bucket` |
| `--case-sensitive` | Búsqueda sensible a mayúsculas | False | `--case-sensitive` |

## API de Python

### Clase OBSManager

#### Inicialización
```python
from obs_manager import OBSManager

# Inicializar con archivo de configuración
manager = OBSManager(config_file="obs_config.json")

# Inicializar con credenciales
manager = OBSManager(
    access_key_id="tu_clave",
    secret_access_key="tu_secreto",
    server="https://obs.sa-peru-1.myhuaweicloud.com/",
    region="sa-peru-1"
)
```

#### Métodos

##### list_objects(bucket_name, prefix=None, max_keys=1000)
Listar objetos en un bucket.

**Parámetros:**
- `bucket_name` (str): Nombre del bucket
- `prefix` (str, opcional): Filtro de prefijo de objeto
- `max_keys` (int): Número máximo de objetos a retornar

**Retorna:**
- `list`: Lista de diccionarios de objetos

**Ejemplo:**
```python
objects = manager.list_objects("mi-bucket", prefix="carpeta/")
for obj in objects:
    print(f"Objeto: {obj['key']}, Tamaño: {obj['size']}")
```

##### archive_objects(bucket_name, prefix=None, days_old=30, dry_run=False)
Archivar objetos a almacenamiento COLD.

**Parámetros:**
- `bucket_name` (str): Nombre del bucket
- `prefix` (str, opcional): Filtro de prefijo de objeto
- `days_old` (int): Archivar objetos más antiguos que esta cantidad de días
- `dry_run` (bool): Si es True, solo mostrar qué se archivaría

**Retorna:**
- `dict`: Resultados con conteos y objetos procesados

**Ejemplo:**
```python
result = manager.archive_objects("mi-bucket", days_old=90)
print(f"Archivados {result['archived_count']} objetos")
```

##### warm_objects(bucket_name, prefix=None, dry_run=False)
Mover objetos a almacenamiento WARM.

**Parámetros:**
- `bucket_name` (str): Nombre del bucket
- `prefix` (str, opcional): Filtro de prefijo de objeto
- `dry_run` (bool): Si es True, solo mostrar qué se movería

**Retorna:**
- `dict`: Resultados con conteos y objetos procesados

##### restore_objects(bucket_name, prefix=None, days=1)
Restaurar objetos desde almacenamiento COLD.

**Parámetros:**
- `bucket_name` (str): Nombre del bucket
- `prefix` (str, opcional): Filtro de prefijo de objeto
- `days` (int): Número de días para mantener objetos restaurados disponibles

**Retorna:**
- `dict`: Resultados con conteos y objetos procesados

##### download_objects(bucket_name, prefix=None, local_path="./downloads", overwrite=False)
Descargar objetos desde bucket.

**Parámetros:**
- `bucket_name` (str): Nombre del bucket
- `prefix` (str, opcional): Filtro de prefijo de objeto
- `local_path` (str): Directorio local para descargar
- `overwrite` (bool): Si sobrescribir archivos existentes

**Retorna:**
- `dict`: Resultados con conteos y objetos descargados

##### search_objects(search_text, bucket_name=None, case_sensitive=False)
Buscar objetos por nombre.

**Parámetros:**
- `search_text` (str): Texto a buscar en nombres de objeto
- `bucket_name` (str, opcional): Bucket específico para buscar
- `case_sensitive` (bool): Si la búsqueda es sensible a mayúsculas

**Retorna:**
- `list`: Lista de objetos coincidentes

## Clases de Almacenamiento

### STANDARD
- **Caso de uso**: Datos accedidos frecuentemente
- **Costo**: Mayor costo de almacenamiento, menor costo de acceso
- **Tiempo de acceso**: Inmediato
- **Duración mínima de almacenamiento**: Ninguna

### WARM
- **Caso de uso**: Datos accedidos infrecuentemente
- **Costo**: Costo medio de almacenamiento, costo medio de acceso
- **Tiempo de acceso**: Inmediato
- **Duración mínima de almacenamiento**: 30 días

### COLD
- **Caso de uso**: Datos de archivo y respaldo
- **Costo**: Menor costo de almacenamiento, mayor costo de acceso
- **Tiempo de acceso**: Requiere restauración (1-12 horas)
- **Duración mínima de almacenamiento**: 90 días

## Manejo de Errores

### Excepciones Comunes

#### OBSException
Excepción base para errores relacionados con OBS.

```python
from obs_manager import OBSException

try:
    manager.list_objects("bucket-inexistente")
except OBSException as e:
    print(f"Error OBS: {e}")
```

#### ConfigurationError
Se lanza cuando la configuración es inválida o falta.

```python
from config import ConfigurationError

try:
    manager = OBSManager()
except ConfigurationError as e:
    print(f"Error de Configuración: {e}")
```

#### SecurityError
Se lanza cuando falla la validación de seguridad.

```python
from security import SecurityError

try:
    manager.load_encrypted_config("config.enc", "contraseña_incorrecta")
except SecurityError as e:
    print(f"Error de Seguridad: {e}")
```

## Formatos de Respuesta

### Diccionario de Objeto
```python
{
    "key": "carpeta/archivo.txt",
    "size": 1024,
    "last_modified": "2025-01-01T12:00:00Z",
    "etag": "d41d8cd98f00b204e9800998ecf8427e",
    "storage_class": "STANDARD",
    "owner": {
        "id": "owner_id",
        "display_name": "owner_name"
    }
}
```

### Diccionario de Resultado de Operación
```python
{
    "success": True,
    "processed_count": 150,
    "success_count": 148,
    "error_count": 2,
    "objects": [...],
    "errors": [...]
}
```

## Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `OBS_ACCESS_KEY_ID` | ID de clave de acceso | `AKIAIOSFODNN7EXAMPLE` |
| `OBS_SECRET_ACCESS_KEY` | Clave de acceso secreta | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `OBS_SERVER` | Endpoint del servidor OBS | `https://obs.sa-peru-1.myhuaweicloud.com/` |
| `OBS_REGION` | Región OBS | `sa-peru-1` |
| `OBS_LOG_LEVEL` | Nivel de logging | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Códigos de Salida

| Código | Descripción |
|--------|-------------|
| 0 | Éxito |
| 1 | Error general |
| 2 | Error de configuración |
| 3 | Error de autenticación |
| 4 | Error de red |
| 5 | Error de permisos |

## Ejemplos

### Uso Básico
```bash
# Listar todos los objetos en un bucket
python obs_utils_improved.py --operation list --bucket mi-bucket

# Archivar archivos antiguos
python obs_utils_improved.py --operation archive --bucket mi-bucket --days-old 90

# Descargar carpeta específica
python obs_utils_improved.py --operation download --bucket mi-bucket --prefix "reportes/2024/"
```

### Uso Avanzado
```bash
# Operación de archivo en modo de prueba
python obs_utils_improved.py --operation archive --bucket mi-bucket --dry-run

# Buscar con configuración personalizada
python obs_utils_improved.py --config-file config-prod.json --operation search --search-text "backup"

# Modo debug
python obs_utils_improved.py --log-level DEBUG --operation list --bucket mi-bucket
```

### Uso de API Python
```python
from obs_manager import OBSManager

# Inicializar
manager = OBSManager(config_file="obs_config.json")

# Listar objetos
objects = manager.list_objects("mi-bucket")
print(f"Encontrados {len(objects)} objetos")

# Archivar objetos antiguos
result = manager.archive_objects("mi-bucket", days_old=90)
print(f"Archivados {result['success_count']} objetos")

# Buscar respaldos
backups = manager.search_objects("backup", case_sensitive=False)
for backup in backups:
    print(f"Respaldo: {backup['key']}")
```

## Soporte

Para preguntas sobre la API y problemas:
- Revisar los [Ejemplos](EJEMPLOS.md) para uso práctico
- Revisar la [Guía de Solución de Problemas](SOLUCION_PROBLEMAS.md)
- Contactar [contact@ccvass.com](mailto:contact@ccvass.com)

---

**Desarrollado por CCVASS - Lima, Perú 🇵🇪**
