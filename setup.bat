@echo off
REM OBS Utils Setup Script for Windows
REM Configura el entorno y las credenciales para OBS Utils

echo === OBS Utils Setup (Windows) ===
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is required but not installed.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activar entorno virtual
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Installing dependencies...
pip install -r requirements.txt

REM Crear archivo de configuración si no existe
if not exist "obs_config.json" (
    if exist "obs_config.json.sample" (
        echo Creating configuration file from sample...
        copy obs_config.json.sample obs_config.json
        echo Configuration file created: obs_config.json
        echo Please edit this file with your actual credentials.
    ) else (
        echo Creating sample configuration file...
        python obs_utils_improved.py --create-config
        copy obs_config.json.sample obs_config.json
    )
) else (
    echo Configuration file already exists: obs_config.json
)

REM Crear directorio de logs
if not exist "logs" mkdir logs

echo.
echo === Setup Complete ===
echo.
echo Next steps:
echo 1. Edit obs_config.json with your Huawei Cloud OBS credentials
echo 2. Run the tool:
echo    - Interactive mode: python obs_utils_improved.py
echo    - Command line: python obs_utils_improved.py --operation list --bucket your-bucket
echo 3. Or activate virtual environment first:
echo    venv\Scripts\activate.bat
echo    python obs_utils_improved.py
echo.
echo For help: python obs_utils_improved.py --help
echo.
pause
