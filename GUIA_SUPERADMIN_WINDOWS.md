# 🔐 Guía del Superadministrador - Windows

## 👨‍💼 Perfil del Superadministrador

**Nivel de Acceso**: ADMIN (Nivel 4)  
**Responsabilidades**: Gestión completa del sistema, configuración de seguridad, administración de usuarios  
**Riesgo**: Crítico  

## 🚀 Instalación y Configuración Inicial

### Paso 1: Preparación del Sistema
```cmd
# Abrir PowerShell como Administrador
# Verificar versión de Python
python --version

# Si no tienes Python, descargar desde python.org
# Versión recomendada: Python 3.9 o superior
```

### Paso 2: Descarga e Instalación
```cmd
# Clonar el repositorio
git clone https://github.com/ccvass/obs-utils.git
cd obs-utils

# Ejecutar instalación automática
setup_secure.bat
```

### Paso 3: Configuración de Seguridad Avanzada
```cmd
# Configurar sistema de seguridad multinivel
python obs_utils_improved.py --enable-security-levels

# Establecer contraseña de administrador
python obs_utils_improved.py --set-admin-password

# Configurar encriptación AES-256
python obs_utils_improved.py --setup-secure-config
```

## 🔒 Gestión de Seguridad

### Configuración de Niveles de Seguridad

#### Nivel 1: READ_ONLY (Sin contraseña)
```cmd
# Operaciones permitidas sin autenticación
python obs_utils_improved.py --operation list --bucket mi-bucket
python obs_utils_improved.py --operation search --search-text "backup"
python obs_utils_improved.py --operation download --bucket mi-bucket
```

#### Nivel 2: STANDARD (Contraseña de Operador)
```cmd
# Configurar contraseña de operador
python obs_utils_improved.py --set-operator-password

# Operaciones de archivo y restauración
python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "archivos-antiguos/"
```

#### Nivel 3: DESTRUCTIVE (Contraseña de Supervisor)
```cmd
# Configurar contraseña de supervisor
python obs_utils_improved.py --set-supervisor-password

# Operaciones de eliminación
python obs_utils_improved.py --operation delete --bucket mi-bucket --prefix "temporal/"
```

#### Nivel 4: ADMIN (Contraseña de Administrador)
```cmd
# Operaciones administrativas críticas
python obs_utils_improved.py --operation create-bucket --bucket nuevo-bucket
python obs_utils_improved.py --operation configure-security --enable-encryption
```

### Políticas de Contraseñas

#### Contraseña de Operador
- **Longitud mínima**: 8 caracteres
- **Complejidad**: Letras y números
- **Rotación**: Cada 90 días

#### Contraseña de Supervisor
- **Longitud mínima**: 12 caracteres
- **Complejidad**: Letras, números y símbolos
- **Rotación**: Cada 60 días

#### Contraseña de Administrador
- **Longitud mínima**: 16 caracteres
- **Complejidad**: Mezcla fuerte de todos los tipos de caracteres
- **Rotación**: Cada 30 días

## 🛡️ Administración de Usuarios

### Crear Perfiles de Usuario
```cmd
# Crear perfil de operador
python obs_utils_improved.py --create-user-profile --role operator --name "Juan Perez"

# Crear perfil de supervisor
python obs_utils_improved.py --create-user-profile --role supervisor --name "Maria Garcia"

# Listar usuarios
python obs_utils_improved.py --list-users
```

### Gestión de Permisos
```cmd
# Asignar permisos específicos
python obs_utils_improved.py --assign-permissions --user "juan.perez" --level STANDARD

# Revocar permisos
python obs_utils_improved.py --revoke-permissions --user "juan.perez" --level DESTRUCTIVE

# Auditar permisos
python obs_utils_improved.py --audit-permissions --user "juan.perez"
```

## 📊 Monitoreo y Auditoría

### Configuración de Logs de Auditoría
```cmd
# Habilitar logging avanzado
python obs_utils_improved.py --configure-audit-logging --level DEBUG

# Configurar rotación de logs
python obs_utils_improved.py --configure-log-rotation --size 100MB --keep 30
```

