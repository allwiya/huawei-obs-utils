@echo off
REM Enhanced setup script for OBS Utils with security features - Windows
REM Para superadministradores

echo.
echo 🔒 OBS Utils - Instalacion Segura para Windows
echo ===============================================
echo.

REM Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Ejecutandose como administrador
) else (
    echo ⚠️  Recomendado: Ejecutar como administrador para instalacion completa
    echo    Clic derecho en Command Prompt ^> "Ejecutar como administrador"
    echo.
    pause
)

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorLevel% == 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python %PYTHON_VERSION% encontrado
) else (
    echo ❌ Python no encontrado
    echo    Descargar desde: https://python.org
    echo    ⚠️  IMPORTANTE: Marcar "Add Python to PATH" durante instalacion
    pause
    exit /b 1
)

REM Crear entorno virtual
echo.
echo 🔧 Creando entorno virtual...
if exist venv (
    echo ⚠️  Entorno virtual ya existe. Eliminando...
    rmdir /s /q venv
)

python -m venv venv
if %errorLevel% == 0 (
    echo ✅ Entorno virtual creado
) else (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

REM Activar entorno virtual
echo.
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo.
echo 📦 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo 📦 Instalando dependencias...
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorLevel% == 0 (
        echo ✅ Dependencias instaladas correctamente
    ) else (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
) else (
    echo ❌ Archivo requirements.txt no encontrado
    pause
    exit /b 1
)

REM Crear directorio de logs
echo.
echo 📁 Creando directorio de logs...
if not exist logs mkdir logs
echo ✅ Directorio de logs creado

REM Probar instalacion
echo.
echo 🧪 Probando instalacion...
python -c "from obs_manager import OBSManager; from config import Config; print('✅ Modulos principales OK')" 2>nul
if %errorLevel% == 0 (
    echo ✅ Modulos principales funcionando
) else (
    echo ❌ Error en modulos principales
    pause
    exit /b 1
)

python -c "from security import ConfigSecurity; print('✅ Modulo de seguridad OK')" 2>nul
if %errorLevel% == 0 (
    echo ✅ Modulo de seguridad funcionando
) else (
    echo ⚠️  Modulo de seguridad no disponible
    echo    Instalando cryptography...
    pip install cryptography
)

python -c "from security_levels import MultiLevelSecurity; print('✅ Niveles de seguridad OK')" 2>nul
if %errorLevel% == 0 (
    echo ✅ Sistema de niveles de seguridad funcionando
) else (
    echo ⚠️  Sistema de niveles no disponible
)

REM Crear script de ejecucion
echo.
echo 📝 Creando scripts de ejecucion...

REM Script run.bat
echo @echo off > run.bat
echo REM Script de ejecucion rapida para OBS Utils >> run.bat
echo. >> run.bat
echo REM Obtener directorio del script >> run.bat
echo cd /d "%%~dp0" >> run.bat
echo. >> run.bat
echo REM Activar entorno virtual >> run.bat
echo if exist venv\Scripts\activate.bat ( >> run.bat
echo     call venv\Scripts\activate.bat >> run.bat
echo ^) else ( >> run.bat
echo     echo ❌ Error: Entorno virtual no encontrado. Ejecuta setup_secure.bat >> run.bat
echo     pause >> run.bat
echo     exit /b 1 >> run.bat
echo ^) >> run.bat
echo. >> run.bat
echo REM Ejecutar OBS Utils con argumentos >> run.bat
echo python obs_utils_improved.py %%* >> run.bat

echo ✅ Script run.bat creado

REM Script para usuarios
echo @echo off > run_usuario.bat
echo REM Script para usuarios operadores >> run_usuario.bat
echo. >> run_usuario.bat
echo cd /d "%%~dp0" >> run_usuario.bat
echo call venv\Scripts\activate.bat >> run_usuario.bat
echo python obs_utils_improved.py --enable-security-levels %%* >> run_usuario.bat

echo ✅ Script run_usuario.bat creado

REM Configuracion de seguridad
echo.
echo 🔐 Configuracion de Seguridad
echo ==============================
echo.
echo Elige el metodo de configuracion:
echo 1. Configuracion cifrada (Mas segura - recomendada)
echo 2. Variables de entorno (Buena para servidores)
echo 3. Archivo con permisos seguros (Basica)
echo 4. Configurar niveles de seguridad (Avanzada)
echo 5. Saltar configuracion (configurar manualmente despues)
echo.

set /p choice="Ingresa tu opcion (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🔐 Configurando archivo cifrado...
    python obs_utils_improved.py --setup-secure-config
) else if "%choice%"=="2" (
    echo.
    echo 🌍 Configuracion de variables de entorno...
    echo.
    echo Agrega estas lineas a las variables de entorno del sistema:
    echo.
    echo Variable: OBS_ACCESS_KEY_ID
    echo Valor: tu_access_key_aqui
    echo.
    echo Variable: OBS_SECRET_ACCESS_KEY  
    echo Valor: tu_secret_key_aqui
    echo.
    echo Variable: OBS_SERVER
    echo Valor: https://obs.sa-peru-1.myhuaweicloud.com/
    echo.
    echo Para configurar:
    echo 1. Win + R ^> sysdm.cpl ^> Variables de entorno
    echo 2. O usar: setx VARIABLE "valor" /M
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo 📁 Creando archivo de configuracion basico...
    python obs_utils_improved.py --create-config
    echo.
    echo ⚠️  Edita obs_config.json con tus credenciales reales
    echo    Usa Notepad o cualquier editor de texto
    echo.
    pause
) else if "%choice%"=="4" (
    echo.
    echo 🔐 Configurando niveles de seguridad avanzados...
    python obs_utils_improved.py --setup-security-levels
) else if "%choice%"=="5" (
    echo.
    echo ⏭️  Configuracion omitida
    echo    Configura manualmente despues con:
    echo    python obs_utils_improved.py --setup-secure-config
) else (
    echo ❌ Opcion invalida. Configuracion omitida.
)

