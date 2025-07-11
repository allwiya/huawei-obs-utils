# OBS Utils Setup Script for PowerShell
# Configura el entorno y las credenciales para OBS Utils

Write-Host "=== OBS Utils Setup (PowerShell) ===" -ForegroundColor Green
Write-Host

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is required but not installed." -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activar entorno virtual
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Instalar dependencias
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Crear archivo de configuración si no existe
if (-not (Test-Path "obs_config.json")) {
    if (Test-Path "obs_config.json.sample") {
        Write-Host "Creating configuration file from sample..." -ForegroundColor Yellow
        Copy-Item "obs_config.json.sample" "obs_config.json"
        Write-Host "Configuration file created: obs_config.json" -ForegroundColor Green
        Write-Host "Please edit this file with your actual credentials." -ForegroundColor Yellow
    } else {
        Write-Host "Creating sample configuration file..." -ForegroundColor Yellow
        python obs_utils_improved.py --create-config
        Copy-Item "obs_config.json.sample" "obs_config.json"
    }
} else {
    Write-Host "Configuration file already exists: obs_config.json" -ForegroundColor Green
}

# Crear directorio de logs
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

Write-Host
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit obs_config.json with your Huawei Cloud OBS credentials"
Write-Host "2. Run the tool:"
Write-Host "   - Interactive mode: python obs_utils_improved.py"
Write-Host "   - Command line: python obs_utils_improved.py --operation list --bucket your-bucket"
Write-Host "3. Or activate virtual environment first:"
Write-Host "   venv\Scripts\Activate.ps1"
Write-Host "   python obs_utils_improved.py"
Write-Host
Write-Host "For help: python obs_utils_improved.py --help" -ForegroundColor Yellow
Write-Host
Read-Host "Press Enter to continue"