### Revisión de Logs de Seguridad
```cmd
# Ver logs de seguridad
python obs_utils_improved.py --view-security-logs --last 24h

# Generar reporte de auditoría
python obs_utils_improved.py --generate-audit-report --period monthly

# Exportar logs para análisis
python obs_utils_improved.py --export-logs --format json --output audit_report.json
```

### Alertas de Seguridad
```cmd
# Configurar alertas por email
python obs_utils_improved.py --configure-alerts --email admin@empresa.com

# Configurar alertas Slack
python obs_utils_improved.py --configure-alerts --slack-webhook https://hooks.slack.com/...

# Configurar umbrales de alerta
python obs_utils_improved.py --set-alert-thresholds --failed-logins 3 --bulk-operations 100
```

## 🔧 Configuración Avanzada

### Archivo de Configuración Principal
```json
{
  "admin_config": {
    "security_levels": {
      "enabled": true,
      "enforce_password_policy": true,
      "session_timeout": 1800,
      "max_failed_attempts": 3,
      "lockout_duration": 900
    },
    "audit_logging": {
      "enabled": true,
      "log_level": "INFO",
      "log_file": "logs/security_audit.log",
      "max_file_size": "100MB",
      "backup_count": 30
    },
    "alerts": {
      "email_enabled": true,
      "email_recipients": ["admin@empresa.com", "security@empresa.com"],
      "slack_enabled": true,
      "slack_webhook": "https://hooks.slack.com/...",
      "alert_thresholds": {
        "failed_logins": 3,
        "bulk_operations": 100,
        "unusual_hours": true
      }
    },
    "backup": {
      "auto_backup": true,
      "backup_interval": "daily",
      "backup_location": "C:\\OBS_Backups\\",
      "retention_days": 30
    }
  }
}
```

### Variables de Entorno del Sistema
```cmd
# Configurar variables de entorno permanentes
setx OBS_ADMIN_MODE "true"
setx OBS_LOG_LEVEL "DEBUG"
setx OBS_BACKUP_PATH "C:\OBS_Backups"
setx OBS_ALERT_EMAIL "admin@empresa.com"
```

## 🚨 Gestión de Incidentes

### Procedimiento de Respuesta a Incidentes

#### Paso 1: Detección
```cmd
# Verificar alertas de seguridad
python obs_utils_improved.py --check-security-alerts

# Revisar logs de actividad sospechosa
python obs_utils_improved.py --scan-suspicious-activity --last 24h
```

#### Paso 2: Contención
```cmd
# Bloquear usuario comprometido
python obs_utils_improved.py --lock-user --username "usuario_comprometido"

# Revocar sesiones activas
python obs_utils_improved.py --revoke-all-sessions --user "usuario_comprometido"

# Cambiar contraseñas de emergencia
python obs_utils_improved.py --emergency-password-reset --all-levels
```

#### Paso 3: Investigación
```cmd
# Generar reporte detallado del incidente
python obs_utils_improved.py --incident-report --user "usuario_comprometido" --timeframe "last 7 days"

# Exportar evidencia forense
python obs_utils_improved.py --export-forensic-data --incident-id "INC-2025-001"
```

#### Paso 4: Recuperación
```cmd
# Restaurar configuración desde backup
python obs_utils_improved.py --restore-config --backup-date "2025-07-10"

# Verificar integridad del sistema
python obs_utils_improved.py --system-integrity-check

# Reactivar servicios
python obs_utils_improved.py --restart-services --verify-security
```

## 📋 Tareas de Mantenimiento

### Mantenimiento Diario
```cmd
# Verificar estado del sistema
python obs_utils_improved.py --system-health-check

# Revisar logs de seguridad
python obs_utils_improved.py --review-security-logs --today

# Verificar backups
python obs_utils_improved.py --verify-backups --last 24h
```

