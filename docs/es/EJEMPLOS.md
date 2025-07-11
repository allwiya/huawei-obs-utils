# Ejemplos de Uso

Esta guía proporciona ejemplos prácticos de cómo usar OBS Utils para diferentes escenarios comunes.

## 🚀 Ejemplos Básicos

### 1. Listar Objetos en un Bucket

#### Listar todos los objetos
```bash
python obs_utils_improved.py --operation list --bucket mi-bucket
```

#### Listar objetos con prefijo específico
```bash
python obs_utils_improved.py --operation list --bucket mi-bucket --prefix "documentos/"
```

#### Limitar número de objetos listados
```bash
python obs_utils_improved.py --operation list --bucket mi-bucket --max-keys 50
```

### 2. Archivar Archivos Antiguos

#### Archivar archivos más antiguos que 30 días
```bash
python obs_utils_improved.py --operation archive --bucket mi-bucket --days-old 30
```

#### Archivar solo archivos en una carpeta específica
```bash
python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "logs/2024/" --days-old 90
```

#### Modo de prueba (ver qué se archivaría sin hacer cambios)
```bash
python obs_utils_improved.py --operation archive --bucket mi-bucket --dry-run
```

### 3. Descargar Archivos

#### Descargar todos los archivos de un bucket
```bash
python obs_utils_improved.py --operation download --bucket mi-bucket
```

#### Descargar archivos de una carpeta específica
```bash
python obs_utils_improved.py --operation download --bucket mi-bucket --prefix "reportes/2024/"
```

#### Descargar a un directorio específico
```bash
python obs_utils_improved.py --operation download --bucket mi-bucket --local-path "/home/usuario/descargas/"
```

#### Sobrescribir archivos existentes
```bash
python obs_utils_improved.py --operation download --bucket mi-bucket --overwrite
```

## 🔍 Ejemplos de Búsqueda

### 1. Buscar Archivos por Nombre

#### Buscar archivos que contengan "backup"
```bash
python obs_utils_improved.py --operation search --search-text "backup"
```

#### Buscar en un bucket específico
```bash
python obs_utils_improved.py --operation search --search-text "log" --bucket mi-bucket
```

#### Búsqueda sensible a mayúsculas
```bash
python obs_utils_improved.py --operation search --search-text "BACKUP" --case-sensitive
```

### 2. Búsquedas Avanzadas

#### Buscar archivos de respaldo del año 2024
```bash
python obs_utils_improved.py --operation search --search-text "backup_2024"
```

#### Buscar archivos de configuración
```bash
python obs_utils_improved.py --operation search --search-text ".conf"
```

## 🗄️ Gestión de Clases de Almacenamiento

### 1. Mover a Almacenamiento WARM

#### Mover archivos infrecuentemente accedidos
```bash
python obs_utils_improved.py --operation warm --bucket mi-bucket --prefix "archivos-antiguos/"
```

#### Modo de prueba para almacenamiento WARM
```bash
python obs_utils_improved.py --operation warm --bucket mi-bucket --dry-run
```

### 2. Restaurar desde Almacenamiento COLD

#### Restaurar archivos archivados por 1 día
```bash
python obs_utils_improved.py --operation restore --bucket mi-bucket --prefix "archivados/"
```

#### Restaurar por una semana
```bash
python obs_utils_improved.py --operation restore --bucket mi-bucket --prefix "respaldos/" --days 7
```

## 🔧 Configuración y Administración

### 1. Configuración Inicial

#### Crear configuración básica
```bash
python obs_utils_improved.py --create-config
```

#### Configurar encriptación segura
```bash
python obs_utils_improved.py --setup-secure-config
```

#### Probar configuración
```bash
python obs_utils_improved.py --test-config
```

### 2. Gestión de Configuración

#### Usar archivo de configuración personalizado
```bash
python obs_utils_improved.py --config-file /ruta/a/mi-config.json --operation list --bucket mi-bucket
```

#### Cambiar contraseña de encriptación
```bash
python obs_utils_improved.py --change-password
```

## 📊 Ejemplos con Logging y Debug

### 1. Logging Detallado

#### Ejecutar con logging DEBUG
```bash
python obs_utils_improved.py --log-level DEBUG --operation list --bucket mi-bucket
```

