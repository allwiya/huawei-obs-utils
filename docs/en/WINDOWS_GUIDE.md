# OBS Utils - Guía Completa para Windows

Esta guía está específicamente diseñada para usuarios de Windows que quieren usar OBS Utils de manera sencilla y completa.

## 🚀 Instalación Rápida

### Paso 1: Descargar Python
1. Ve a https://python.org/downloads/
2. Descarga Python 3.7 o superior
3. **IMPORTANTE**: Durante la instalación, marca "Add Python to PATH"

### Paso 2: Descargar OBS Utils
1. Descarga el proyecto como ZIP
2. Extrae en una carpeta (ej: `C:\obs_utils`)

### Paso 3: Instalación Automática
1. Abre **Command Prompt** (cmd):
   - Presiona `Win + R`
   - Escribe `cmd` y presiona Enter
2. Navega a la carpeta:
   ```cmd
   cd C:\obs_utils
   ```
3. Ejecuta la instalación:
   ```cmd
   setup.bat
   ```

¡Listo! El script configurará todo automáticamente.

## ⚙️ Configuración de Credenciales

### Opción 1: Archivo de Configuración (Más Fácil)
1. Abre el archivo `obs_config.json` con Notepad:
   ```cmd
   notepad obs_config.json
   ```
2. Reemplaza los valores con tus credenciales:
   ```json
   {
     "access_key_id": "TU_ACCESS_KEY_AQUI",
     "secret_access_key": "TU_SECRET_KEY_AQUI",
     "server": "https://obs.sa-peru-1.myhuaweicloud.com/",
     "region": "sa-peru-1"
   }
   ```
3. Guarda el archivo (Ctrl+S)

### Opción 2: Variables de Entorno
En Command Prompt:
```cmd
set OBS_ACCESS_KEY_ID=tu_access_key
set OBS_SECRET_ACCESS_KEY=tu_secret_key
set OBS_SERVER=https://obs.sa-peru-1.myhuaweicloud.com/
set OBS_REGION=sa-peru-1
```

En PowerShell:
```powershell
$env:OBS_ACCESS_KEY_ID="tu_access_key"
$env:OBS_SECRET_ACCESS_KEY="tu_secret_key"
$env:OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
$env:OBS_REGION="sa-peru-1"
```

## 🎯 Uso Básico

### Modo Fácil (Recomendado)
Simplemente ejecuta:
```cmd
run.bat
```

Esto abrirá el modo interactivo que te guiará paso a paso.

### Comandos Directos
```cmd
# Listar archivos de un bucket
run.bat --operation list --bucket mi-bucket

# Descargar archivos
run.bat --operation download --bucket mi-bucket --prefix "carpeta/"

# Buscar archivos
run.bat --operation search --search-text "backup"
```

## 📚 Métodos Disponibles para Windows

### 1. Listar Objetos (`list`)

**Descripción**: Lista todos los archivos en un bucket.

**Comando básico**:
```cmd
run.bat --operation list --bucket mi-bucket
```

**Con filtro de carpeta**:
```cmd
run.bat --operation list --bucket mi-bucket --prefix "documentos\"
```

**Ejemplos prácticos**:
```cmd
# Ver todos los archivos del bucket "empresa"
run.bat --operation list --bucket empresa

# Ver solo archivos de la carpeta "reportes"
run.bat --operation list --bucket empresa --prefix "reportes\"

# Ver archivos de subcarpeta específica
run.bat --operation list --bucket empresa --prefix "reportes\2024\"
```

### 2. Cambiar Clase de Almacenamiento

#### Archivar (`archive`) - Almacenamiento Más Barato
**Descripción**: Mueve archivos a almacenamiento COLD (más barato, requiere restauración).

```cmd
# Archivar todos los archivos de un bucket
run.bat --operation archive --bucket mi-bucket

# Archivar solo una carpeta específica
run.bat --operation archive --bucket mi-bucket --prefix "archivos-2023\"

# Archivar archivos de backup antiguos
run.bat --operation archive --bucket backups --prefix "backup-2023\"
```

#### Acceso Infrecuente (`warm`) - Costo Medio
**Descripción**: Mueve archivos a almacenamiento WARM (costo medio, acceso inmediato).

```cmd
# Mover archivos a WARM storage
run.bat --operation warm --bucket mi-bucket --prefix "datos-historicos\"

# Optimizar costos de archivos de logs
run.bat --operation warm --bucket logs --prefix "application-logs\"
```

### 3. Restaurar Objetos Archivados (`restore`)

