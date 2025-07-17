@echo off
REM OBS Utils - Secure Installation Script for Windows
REM Instalador seguro con configuración encriptada y niveles de usuario
REM 
REM Copyright 2025 CCVASS - Lima, Peru
REM Licensed under Apache License 2.0
REM Contact: contact@ccvass.com

setlocal enabledelayedexpansion

REM Configurar colores (si está disponible)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Función para mostrar header
:print_header
echo ================================================
echo   OBS Utils - Instalación Segura (Windows)
echo   CCVASS - Lima, Peru (2025)
echo ================================================
echo.
goto :eof

REM Función para mostrar éxito
:print_success
echo %GREEN%✓ %~1%NC%
goto :eof

REM Función para mostrar advertencia
:print_warning
echo %YELLOW%⚠ %~1%NC%
goto :eof

REM Función para mostrar error
:print_error
echo %RED%✗ %~1%NC%
goto :eof

REM Función para mostrar información
:print_info
echo %BLUE%ℹ %~1%NC%
goto :eof

REM Verificar requisitos del sistema
:check_requirements
call :print_info "Verificando requisitos del sistema..."

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Python no está instalado o no está en PATH"
    echo.
    echo Por favor instala Python 3.9 o superior desde:
    echo https://python.org/downloads/
    echo.
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

REM Obtener versión de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
call :print_success "Python %python_version% encontrado"

REM Verificar pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    call :print_error "pip no está disponible"
    echo Reinstala Python con pip incluido
    pause
    exit /b 1
)

call :print_success "pip disponible"
goto :eof

REM Configurar entorno virtual
:setup_virtual_environment
call :print_info "Configurando entorno virtual..."