#### Ejecutar con logging INFO
```bash
python obs_utils_improved.py --log-level INFO --operation archive --bucket mi-bucket
```

### 2. Monitoreo de Operaciones

#### Ver logs en tiempo real
```bash
# En una terminal
tail -f logs/obs_utils.log

# En otra terminal
python obs_utils_improved.py --operation download --bucket mi-bucket
```

## 🐍 Ejemplos de API Python

### 1. Uso Básico de la API

```python
from obs_manager import OBSManager

# Inicializar el manager
manager = OBSManager(config_file="obs_config.json")

# Listar objetos
objects = manager.list_objects("mi-bucket")
print(f"Encontrados {len(objects)} objetos")

# Mostrar información de cada objeto
for obj in objects:
    print(f"Archivo: {obj['key']}")
    print(f"Tamaño: {obj['size']} bytes")
    print(f"Última modificación: {obj['last_modified']}")
    print(f"Clase de almacenamiento: {obj['storage_class']}")
    print("-" * 40)
```

### 2. Operaciones por Lotes

```python
from obs_manager import OBSManager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Inicializar
manager = OBSManager(config_file="obs_config.json")

# Procesar múltiples buckets
buckets = ["bucket1", "bucket2", "bucket3"]

for bucket in buckets:
    print(f"Procesando bucket: {bucket}")
    
    # Archivar archivos antiguos
    result = manager.archive_objects(bucket, days_old=90, dry_run=False)
    
    print(f"  - Procesados: {result['processed_count']}")
    print(f"  - Archivados: {result['success_count']}")
    print(f"  - Errores: {result['error_count']}")
```

### 3. Manejo de Errores

```python
from obs_manager import OBSManager, OBSException
from config import ConfigurationError

try:
    # Inicializar manager
    manager = OBSManager(config_file="obs_config.json")
    
    # Intentar listar objetos
    objects = manager.list_objects("bucket-inexistente")
    
except ConfigurationError as e:
    print(f"Error de configuración: {e}")
    print("Ejecuta: python obs_utils_improved.py --create-config")
    
except OBSException as e:
    print(f"Error de OBS: {e}")
    print("Verifica tus credenciales y el nombre del bucket")
    
except Exception as e:
    print(f"Error inesperado: {e}")
```

### 4. Búsqueda y Filtrado Avanzado

```python
from obs_manager import OBSManager
from datetime import datetime, timedelta

manager = OBSManager(config_file="obs_config.json")

# Buscar archivos de respaldo
backup_files = manager.search_objects("backup", case_sensitive=False)

# Filtrar por fecha (archivos de la última semana)
week_ago = datetime.now() - timedelta(days=7)

recent_backups = []
for file in backup_files:
    file_date = datetime.fromisoformat(file['last_modified'].replace('Z', '+00:00'))
    if file_date > week_ago:
        recent_backups.append(file)

print(f"Respaldos recientes encontrados: {len(recent_backups)}")
for backup in recent_backups:
    print(f"  - {backup['key']} ({backup['size']} bytes)")
```

## 🔄 Ejemplos de Automatización

### 1. Script de Mantenimiento Diario

```bash
#!/bin/bash
# daily_maintenance.sh

echo "Iniciando mantenimiento diario de OBS..."

# Archivar logs antiguos
python obs_utils_improved.py --operation archive --bucket logs-bucket --prefix "logs/" --days-old 30

# Mover archivos infrecuentes a WARM
python obs_utils_improved.py --operation warm --bucket data-bucket --prefix "old-data/"

# Limpiar archivos temporales muy antiguos
python obs_utils_improved.py --operation list --bucket temp-bucket --prefix "temp/" | \
grep "$(date -d '7 days ago' '+%Y-%m-%d')" | \
while read file; do
    echo "Eliminando archivo temporal antiguo: $file"
    # Aquí agregarías lógica para eliminar
done

echo "Mantenimiento completado."
```

### 2. Script de Respaldo Semanal

```bash
#!/bin/bash
# weekly_backup.sh

BACKUP_DATE=$(date +%Y%m%d)
BUCKET="backup-bucket"

echo "Iniciando respaldo semanal - $BACKUP_DATE"

# Descargar respaldos críticos
python obs_utils_improved.py --operation download \
    --bucket $BUCKET \
    --prefix "critical/" \
    --local-path "/backup/weekly/$BACKUP_DATE/"

# Verificar integridad
if [ $? -eq 0 ]; then
    echo "Respaldo completado exitosamente"
    # Enviar notificación de éxito
else
    echo "Error en el respaldo"
    # Enviar alerta
fi
```