**Descripción**: Restaura archivos archivados para acceso temporal.

**Restauración básica** (30 días, velocidad rápida):
```cmd
run.bat --operation restore --bucket mi-bucket --prefix "archivos-2023\"
```

**Restauración personalizada**:
```cmd
# Restauración rápida por 7 días
run.bat --operation restore --bucket mi-bucket --prefix "urgente\" --days 7 --tier "Expedited"

# Restauración estándar por 30 días
run.bat --operation restore --bucket mi-bucket --prefix "normales\" --days 30 --tier "Standard"

# Restauración masiva por 90 días (más barata)
run.bat --operation restore --bucket mi-bucket --prefix "historicos\" --days 90 --tier "Bulk"
```

**Opciones de velocidad**:
- `Expedited`: 1-5 minutos (más caro)
- `Standard`: 3-5 horas (costo medio)
- `Bulk`: 5-12 horas (más barato)

### 4. Descargar Archivos (`download`)

#### Descargar Múltiples Archivos
**Descripción**: Descarga archivos manteniendo la estructura de carpetas.

```cmd
# Descargar todos los archivos de un bucket
run.bat --operation download --bucket mi-bucket --download-path "C:\Descargas\"

# Descargar una carpeta específica
run.bat --operation download --bucket mi-bucket --prefix "reportes\" --download-path "C:\Documentos\Reportes\"

# Descargar manteniendo estructura original
run.bat --operation download --bucket mi-bucket --prefix "proyecto\"
```

#### Descargar Archivo Específico
```cmd
# Descargar un archivo específico
run.bat --operation download --bucket mi-bucket --object-key "documento.pdf" --download-path "C:\Documentos\"

# Descargar con nombre personalizado
run.bat --operation download --bucket mi-bucket --object-key "reporte.xlsx" --download-path "C:\Documentos\reporte_local.xlsx"
```

**Consejos para rutas en Windows**:
- Usa comillas para rutas con espacios: `"C:\Mis Documentos\"`
- Usa barras invertidas: `\` no `/`
- Termina las carpetas con `\`

### 5. Buscar Archivos (`search`)

**Descripción**: Busca archivos por nombre en buckets.

```cmd
# Buscar en todos los buckets
run.bat --operation search --search-text "backup"

# Buscar en bucket específico
run.bat --operation search --search-text "log" --bucket mi-bucket

# Buscar en carpeta específica
run.bat --operation search --search-text "config" --bucket mi-bucket --prefix "aplicacion\"

# Buscar archivos por extensión
run.bat --operation search --search-text ".pdf" --bucket documentos
```

**Ejemplos de búsqueda**:
```cmd
# Encontrar todos los archivos de Excel
run.bat --operation search --search-text ".xlsx"

# Buscar archivos de configuración
run.bat --operation search --search-text "config" --bucket sistema

# Encontrar backups de base de datos
run.bat --operation search --search-text "database_backup" --bucket backups
```

## 📋 Tabla de Comandos Rápidos

| Operación | Comando Base | Ejemplo |
|-----------|--------------|---------|
| **Listar** | `--operation list` | `run.bat --operation list --bucket docs` |
| **Archivar** | `--operation archive` | `run.bat --operation archive --bucket old-files` |
| **WARM Storage** | `--operation warm` | `run.bat --operation warm --bucket logs` |
| **Restaurar** | `--operation restore` | `run.bat --operation restore --bucket archive` |
| **Descargar** | `--operation download` | `run.bat --operation download --bucket files` |
| **Buscar** | `--operation search` | `run.bat --operation search --search-text "backup"` |

## 🎯 Parámetros Disponibles

| Parámetro | Descripción | Ejemplo Windows |
|-----------|-------------|-----------------|
| `--bucket` | Nombre del bucket | `--bucket "mi-bucket"` |
| `--prefix` | Carpeta/prefijo | `--prefix "documentos\"` |
| `--object-key` | Archivo específico | `--object-key "archivo.txt"` |
| `--download-path` | Ruta de descarga | `--download-path "C:\Descargas\"` |
| `--search-text` | Texto a buscar | `--search-text "backup"` |
| `--days` | Días para restauración | `--days 30` |
| `--tier` | Velocidad de restauración | `--tier "Expedited"` |
| `--config` | Archivo de configuración | `--config "mi_config.json"` |

## 💼 Ejemplos Prácticos para Windows

### Ejemplo 1: Gestión de Documentos de Oficina