REM Crear accesos directos en escritorio (opcional)
echo.
set /p desktop="¿Crear accesos directos en el escritorio? (s/N): "
if /i "%desktop%"=="s" (
    echo 🖥️  Creando accesos directos...
    
    REM Crear acceso directo para administradores
    echo Set oWS = WScript.CreateObject("WScript.Shell"^) > create_shortcut.vbs
    echo sLinkFile = oWS.ExpandEnvironmentStrings("%%USERPROFILE%%\Desktop\OBS Utils Admin.lnk"^) >> create_shortcut.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile^) >> create_shortcut.vbs
    echo oLink.TargetPath = "%CD%\run.bat" >> create_shortcut.vbs
    echo oLink.WorkingDirectory = "%CD%" >> create_shortcut.vbs
    echo oLink.Description = "OBS Utils - Administrador" >> create_shortcut.vbs
    echo oLink.Save >> create_shortcut.vbs
    
    REM Crear acceso directo para usuarios
    echo Set oWS = WScript.CreateObject("WScript.Shell"^) > create_shortcut_user.vbs
    echo sLinkFile = oWS.ExpandEnvironmentStrings("%%USERPROFILE%%\Desktop\OBS Utils Usuario.lnk"^) >> create_shortcut_user.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile^) >> create_shortcut_user.vbs
    echo oLink.TargetPath = "%CD%\run_usuario.bat" >> create_shortcut_user.vbs
    echo oLink.WorkingDirectory = "%CD%" >> create_shortcut_user.vbs
    echo oLink.Description = "OBS Utils - Usuario Operador" >> create_shortcut_user.vbs
    echo oLink.Save >> create_shortcut_user.vbs
    
    cscript create_shortcut.vbs >nul 2>&1
    cscript create_shortcut_user.vbs >nul 2>&1
    
    del create_shortcut.vbs >nul 2>&1
    del create_shortcut_user.vbs >nul 2>&1
    
    echo ✅ Accesos directos creados en el escritorio
)

REM Resumen final
echo.
echo 🎉 ¡Instalacion completada exitosamente!
echo =========================================
echo.
echo 📋 Proximos pasos:
echo.
echo 1. Probar la instalacion:
echo    run.bat --operation list --bucket test-bucket
echo.
echo 2. Usar la aplicacion:
echo    run.bat                    # Modo interactivo
echo    run.bat --help            # Ver todas las opciones
echo.
echo 3. Para usuarios operadores:
echo    run_usuario.bat           # Modo con seguridad multinivel
echo.
echo 4. Funciones de seguridad:
echo    run.bat --setup-security-levels     # Configurar niveles
echo    run.bat --list-security-levels      # Ver niveles configurados
echo    run.bat --encrypt-config            # Cifrar configuracion
echo.
echo 5. Documentacion:
echo    type GUIA_SUPERADMIN_WINDOWS.md     # Guia para administradores
echo    type GUIA_OPERADOR_WINDOWS.md       # Guia para usuarios
echo    type SECURITY.md                    # Guia completa de seguridad
echo.
echo 📁 Archivos importantes:
echo    - run.bat                 # Script principal
echo    - run_usuario.bat         # Script para operadores
echo    - obs_config.json.enc     # Configuracion cifrada (si aplica)
echo    - logs\                   # Directorio de logs
echo.
echo ⚠️  IMPORTANTE:
echo    - Mantén seguras las contraseñas maestras
echo    - Haz backups regulares de la configuracion
echo    - Revisa los logs periodicamente
echo.
echo ✅ ¡Instalacion completa! 🚀
echo.
pause