if not exist "venv" (
    python -m venv venv
    call :print_success "Entorno virtual creado"
) else (
    call :print_info "Entorno virtual ya existe"
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Actualizar pip
python -m pip install --upgrade pip >nul 2>&1

REM Instalar dependencias
if exist "requirements.txt" (
    pip install -r requirements.txt >nul 2>&1
    call :print_success "Dependencias instaladas"
) else (
    pip install cryptography esdk-obs-python >nul 2>&1
    call :print_success "Dependencias básicas instaladas"
)
goto :eof

REM Configurar permisos seguros
:setup_secure_permissions
call :print_info "Configurando estructura de directorios..."

REM Crear directorio de logs
if not exist "logs" mkdir logs

call :print_success "Estructura configurada"
goto :eof

REM Seleccionar tipo de usuario
:select_user_type
echo.
call :print_info "Selecciona el tipo de usuario para configurar los niveles de seguridad:"
echo.
echo 1. 👤 Usuario Básico (READ_ONLY)
echo    - Operaciones: listar, buscar, descargar
echo    - Sin contraseña adicional requerida
echo.
echo 2. 👨‍💼 Usuario Estándar (STANDARD)
echo    - Operaciones: archivar, restaurar, cambiar clase de almacenamiento
echo    - Contraseña de nivel estándar requerida
echo.
echo 3. 🔧 Usuario Avanzado (DESTRUCTIVE)
echo    - Operaciones: eliminar objetos, purgar buckets
echo    - Contraseña de nivel destructivo requerida
echo.
echo 4. 👑 Administrador (ADMIN)
echo    - Operaciones: gestión completa de buckets y permisos
echo    - Contraseña de administrador requerida
echo.
echo 5. 🏢 Configuración Empresarial (Todos los niveles)
echo    - Configurar todos los niveles de seguridad
echo    - Múltiples contraseñas por nivel
echo.

:select_user_loop
set /p user_choice="Selecciona una opción (1-5): "
if "%user_choice%"=="1" goto :user_selected
if "%user_choice%"=="2" goto :user_selected
if "%user_choice%"=="3" goto :user_selected
if "%user_choice%"=="4" goto :user_selected
if "%user_choice%"=="5" goto :user_selected
call :print_error "Opción inválida. Selecciona 1-5."
goto :select_user_loop

:user_selected
echo.
goto :eof

REM Configurar credenciales OBS
:setup_obs_credentials
call :print_info "Configurando credenciales de Huawei Cloud OBS..."
echo.

set /p access_key_id="Access Key ID: "
if "%access_key_id%"=="" (
    call :print_error "Access Key ID es obligatorio"
    goto :setup_obs_credentials
)

REM Para Windows, usamos un método alternativo para ocultar la contraseña
call :print_info "Ingresa Secret Access Key (se ocultará):"
powershell -Command "$secureString = Read-Host 'Secret Access Key' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $secret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $secret" > temp_secret.txt
set /p secret_access_key=<temp_secret.txt
del temp_secret.txt

if "%secret_access_key%"=="" (
    call :print_error "Secret Access Key es obligatorio"
    goto :setup_obs_credentials
)

set /p obs_server="Servidor OBS [https://obs.sa-peru-1.myhuaweicloud.com/]: "
if "%obs_server%"=="" set obs_server=https://obs.sa-peru-1.myhuaweicloud.com/

set /p obs_region="Región [sa-peru-1]: "
if "%obs_region%"=="" set obs_region=sa-peru-1

REM Crear configuración temporal
(
echo {
echo     "access_key_id": "%access_key_id%",
echo     "secret_access_key": "%secret_access_key%",
echo     "server": "%obs_server%",
echo     "region": "%obs_region%",
echo     "max_keys": 1000,
echo     "restore_days": 30,
echo     "restore_tier": "Expedited"
echo }
) > temp_config.json

call :print_success "Credenciales configuradas"
goto :eof

REM Configurar encriptación
:setup_encryption
call :print_info "Configurando encriptación de credenciales..."
echo.

REM Solicitar contraseña maestra usando PowerShell
:master_password_loop
call :print_info "Ingresa contraseña maestra para encriptar credenciales:"
powershell -Command "$secureString = Read-Host 'Contraseña maestra' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_master.txt
set /p master_password=<temp_master.txt
del temp_master.txt

powershell -Command "$secureString = Read-Host 'Confirmar contraseña maestra' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_master_confirm.txt
set /p master_password_confirm=<temp_master_confirm.txt
del temp_master_confirm.txt

if not "%master_password%"=="%master_password_confirm%" (
    call :print_error "Las contraseñas no coinciden. Intenta nuevamente."
    echo.
    goto :master_password_loop
)

REM Configurar contraseñas por nivel según el tipo de usuario
if "%user_choice%"=="1" call :setup_basic_user_passwords
if "%user_choice%"=="2" call :setup_standard_user_passwords
if "%user_choice%"=="3" call :setup_advanced_user_passwords
if "%user_choice%"=="4" call :setup_admin_user_passwords
if "%user_choice%"=="5" call :setup_enterprise_passwords

REM Encriptar configuración usando Python
python -c "
import sys
import json
import os
from security import ConfigSecurity
from security_levels import MultiLevelSecurity

# Cargar configuración temporal
with open('temp_config.json', 'r') as f:
    config_data = json.load(f)

# Crear configuración encriptada
security = ConfigSecurity()
if security.create_encrypted_config(config_data, password='%master_password%'):
    print('✓ Configuración encriptada creada exitosamente')
else:
    print('✗ Error al crear configuración encriptada')
    sys.exit(1)

# Limpiar archivo temporal
os.remove('temp_config.json')
"

if errorlevel 1 (
    call :print_error "Error al encriptar configuración"
    exit /b 1
)

call :print_success "Configuración encriptada completada"
goto :eof

REM Configurar contraseñas para usuario básico
:setup_basic_user_passwords
call :print_info "Configuración de Usuario Básico - Solo operaciones de lectura"
echo No se requieren contraseñas adicionales para operaciones básicas.
goto :eof

REM Configurar contraseñas para usuario estándar
:setup_standard_user_passwords
call :print_info "Configuración de Usuario Estándar"
echo.
powershell -Command "$secureString = Read-Host 'Contraseña para operaciones estándar' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_std.txt
set /p standard_password=<temp_std.txt
del temp_std.txt

python -c "
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
password_hash = hashlib.sha256('%standard_password%'.encode()).hexdigest()
security.set_level_password(SecurityLevel.STANDARD, password_hash)
security.save_security_config('%master_password%')
"
goto :eof

REM Configurar contraseñas para usuario avanzado
:setup_advanced_user_passwords
call :print_info "Configuración de Usuario Avanzado"
echo.
powershell -Command "$secureString = Read-Host 'Contraseña para operaciones estándar' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_std.txt
set /p standard_password=<temp_std.txt
del temp_std.txt

powershell -Command "$secureString = Read-Host 'Contraseña para operaciones destructivas' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_dest.txt
set /p destructive_password=<temp_dest.txt
del temp_dest.txt

python -c "
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
std_hash = hashlib.sha256('%standard_password%'.encode()).hexdigest()
dest_hash = hashlib.sha256('%destructive_password%'.encode()).hexdigest()

security.set_level_password(SecurityLevel.STANDARD, std_hash)
security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
security.save_security_config('%master_password%')
"
goto :eof

REM Configurar contraseñas para administrador
:setup_admin_user_passwords
call :print_info "Configuración de Administrador"
echo.
powershell -Command "$secureString = Read-Host 'Contraseña para operaciones estándar' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_std.txt
set /p standard_password=<temp_std.txt
del temp_std.txt

powershell -Command "$secureString = Read-Host 'Contraseña para operaciones destructivas' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_dest.txt
set /p destructive_password=<temp_dest.txt
del temp_dest.txt

powershell -Command "$secureString = Read-Host 'Contraseña de administrador' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_admin.txt
set /p admin_password=<temp_admin.txt
del temp_admin.txt

python -c "
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
std_hash = hashlib.sha256('%standard_password%'.encode()).hexdigest()
dest_hash = hashlib.sha256('%destructive_password%'.encode()).hexdigest()
admin_hash = hashlib.sha256('%admin_password%'.encode()).hexdigest()

security.set_level_password(SecurityLevel.STANDARD, std_hash)
security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
security.set_level_password(SecurityLevel.ADMIN, admin_hash)
security.save_security_config('%master_password%')
"
goto :eof

REM Configurar contraseñas empresariales
:setup_enterprise_passwords
call :print_info "Configuración Empresarial - Todos los niveles de seguridad"
echo.
powershell -Command "$secureString = Read-Host 'Contraseña para operaciones estándar' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_std.txt
set /p standard_password=<temp_std.txt
del temp_std.txt

powershell -Command "$secureString = Read-Host 'Contraseña para operaciones destructivas' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_dest.txt
set /p destructive_password=<temp_dest.txt
del temp_dest.txt

powershell -Command "$secureString = Read-Host 'Contraseña de administrador' -AsSecureString; $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString); $password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR); [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR); $password" > temp_admin.txt
set /p admin_password=<temp_admin.txt
del temp_admin.txt

python -c "
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
std_hash = hashlib.sha256('%standard_password%'.encode()).hexdigest()
dest_hash = hashlib.sha256('%destructive_password%'.encode()).hexdigest()
admin_hash = hashlib.sha256('%admin_password%'.encode()).hexdigest()

security.set_level_password(SecurityLevel.STANDARD, std_hash)
security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
security.set_level_password(SecurityLevel.ADMIN, admin_hash)
security.save_security_config('%master_password%')
"

call :print_success "Configuración empresarial completada"
goto :eof

REM Crear scripts de acceso rápido
:create_launcher_scripts
call :print_info "Creando scripts de acceso rápido..."

REM Script de activación del entorno
(
echo @echo off
echo REM Script de activación para OBS Utils
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo echo Entorno OBS Utils activado
echo echo Usa: python obs_utils_improved.py [opciones]
echo cmd /k
) > activate_obs.bat

REM Script de ejecución directa
(
echo @echo off
echo REM Launcher directo para OBS Utils
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python obs_utils_improved.py %%*
) > obs.bat

call :print_success "Scripts de acceso creados: activate_obs.bat y obs.bat"
goto :eof

REM Mostrar resumen de instalación
:show_installation_summary
echo.
call :print_header
call :print_success "¡Instalación completada exitosamente!"
echo.

if "%user_choice%"=="1" echo 👤 Configurado como: Usuario Básico (READ_ONLY)
if "%user_choice%"=="2" echo 👨‍💼 Configurado como: Usuario Estándar (STANDARD)
if "%user_choice%"=="3" echo 🔧 Configurado como: Usuario Avanzado (DESTRUCTIVE)
if "%user_choice%"=="4" echo 👑 Configurado como: Administrador (ADMIN)
if "%user_choice%"=="5" echo 🏢 Configurado como: Configuración Empresarial (Todos los niveles)

echo.
call :print_info "Archivos de configuración creados:"
echo   📁 obs_config.json.enc (credenciales encriptadas)
echo   🔑 obs_config.json.salt (salt de encriptación)
echo   🛡️  obs_security_levels.json.enc (niveles de seguridad)
echo.

call :print_info "Formas de usar OBS Utils:"
echo   1. Modo interactivo: obs.bat
echo   2. Línea de comandos: obs.bat --operation list --bucket mi-bucket
echo   3. Activar entorno: activate_obs.bat
echo   4. Manual: venv\Scripts\activate.bat ^&^& python obs_utils_improved.py
echo.

call :print_warning "IMPORTANTE:"
echo   • Guarda tu contraseña maestra de forma segura
echo   • Las contraseñas no se pueden recuperar si se pierden
echo   • Los archivos .enc y .salt son necesarios para el funcionamiento
echo.

call :print_info "Para obtener ayuda: obs.bat --help"
call :print_info "Documentación: docs\ directory"
call :print_info "Soporte: contact@ccvass.com"
echo.
goto :eof

REM Función principal
:main
call :print_header

REM Verificar si ya existe una instalación
if exist "obs_config.json.enc" (
    call :print_warning "Ya existe una configuración encriptada"
    set /p reconfigure="¿Deseas reconfigurar? (s/N): "
    if /i not "!reconfigure!"=="s" (
        call :print_info "Instalación cancelada"
        pause
        exit /b 0
    )
)

REM Ejecutar pasos de instalación
call :check_requirements
call :setup_virtual_environment
call :setup_secure_permissions

REM Seleccionar tipo de usuario
call :select_user_type

REM Configurar credenciales y encriptación
call :setup_obs_credentials
call :setup_encryption
call :create_launcher_scripts
call :show_installation_summary

pause
goto :eof

REM Ejecutar instalación
call :main %*