```cmd
REM Listar todos los documentos
run.bat --operation list --bucket documentos-empresa

REM Buscar archivos de Word
run.bat --operation search --search-text ".docx" --bucket documentos-empresa

REM Descargar reportes mensuales
run.bat --operation download --bucket documentos-empresa --prefix "reportes\2024\" --download-path "C:\Documentos\Reportes\"

REM Archivar documentos del año pasado para ahorrar dinero
run.bat --operation archive --bucket documentos-empresa --prefix "documentos\2023\"
```

### Ejemplo 2: Gestión de Backups

```cmd
REM Ver todos los backups disponibles
run.bat --operation list --bucket backups-sistema

REM Buscar backups de base de datos
run.bat --operation search --search-text "database" --bucket backups-sistema

REM Descargar backup específico
run.bat --operation download --bucket backups-sistema --object-key "backup_20240710.sql" --download-path "C:\Backups\"

REM Archivar backups antiguos (más de 3 meses)
run.bat --operation archive --bucket backups-sistema --prefix "backups\2024\01\"
```

### Ejemplo 3: Gestión de Archivos Multimedia

```cmd
REM Listar fotos y videos
run.bat --operation list --bucket multimedia --prefix "fotos\"

REM Buscar videos MP4
run.bat --operation search --search-text ".mp4" --bucket multimedia

REM Descargar álbum de fotos específico
run.bat --operation download --bucket multimedia --prefix "fotos\vacaciones-2024\" --download-path "C:\Fotos\"

REM Mover videos antiguos a almacenamiento WARM (más barato)
run.bat --operation warm --bucket multimedia --prefix "videos\2023\"
```

## 🤖 Scripts de Automatización para Windows

### Script Batch para Backup Diario

Crear archivo `backup_diario.bat`:
```cmd
@echo off
echo ========================================
echo    BACKUP DIARIO AUTOMATICO
echo ========================================
echo.

REM Configurar fecha
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "datestamp=%YYYY%-%MM%-%DD%"

echo Fecha: %datestamp%
echo.

REM Crear carpeta de backup local
if not exist "C:\Backup\%datestamp%" mkdir "C:\Backup\%datestamp%"

echo Descargando archivos importantes...
run.bat --operation download --bucket documentos --prefix "importantes\" --download-path "C:\Backup\%datestamp%\"

echo.
echo Archivando archivos antiguos para ahorrar costos...
run.bat --operation archive --bucket documentos --prefix "archivos-viejos\"

echo.
echo ========================================
echo    BACKUP COMPLETADO
echo ========================================
pause
```

### Script PowerShell para Monitoreo

Crear archivo `monitoreo.ps1`:
```powershell
# Script de monitoreo para OBS
Write-Host "=== MONITOREO DE BUCKETS ===" -ForegroundColor Green

$buckets = @("documentos", "backups", "multimedia")

foreach ($bucket in $buckets) {
    Write-Host "`nVerificando bucket: $bucket" -ForegroundColor Yellow
    
    # Ejecutar comando y capturar salida
    $output = & .\run.bat --operation list --bucket $bucket 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Bucket $bucket: OK" -ForegroundColor Green
    } else {
        Write-Host "❌ Bucket $bucket: ERROR" -ForegroundColor Red
        Write-Host $output
    }
}

Write-Host "`n=== MONITOREO COMPLETADO ===" -ForegroundColor Green
Read-Host "Presiona Enter para continuar"
```

## 📊 Casos de Uso Empresariales

### 1. Departamento de Contabilidad

```cmd
REM Gestión de facturas y documentos contables
echo === GESTION CONTABLE ===

REM Listar facturas del mes actual
run.bat --operation list --bucket contabilidad --prefix "facturas\2024\07\"

REM Buscar facturas de un proveedor específico
run.bat --operation search --search-text "proveedor_abc" --bucket contabilidad

REM Descargar documentos para auditoría
run.bat --operation download --bucket contabilidad --prefix "auditoria\" --download-path "C:\Auditoria\"

REM Archivar documentos del año fiscal anterior
run.bat --operation archive --bucket contabilidad --prefix "documentos\2023\"
```

### 2. Departamento de Recursos Humanos

```cmd
REM Gestión de documentos de empleados
echo === RECURSOS HUMANOS ===

REM Listar expedientes de empleados
run.bat --operation list --bucket rrhh --prefix "expedientes\"

REM Buscar contratos
run.bat --operation search --search-text "contrato" --bucket rrhh

REM Descargar documentos de nómina
run.bat --operation download --bucket rrhh --prefix "nomina\2024\" --download-path "C:\RRHH\Nomina\"