### 3. Monitoreo con Cron

```bash
# Agregar a crontab: crontab -e

# Mantenimiento diario a las 2 AM
0 2 * * * /ruta/a/obs_utils/daily_maintenance.sh >> /var/log/obs_maintenance.log 2>&1

# Respaldo semanal los domingos a las 3 AM
0 3 * * 0 /ruta/a/obs_utils/weekly_backup.sh >> /var/log/obs_backup.log 2>&1

# Verificación de configuración diaria
30 1 * * * cd /ruta/a/obs_utils && python obs_utils_improved.py --test-config >> /var/log/obs_config_check.log 2>&1
```

## 🌐 Ejemplos Multi-Región

### 1. Configuración para Múltiples Regiones

```bash
# Configuración para Perú
python obs_utils_improved.py --config-file config-peru.json --operation list --bucket bucket-peru

# Configuración para Singapur
python obs_utils_improved.py --config-file config-singapore.json --operation list --bucket bucket-singapore
```

### 2. Script de Sincronización Multi-Región

```python
from obs_manager import OBSManager

# Configuraciones para diferentes regiones
configs = {
    'peru': 'config-peru.json',
    'singapore': 'config-singapore.json',
    'paris': 'config-paris.json'
}

# Inicializar managers para cada región
managers = {}
for region, config_file in configs.items():
    managers[region] = OBSManager(config_file=config_file)

# Listar buckets en todas las regiones
for region, manager in managers.items():
    print(f"\n=== Región: {region.upper()} ===")
    try:
        # Aquí necesitarías implementar list_buckets si no existe
        buckets = manager.list_buckets()  # Método hipotético
        for bucket in buckets:
            objects = manager.list_objects(bucket['name'])
            print(f"Bucket: {bucket['name']} - {len(objects)} objetos")
    except Exception as e:
        print(f"Error en región {region}: {e}")
```

## 🔐 Ejemplos de Seguridad

### 1. Verificación de Configuración Segura

```bash
# Verificar permisos de archivos
ls -la obs_config.json*

# Probar configuración encriptada
python obs_utils_improved.py --test-config

# Verificar variables de entorno
env | grep OBS | wc -l
```

### 2. Rotación de Credenciales

```bash
#!/bin/bash
# rotate_credentials.sh

echo "Iniciando rotación de credenciales..."

# Respaldar configuración actual
cp obs_config.json.enc obs_config.json.enc.backup.$(date +%Y%m%d)

# Configurar nuevas credenciales
python obs_utils_improved.py --setup-secure-config

# Probar nueva configuración
if python obs_utils_improved.py --test-config; then
    echo "Nueva configuración válida"
    rm obs_config.json.enc.backup.*
else
    echo "Error en nueva configuración, restaurando respaldo"
    mv obs_config.json.enc.backup.* obs_config.json.enc
fi
```

## 📈 Ejemplos de Monitoreo y Reportes

### 1. Reporte de Uso de Almacenamiento

```python
from obs_manager import OBSManager
from collections import defaultdict

manager = OBSManager(config_file="obs_config.json")

# Obtener estadísticas por clase de almacenamiento
storage_stats = defaultdict(lambda: {'count': 0, 'size': 0})

buckets = ['bucket1', 'bucket2', 'bucket3']  # Lista de buckets

for bucket in buckets:
    objects = manager.list_objects(bucket)
    
    for obj in objects:
        storage_class = obj.get('storage_class', 'STANDARD')
        storage_stats[storage_class]['count'] += 1
        storage_stats[storage_class]['size'] += obj['size']

# Generar reporte
print("=== REPORTE DE USO DE ALMACENAMIENTO ===")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

total_objects = 0
total_size = 0

for storage_class, stats in storage_stats.items():
    count = stats['count']
    size_gb = stats['size'] / (1024**3)  # Convertir a GB
    
    print(f"{storage_class}:")
    print(f"  Objetos: {count:,}")
    print(f"  Tamaño: {size_gb:.2f} GB")
    print()
    
    total_objects += count
    total_size += stats['size']

print(f"TOTAL:")
print(f"  Objetos: {total_objects:,}")
print(f"  Tamaño: {total_size / (1024**3):.2f} GB")
```

