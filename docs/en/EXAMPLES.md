# 📚 Ejemplos Avanzados de Uso - OBS Utils

Este archivo contiene ejemplos avanzados y casos de uso específicos para el proyecto OBS Utils.

## 📋 Índice de Ejemplos

1. [Gestión Básica de Buckets](#gestión-básica-de-buckets)
2. [Optimización de Costos](#optimización-de-costos)
3. [Migración de Datos](#migración-de-datos)
4. [Automatización con Scripts](#automatización-con-scripts)
5. [Monitoreo y Reportes](#monitoreo-y-reportes)
6. [Casos de Uso Empresariales](#casos-de-uso-empresariales)

## 🗂️ Gestión Básica de Buckets

### Ejemplo 1: Inventario Completo de Buckets

```python
#!/usr/bin/env python3
"""
Script para generar un inventario completo de todos los buckets
"""
from obs_manager import OBSManager
import csv
from datetime import datetime

def generate_inventory():
    obs_manager = OBSManager()
    
    try:
        # Crear archivo CSV para el inventario
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"inventory_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Bucket', 'Object Key', 'Size (bytes)', 'Last Modified', 'Storage Class', 'Owner'])
            
            # Obtener lista de buckets (simulado - necesitarías implementar list_buckets)
            buckets = ["bucket1", "bucket2", "bucket3"]  # Reemplazar con buckets reales
            
            for bucket in buckets:
                print(f"Procesando bucket: {bucket}")
                
                # Usar el generador interno para obtener información detallada
                for content in obs_manager._paginated_list_objects(bucket):
                    writer.writerow([
                        bucket,
                        content.key,
                        content.size,
                        content.lastModified,
                        content.storageClass,
                        content.owner.owner_name
                    ])
        
        print(f"Inventario generado: {csv_file}")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    generate_inventory()
```

### Ejemplo 2: Limpieza de Archivos Temporales

```python
#!/usr/bin/env python3
"""
Script para limpiar archivos temporales y de cache
"""
from obs_manager import OBSManager
from datetime import datetime, timedelta

def cleanup_temp_files():
    obs_manager = OBSManager()
    
    try:
        # Buscar archivos temporales
        temp_patterns = [".tmp", ".temp", ".cache", "~"]
        
        for pattern in temp_patterns:
            print(f"Buscando archivos {pattern}...")
            count = obs_manager.search_objects(pattern, "temp-bucket")
            print(f"Encontrados {count} archivos temporales con patrón {pattern}")
        
        # Buscar archivos antiguos en carpeta temp
        print("Listando archivos en carpeta temporal...")
        temp_count = obs_manager.list_objects("main-bucket", "temp/")
        print(f"Total de archivos temporales: {temp_count}")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    cleanup_temp_files()
```

## 💰 Optimización de Costos

### Ejemplo 3: Análisis de Costos por Storage Class

```python
#!/usr/bin/env python3
"""
Script para analizar distribución de storage classes y estimar costos
"""
from obs_manager import OBSManager
import json
from collections import defaultdict

def analyze_storage_costs():
    obs_manager = OBSManager()
    
    try:
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "buckets": {},
            "summary": defaultdict(lambda: {"count": 0, "total_size": 0})
        }
        
        buckets = ["production-bucket", "backup-bucket", "archive-bucket"]
        
        for bucket in buckets:
            print(f"Analizando bucket: {bucket}")
            bucket_stats = defaultdict(lambda: {"count": 0, "total_size": 0})
            
            for content in obs_manager._paginated_list_objects(bucket):
                storage_class = content.storageClass
                bucket_stats[storage_class]["count"] += 1
                bucket_stats[storage_class]["total_size"] += content.size
                
                # Actualizar resumen global
                analysis["summary"][storage_class]["count"] += 1
                analysis["summary"][storage_class]["total_size"] += content.size
            
            analysis["buckets"][bucket] = dict(bucket_stats)
        
        # Guardar análisis
        with open("storage_cost_analysis.json", "w") as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Mostrar resumen
        print("\n=== RESUMEN DE STORAGE CLASSES ===")
        for storage_class, stats in analysis["summary"].items():
            size_gb = stats["total_size"] / (1024**3)
            print(f"{storage_class}: {stats['count']} archivos, {size_gb:.2f} GB")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    analyze_storage_costs()
```

### Ejemplo 4: Migración Automática por Edad

```python
#!/usr/bin/env python3
"""
Script para migrar archivos automáticamente basado en su edad
"""
from obs_manager import OBSManager
from datetime import datetime, timedelta
import dateutil.parser

def auto_migrate_by_age():
    obs_manager = OBSManager()
    
    try:
        # Definir políticas de migración
        policies = {
            "WARM": timedelta(days=30),    # Archivos > 30 días a WARM
            "COLD": timedelta(days=90)     # Archivos > 90 días a COLD
        }
        
        bucket = "data-bucket"
        now = datetime.now(tz=datetime.now().astimezone().tzinfo)
        
        candidates = {"WARM": [], "COLD": []}
        
        print("Analizando archivos para migración automática...")
        
        for content in obs_manager._paginated_list_objects(bucket):
            # Parsear fecha de modificación
            last_modified = dateutil.parser.parse(content.lastModified)
            age = now - last_modified
            
            current_class = content.storageClass
            
            # Determinar si necesita migración
            if age > policies["COLD"] and current_class != "COLD":
                candidates["COLD"].append(content.key)
            elif age > policies["WARM"] and current_class == "STANDARD":
                candidates["WARM"].append(content.key)
        
        # Ejecutar migraciones
        for target_class, files in candidates.items():
            if files:
                print(f"Migrando {len(files)} archivos a {target_class}...")
                # Aquí implementarías la migración por lotes
                # Por ahora solo mostramos los candidatos
                for file_key in files[:5]:  # Mostrar solo los primeros 5
                    print(f"  - {file_key}")
                if len(files) > 5:
                    print(f"  ... y {len(files) - 5} más")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    auto_migrate_by_age()
```

## 🔄 Migración de Datos

### Ejemplo 5: Sincronización de Buckets

```python
#!/usr/bin/env python3
"""
Script para sincronizar contenido entre buckets
"""
from obs_manager import OBSManager
import os

def sync_buckets():
    obs_manager = OBSManager()
    
    try:
        source_bucket = "production-bucket"
        target_bucket = "backup-bucket"
        
        print(f"Sincronizando {source_bucket} -> {target_bucket}")
        
        # Obtener lista de archivos del bucket origen
        source_files = set()
        for content in obs_manager._paginated_list_objects(source_bucket):
            source_files.add(content.key)
        
        # Obtener lista de archivos del bucket destino
        target_files = set()
        for content in obs_manager._paginated_list_objects(target_bucket):
            target_files.add(content.key)
        
        # Encontrar diferencias
        missing_files = source_files - target_files
        extra_files = target_files - source_files
        
        print(f"Archivos faltantes en destino: {len(missing_files)}")
        print(f"Archivos extra en destino: {len(extra_files)}")
        
        # Mostrar algunos ejemplos
        if missing_files:
            print("\nEjemplos de archivos faltantes:")
            for file_key in list(missing_files)[:5]:
                print(f"  - {file_key}")
        
        if extra_files:
            print("\nEjemplos de archivos extra:")
            for file_key in list(extra_files)[:5]:
                print(f"  - {file_key}")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    sync_buckets()
```

### Ejemplo 6: Backup Incremental

```python
#!/usr/bin/env python3
"""
Script para realizar backup incremental basado en fechas
"""
from obs_manager import OBSManager
from datetime import datetime, timedelta
import dateutil.parser
import json
import os

def incremental_backup():
    obs_manager = OBSManager()
    
    try:
        # Cargar último backup (si existe)
        last_backup_file = "last_backup.json"
        last_backup_date = None
        
        if os.path.exists(last_backup_file):
            with open(last_backup_file, 'r') as f:
                data = json.load(f)
                last_backup_date = dateutil.parser.parse(data['last_backup'])
        else:
            # Si no hay backup previo, usar fecha de hace 7 días
            last_backup_date = datetime.now() - timedelta(days=7)
        
        print(f"Buscando archivos modificados desde: {last_backup_date}")
        
        source_bucket = "production-bucket"
        backup_dir = "./incremental_backup"
        os.makedirs(backup_dir, exist_ok=True)
        
        files_to_backup = []
        
        # Encontrar archivos modificados
        for content in obs_manager._paginated_list_objects(source_bucket):
            file_modified = dateutil.parser.parse(content.lastModified)
            
            if file_modified > last_backup_date:
                files_to_backup.append(content.key)
        
        print(f"Archivos para backup incremental: {len(files_to_backup)}")
        
        # Descargar archivos (simulado)
        backed_up = 0
        for file_key in files_to_backup[:10]:  # Limitar a 10 para el ejemplo
            print(f"Descargando: {file_key}")
            success = obs_manager.download_single_file(
                source_bucket, 
                file_key, 
                os.path.join(backup_dir, file_key)
            )
            if success:
                backed_up += 1
        
        # Actualizar registro de último backup
        with open(last_backup_file, 'w') as f:
            json.dump({
                'last_backup': datetime.now().isoformat(),
                'files_backed_up': backed_up,
                'total_candidates': len(files_to_backup)
            }, f, indent=2)
        
        print(f"Backup incremental completado: {backed_up} archivos")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    incremental_backup()
```

## 🤖 Automatización con Scripts

### Ejemplo 7: Monitoreo Automático

```python
#!/usr/bin/env python3
"""
Script de monitoreo automático para ejecutar periódicamente
"""
from obs_manager import OBSManager
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json

def monitoring_check():
    obs_manager = OBSManager()
    
    try:
        report = {
            "timestamp": datetime.now().isoformat(),
            "buckets": {},
            "alerts": []
        }
        
        buckets_to_monitor = ["critical-bucket", "backup-bucket", "logs-bucket"]
        
        for bucket in buckets_to_monitor:
            try:
                count = obs_manager.list_objects(bucket)
                report["buckets"][bucket] = {
                    "status": "OK",
                    "object_count": count
                }
                
                # Verificar si el bucket está vacío (posible problema)
                if count == 0:
                    report["alerts"].append(f"ALERTA: Bucket {bucket} está vacío")
                
            except Exception as e:
                report["buckets"][bucket] = {
                    "status": "ERROR",
                    "error": str(e)
                }
                report["alerts"].append(f"ERROR: No se puede acceder al bucket {bucket}")
        
        # Guardar reporte
        with open("monitoring_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Enviar alertas si hay problemas
        if report["alerts"]:
            send_alert_email(report["alerts"])
        
        print("Monitoreo completado")
        for alert in report["alerts"]:
            print(f"⚠️  {alert}")
        
    finally:
        obs_manager.close()

def send_alert_email(alerts):
    """Enviar email de alerta (configurar SMTP según necesidades)"""
    # Configuración de email (ejemplo)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = "monitoring@empresa.com"
    email_password = "password"
    
    message = MIMEText("\n".join(alerts))
    message["Subject"] = "OBS Monitoring Alert"
    message["From"] = email_user
    message["To"] = "admin@empresa.com"
    
    # Descomentar para enviar email real
    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     server.starttls()
    #     server.login(email_user, email_password)
    #     server.send_message(message)
    
    print("📧 Alerta enviada por email (simulado)")

if __name__ == "__main__":
    monitoring_check()
```

### Ejemplo 8: Limpieza Programada

```python
#!/usr/bin/env python3
"""
Script para limpieza programada de archivos antiguos
"""
from obs_manager import OBSManager
from datetime import datetime, timedelta
import dateutil.parser

def scheduled_cleanup():
    obs_manager = OBSManager()
    
    try:
        # Configuración de limpieza
        cleanup_rules = {
            "temp-bucket": {
                "max_age_days": 7,
                "patterns": [".tmp", ".temp"]
            },
            "logs-bucket": {
                "max_age_days": 30,
                "patterns": [".log"]
            },
            "cache-bucket": {
                "max_age_days": 1,
                "patterns": [".cache"]
            }
        }
        
        now = datetime.now(tz=datetime.now().astimezone().tzinfo)
        
        for bucket, rules in cleanup_rules.items():
            print(f"Procesando limpieza en bucket: {bucket}")
            max_age = timedelta(days=rules["max_age_days"])
            
            candidates_for_deletion = []
            
            # Buscar archivos candidatos para eliminación
            for pattern in rules["patterns"]:
                print(f"  Buscando archivos {pattern}...")
                # Aquí usarías search_objects y luego verificarías la edad
                count = obs_manager.search_objects(pattern, bucket)
                print(f"  Encontrados {count} archivos con patrón {pattern}")
            
            # En un script real, aquí implementarías la lógica de eliminación
            # Por seguridad, este ejemplo solo simula la operación
            print(f"  Simulando eliminación de archivos antiguos...")
            print(f"  Criterio: archivos > {rules['max_age_days']} días")
        
        print("Limpieza programada completada")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    scheduled_cleanup()
```

## 📊 Monitoreo y Reportes

### Ejemplo 9: Dashboard de Métricas

```python
#!/usr/bin/env python3
"""
Script para generar dashboard de métricas de OBS
"""
from obs_manager import OBSManager
import json
from datetime import datetime
from collections import defaultdict

def generate_dashboard():
    obs_manager = OBSManager()
    
    try:
        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "metrics": {
                "total_objects": 0,
                "total_size_bytes": 0,
                "storage_classes": defaultdict(int),
                "file_types": defaultdict(int),
                "buckets": {}
            }
        }
        
        buckets = ["production", "staging", "backup", "archive"]
        
        for bucket in buckets:
            print(f"Analizando métricas del bucket: {bucket}")
            
            bucket_metrics = {
                "object_count": 0,
                "total_size": 0,
                "storage_classes": defaultdict(int),
                "file_extensions": defaultdict(int)
            }
            
            try:
                for content in obs_manager._paginated_list_objects(bucket):
                    # Métricas generales
                    dashboard["metrics"]["total_objects"] += 1
                    dashboard["metrics"]["total_size_bytes"] += content.size
                    dashboard["metrics"]["storage_classes"][content.storageClass] += 1
                    
                    # Métricas del bucket
                    bucket_metrics["object_count"] += 1
                    bucket_metrics["total_size"] += content.size
                    bucket_metrics["storage_classes"][content.storageClass] += 1
                    
                    # Análisis de extensiones
                    if '.' in content.key:
                        ext = content.key.split('.')[-1].lower()
                        bucket_metrics["file_extensions"][ext] += 1
                        dashboard["metrics"]["file_types"][ext] += 1
                
                dashboard["metrics"]["buckets"][bucket] = dict(bucket_metrics)
                
            except Exception as e:
                print(f"Error procesando bucket {bucket}: {e}")
                dashboard["metrics"]["buckets"][bucket] = {"error": str(e)}
        
        # Convertir defaultdict a dict para JSON
        dashboard["metrics"]["storage_classes"] = dict(dashboard["metrics"]["storage_classes"])
        dashboard["metrics"]["file_types"] = dict(dashboard["metrics"]["file_types"])
        
        # Guardar dashboard
        with open("obs_dashboard.json", "w") as f:
            json.dump(dashboard, f, indent=2)
        
        # Mostrar resumen
        print("\n=== DASHBOARD DE MÉTRICAS ===")
        print(f"Total de objetos: {dashboard['metrics']['total_objects']:,}")
        print(f"Tamaño total: {dashboard['metrics']['total_size_bytes'] / (1024**3):.2f} GB")
        
        print("\nDistribución por Storage Class:")
        for storage_class, count in dashboard["metrics"]["storage_classes"].items():
            print(f"  {storage_class}: {count:,} objetos")
        
        print("\nTop 5 tipos de archivo:")
        sorted_types = sorted(
            dashboard["metrics"]["file_types"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        for ext, count in sorted_types:
            print(f"  .{ext}: {count:,} archivos")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    generate_dashboard()
```

## 🏢 Casos de Uso Empresariales

### Ejemplo 10: Auditoría de Cumplimiento

```python
#!/usr/bin/env python3
"""
Script de auditoría para cumplimiento normativo
"""
from obs_manager import OBSManager
from datetime import datetime, timedelta
import dateutil.parser
import csv

def compliance_audit():
    obs_manager = OBSManager()
    
    try:
        # Configuración de auditoría
        audit_config = {
            "retention_days": 2555,  # 7 años
            "sensitive_patterns": ["ssn", "credit", "personal", "confidential"],
            "required_encryption": True
        }
        
        audit_report = []
        now = datetime.now(tz=datetime.now().astimezone().tzinfo)
        retention_date = now - timedelta(days=audit_config["retention_days"])
        
        buckets_to_audit = ["customer-data", "financial-records", "hr-documents"]
        
        for bucket in buckets_to_audit:
            print(f"Auditando bucket: {bucket}")
            
            for content in obs_manager._paginated_list_objects(bucket):
                file_date = dateutil.parser.parse(content.lastModified)
                
                # Verificar retención
                retention_compliant = file_date > retention_date
                
                # Verificar patrones sensibles
                sensitive_data = any(pattern in content.key.lower() 
                                   for pattern in audit_config["sensitive_patterns"])
                
                # Verificar storage class apropiado para datos antiguos
                appropriate_storage = True
                if file_date < (now - timedelta(days=365)):  # Más de 1 año
                    appropriate_storage = content.storageClass in ["COLD", "WARM"]
                
                audit_entry = {
                    "bucket": bucket,
                    "object_key": content.key,
                    "last_modified": content.lastModified,
                    "size": content.size,
                    "storage_class": content.storageClass,
                    "retention_compliant": retention_compliant,
                    "contains_sensitive": sensitive_data,
                    "appropriate_storage": appropriate_storage,
                    "owner": content.owner.owner_name
                }
                
                audit_report.append(audit_entry)
        
        # Generar reporte CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"compliance_audit_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            if audit_report:
                writer = csv.DictWriter(file, fieldnames=audit_report[0].keys())
                writer.writeheader()
                writer.writerows(audit_report)
        
        # Resumen de cumplimiento
        total_files = len(audit_report)
        non_compliant = sum(1 for entry in audit_report if not entry["retention_compliant"])
        sensitive_files = sum(1 for entry in audit_report if entry["contains_sensitive"])
        inappropriate_storage = sum(1 for entry in audit_report if not entry["appropriate_storage"])
        
        print(f"\n=== REPORTE DE AUDITORÍA ===")
        print(f"Total de archivos auditados: {total_files:,}")
        print(f"Archivos fuera de retención: {non_compliant:,}")
        print(f"Archivos con datos sensibles: {sensitive_files:,}")
        print(f"Archivos con storage inapropiado: {inappropriate_storage:,}")
        print(f"Reporte guardado en: {csv_file}")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    compliance_audit()
```

## 🔧 Utilidades de Desarrollo

### Ejemplo 11: Testing y Validación

```python
#!/usr/bin/env python3
"""
Script de testing para validar funcionalidad de OBS
"""
from obs_manager import OBSManager
import tempfile
import os

def run_tests():
    obs_manager = OBSManager()
    test_bucket = "test-bucket"
    
    try:
        print("=== EJECUTANDO TESTS DE FUNCIONALIDAD ===")
        
        # Test 1: Conectividad
        print("Test 1: Verificando conectividad...")
        try:
            count = obs_manager.list_objects(test_bucket)
            print(f"✅ Conectividad OK - {count} objetos encontrados")
        except Exception as e:
            print(f"❌ Error de conectividad: {e}")
            return
        
        # Test 2: Búsqueda
        print("Test 2: Verificando búsqueda...")
        try:
            search_count = obs_manager.search_objects("test", test_bucket)
            print(f"✅ Búsqueda OK - {search_count} objetos encontrados")
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
        
        # Test 3: Descarga (si hay archivos)
        if count > 0:
            print("Test 3: Verificando descarga...")
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    download_count = obs_manager.download_objects(
                        test_bucket, 
                        "", 
                        temp_dir
                    )
                    print(f"✅ Descarga OK - {download_count} archivos descargados")
            except Exception as e:
                print(f"❌ Error en descarga: {e}")
        
        # Test 4: Validación de configuración
        print("Test 4: Verificando configuración...")
        if obs_manager.config.validate_credentials():
            print("✅ Configuración OK")
        else:
            print("❌ Configuración inválida")
        
        print("\n=== TESTS COMPLETADOS ===")
        
    finally:
        obs_manager.close()

if __name__ == "__main__":
    run_tests()
```

---

## 📝 Notas Importantes

1. **Seguridad**: Todos los ejemplos asumen que las credenciales están configuradas correctamente
2. **Rendimiento**: Los ejemplos incluyen paginación para manejar grandes volúmenes de datos
3. **Error Handling**: Cada ejemplo incluye manejo básico de errores
4. **Logging**: Se recomienda agregar logging detallado en implementaciones de producción
5. **Testing**: Siempre probar en entornos de desarrollo antes de producción

## 🔗 Referencias

- [Documentación Principal](README.md)
- [Guía de Instalación](QUICKSTART.md)
- [Configuración Avanzada](README.md#configuración-avanzada)
- [Solución de Problemas](README.md#solución-de-problemas)
