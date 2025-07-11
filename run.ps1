# OBS Utils Runner for PowerShell
# Script para ejecutar OBS Utils fácilmente en PowerShell

# Verificar si el entorno virtual existe
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Running setup..." -ForegroundColor Yellow
    & ".\setup.ps1"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

# Activar entorno virtual
& "venv\Scripts\Activate.ps1"

# Ejecutar OBS Utils con los argumentos proporcionados
if ($args.Count -eq 0) {
    # Modo interactivo si no hay argumentos
    python obs_utils_improved.py
} else {
    # Pasar todos los argumentos al script
    python obs_utils_improved.py @args
}

# Mantener la ventana abierta si hay error
if ($LASTEXITCODE -ne 0) {
    Read-Host "Press Enter to continue"
}