REM Mover documentos antiguos a almacenamiento WARM
run.bat --operation warm --bucket rrhh --prefix "expedientes\inactivos\"
```

## 🔧 Configuración Avanzada para Windows

### Variables de Entorno Permanentes

Para configurar variables de entorno permanentes en Windows:

**Método Command Prompt** (como administrador):
```cmd
setx OBS_ACCESS_KEY_ID "tu_access_key" /M
setx OBS_SECRET_ACCESS_KEY "tu_secret_key" /M
setx OBS_SERVER "https://obs.sa-peru-1.myhuaweicloud.com/" /M
setx OBS_REGION "sa-peru-1" /M
```

**Método PowerShell** (como administrador):
```powershell
[Environment]::SetEnvironmentVariable("OBS_ACCESS_KEY_ID", "tu_access_key", "Machine")
[Environment]::SetEnvironmentVariable("OBS_SECRET_ACCESS_KEY", "tu_secret_key", "Machine")
[Environment]::SetEnvironmentVariable("OBS_SERVER", "https://obs.sa-peru-1.myhuaweicloud.com/", "Machine")
[Environment]::SetEnvironmentVariable("OBS_REGION", "sa-peru-1", "Machine")
```

## 📁 Estructura de Carpetas Recomendada

```
C:\obs_utils\
├── run.bat                    ← Script principal
├── setup.bat                  ← Instalación
├── obs_config.json           ← Configuración
├── logs\                     ← Logs automáticos
├── scripts\                  ← Tus scripts personalizados
│   ├── backup_diario.bat
│   ├── limpieza_semanal.bat
│   └── monitoreo.ps1
├── downloads\                ← Descargas por defecto
├── temp\                     ← Archivos temporales
└── venv\                     ← Entorno Python
```

## 🆘 Solución de Problemas Específicos de Windows

### Error: "Python no se reconoce como comando"
**Solución completa**:
1. Desinstalar Python actual
2. Descargar Python desde https://python.org/downloads/
3. Durante la instalación, **marcar "Add Python to PATH"**
4. Reiniciar Command Prompt
5. Verificar: `python --version`

### Error: "Invalid credentials"
**Verificación paso a paso**:
```cmd
REM 1. Verificar que el archivo existe
dir obs_config.json

REM 2. Ver contenido del archivo
type obs_config.json

REM 3. Editar si es necesario
notepad obs_config.json

REM 4. Probar conexión
run.bat --operation list --bucket test-bucket
```

### Ver Logs Detallados
```cmd
REM Ver el último archivo de log
for /f %%i in ('dir /b /od logs\obs_utils_*.log') do set newest=%%i
type "logs\%newest%"

REM Buscar errores específicos
findstr /i "error" logs\obs_utils_*.log

REM Ver logs en tiempo real (PowerShell)
Get-Content logs\obs_utils_*.log -Wait -Tail 10
```

## 💡 Consejos Avanzados para Windows

### 1. Uso de Variables de Entorno
```cmd
REM Usar variables de entorno para rutas
run.bat --operation download --bucket docs --download-path "%USERPROFILE%\Documents\"

REM Usar fecha actual en nombres
set TODAY=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%
run.bat --operation download --bucket backups --download-path "C:\Backup\%TODAY%\"
```

### 2. Procesamiento por Lotes
```cmd
REM Procesar múltiples buckets
for %%b in (bucket1 bucket2 bucket3) do (
    echo Procesando %%b...
    run.bat --operation list --bucket %%b
)
```

### 3. Integración con Tareas Programadas
1. Abrir "Programador de tareas" (`taskschd.msc`)
2. Crear tarea básica
3. Configurar programa: `C:\obs_utils\backup_diario.bat`
4. Establecer frecuencia (diaria, semanal, etc.)

## 📞 Ayuda y Soporte

### Comandos de Ayuda
```cmd
REM Ver todas las opciones disponibles
run.bat --help

REM Ejecutar en modo interactivo (más fácil)
run.bat

REM Crear archivo de configuración de ejemplo
run.bat --create-config
```

### Información del Sistema
```cmd
REM Verificar versión de Python
python --version

REM Verificar variables de entorno
echo %OBS_ACCESS_KEY_ID%
echo %OBS_SECRET_ACCESS_KEY%

REM Ver información del sistema
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
```

---

**¿Necesitas más ayuda específica para Windows?** 
- Ejecuta `run.bat` sin parámetros para el modo interactivo
- Revisa los archivos de log en `logs\` para detalles de errores
- Usa PowerShell para comandos más avanzados
- Consulta la documentación completa en `README.md`