### 2. Monitoreo de Operaciones

```bash
#!/bin/bash
# monitor_operations.sh

LOG_FILE="logs/obs_utils.log"
REPORT_FILE="reports/daily_report_$(date +%Y%m%d).txt"

echo "=== REPORTE DIARIO OBS UTILS ===" > $REPORT_FILE
echo "Fecha: $(date)" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Contar operaciones por tipo
echo "Operaciones realizadas hoy:" >> $REPORT_FILE
grep "$(date +%Y-%m-%d)" $LOG_FILE | grep "Operation:" | \
    awk '{print $NF}' | sort | uniq -c >> $REPORT_FILE

echo "" >> $REPORT_FILE

# Contar errores
ERROR_COUNT=$(grep "$(date +%Y-%m-%d)" $LOG_FILE | grep "ERROR" | wc -l)
echo "Errores encontrados: $ERROR_COUNT" >> $REPORT_FILE

if [ $ERROR_COUNT -gt 0 ]; then
    echo "" >> $REPORT_FILE
    echo "Detalles de errores:" >> $REPORT_FILE
    grep "$(date +%Y-%m-%d)" $LOG_FILE | grep "ERROR" >> $REPORT_FILE
fi

# Enviar reporte por email (opcional)
# mail -s "Reporte Diario OBS Utils" admin@empresa.com < $REPORT_FILE
```

## 🆘 Ejemplos de Solución de Problemas

### 1. Diagnóstico de Problemas de Conexión

```bash
#!/bin/bash
# diagnose_connection.sh

echo "=== DIAGNÓSTICO DE CONEXIÓN OBS ==="

# Verificar conectividad básica
echo "1. Verificando conectividad a Internet..."
if ping -c 3 google.com > /dev/null 2>&1; then
    echo "   ✅ Conectividad a Internet OK"
else
    echo "   ❌ Sin conectividad a Internet"
fi

# Verificar endpoint OBS
echo "2. Verificando endpoint OBS..."
OBS_ENDPOINT="obs.sa-peru-1.myhuaweicloud.com"
if ping -c 3 $OBS_ENDPOINT > /dev/null 2>&1; then
    echo "   ✅ Endpoint OBS accesible"
else
    echo "   ❌ Endpoint OBS no accesible"
fi

# Verificar configuración
echo "3. Verificando configuración..."
if python obs_utils_improved.py --test-config > /dev/null 2>&1; then
    echo "   ✅ Configuración válida"
else
    echo "   ❌ Configuración inválida"
    echo "   Ejecuta: python obs_utils_improved.py --create-config"
fi

# Verificar permisos de archivos
echo "4. Verificando permisos de archivos..."
if [ -f "obs_config.json" ]; then
    PERMS=$(stat -c "%a" obs_config.json)
    if [ "$PERMS" = "600" ]; then
        echo "   ✅ Permisos de archivo seguros (600)"
    else
        echo "   ⚠️  Permisos de archivo: $PERMS (recomendado: 600)"
        echo "   Ejecuta: chmod 600 obs_config.json"
    fi
fi
```

### 2. Recuperación de Errores

```python
from obs_manager import OBSManager, OBSException
import time
import logging

def retry_operation(func, max_retries=3, delay=5):
    """Reintentar operación con backoff exponencial"""
    for attempt in range(max_retries):
        try:
            return func()
        except OBSException as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = delay * (2 ** attempt)
            logging.warning(f"Intento {attempt + 1} falló: {e}")
            logging.info(f"Reintentando en {wait_time} segundos...")
            time.sleep(wait_time)

# Ejemplo de uso
manager = OBSManager(config_file="obs_config.json")

def list_objects_with_retry():
    return retry_operation(
        lambda: manager.list_objects("mi-bucket"),
        max_retries=3,
        delay=5
    )

try:
    objects = list_objects_with_retry()
    print(f"Éxito: {len(objects)} objetos encontrados")
except Exception as e:
    print(f"Error final después de reintentos: {e}")
```

---

**¿Necesitas más ejemplos?** Contacta [contact@ccvass.com](mailto:contact@ccvass.com) o revisa la [documentación completa](../es/).

**Desarrollado por CCVASS - Lima, Perú 🇵🇪**
