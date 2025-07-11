@echo off
REM OBS Utils Runner for Windows
REM Script para ejecutar OBS Utils fácilmente en Windows

REM Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if errorlevel 1 exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar OBS Utils con los argumentos proporcionados
if "%1"=="" (
    REM Modo interactivo si no hay argumentos
    python obs_utils_improved.py
) else (
    REM Pasar todos los argumentos al script
    python obs_utils_improved.py %*
)

REM Mantener la ventana abierta si hay error
if errorlevel 1 pause