### Mantenimiento Semanal
```cmd
# Generar reporte semanal
python obs_utils_improved.py --weekly-report --email admin@empresa.com

# Actualizar definiciones de seguridad
python obs_utils_improved.py --update-security-definitions

# Optimizar base de datos de logs
python obs_utils_improved.py --optimize-log-database
```

### Mantenimiento Mensual
```cmd
# Auditoría completa de seguridad
python obs_utils_improved.py --full-security-audit

# Rotación de claves de encriptación
python obs_utils_improved.py --rotate-encryption-keys

# Limpieza de logs antiguos
python obs_utils_improved.py --cleanup-old-logs --older-than 90days
```

## 🔄 Backup y Recuperación

### Configuración de Backup Automático
```cmd
# Configurar backup automático
python obs_utils_improved.py --configure-auto-backup --schedule daily --time "02:00"

# Configurar ubicación de backup
python obs_utils_improved.py --set-backup-location --path "C:\OBS_Backups"

# Configurar retención de backups
python obs_utils_improved.py --set-backup-retention --days 30
```

### Backup Manual
```cmd
# Backup completo del sistema
python obs_utils_improved.py --full-backup --include-logs --include-config

# Backup solo de configuración
python obs_utils_improved.py --backup-config --encrypt

# Backup de base de datos de usuarios
python obs_utils_improved.py --backup-user-database --compress
```

### Recuperación de Desastres
```cmd
# Restaurar desde backup completo
python obs_utils_improved.py --restore-full-backup --backup-file "backup_2025-07-10.enc"

# Restaurar solo configuración
python obs_utils_improved.py --restore-config --backup-file "config_backup_2025-07-10.json"

# Verificar integridad después de restauración
python obs_utils_improved.py --verify-restore --check-all
```

## 📞 Soporte y Escalación

### Contactos de Emergencia
- **Equipo de Seguridad**: security@ccvass.com
- **Soporte Técnico**: support@ccvass.com
- **Emergencias 24/7**: +51-xxx-xxx-xxxx

### Procedimiento de Escalación
1. **Nivel 1**: Operador → Supervisor
2. **Nivel 2**: Supervisor → Administrador
3. **Nivel 3**: Administrador → Equipo de Seguridad
4. **Nivel 4**: Equipo de Seguridad → Dirección Técnica

### Documentación Adicional
- [Guía de Seguridad Completa](SECURITY.md)
- [Manual de Operador](GUIA_OPERADOR_WINDOWS.md)
- [Inicio Rápido](INICIO_RAPIDO_WINDOWS.md)
- [Solución de Problemas](docs/es/SOLUCION_PROBLEMAS.md)

## ✅ Lista de Verificación del Superadministrador

### Configuración Inicial
- [ ] Python 3.9+ instalado
- [ ] OBS Utils descargado e instalado
- [ ] Configuración de seguridad multinivel habilitada
- [ ] Contraseñas de todos los niveles establecidas
- [ ] Encriptación AES-256 configurada
- [ ] Variables de entorno configuradas

### Configuración de Usuarios
- [ ] Perfiles de usuario creados
- [ ] Permisos asignados correctamente
- [ ] Políticas de contraseñas aplicadas
- [ ] Sesiones de usuario configuradas

### Monitoreo y Auditoría
- [ ] Logging de auditoría habilitado
- [ ] Alertas de seguridad configuradas
- [ ] Rotación de logs configurada
- [ ] Reportes automáticos programados

### Backup y Recuperación
- [ ] Backup automático configurado
- [ ] Ubicación de backup segura
- [ ] Procedimientos de recuperación probados
- [ ] Documentación de recuperación actualizada

### Mantenimiento
- [ ] Tareas de mantenimiento programadas
- [ ] Procedimientos de incidentes documentados
- [ ] Contactos de emergencia actualizados
- [ ] Documentación del sistema actualizada

---

**Desarrollado por**: CCVASS - Lima, Perú 🇵🇪  
**Contacto**: contact@ccvass.com  
**Versión**: 2.0.0  
**Última Actualización**: Julio 2025
