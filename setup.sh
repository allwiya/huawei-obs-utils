#!/bin/bash

# OBS Utils Setup Script
# Configura el entorno y las credenciales para OBS Utils

set -e

echo "=== OBS Utils Setup ==="
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activating virtual environment..."
source venv/bin/activate

# Instalar dependencias
echo "Installing dependencies..."
pip install -r requirements.txt

# Crear archivo de configuración si no existe
if [ ! -f "obs_config.json" ]; then
    if [ -f "obs_config.json.sample" ]; then
        echo "Creating configuration file from sample..."
        cp obs_config.json.sample obs_config.json
        echo "Configuration file created: obs_config.json"
        echo "Please edit this file with your actual credentials."
    else
        echo "Creating sample configuration file..."
        python obs_utils_improved.py --create-config
        cp obs_config.json.sample obs_config.json
    fi
else
    echo "Configuration file already exists: obs_config.json"
fi

# Crear directorio de logs
mkdir -p logs

# Hacer ejecutable el script principal
chmod +x obs_utils_improved.py

echo
echo "=== Setup Complete ==="
echo
echo "Next steps:"
echo "1. Edit obs_config.json with your Huawei Cloud OBS credentials"
echo "2. Run the tool:"
echo "   - Interactive mode: ./obs_utils_improved.py"
echo "   - Command line: ./obs_utils_improved.py --operation list --bucket your-bucket"
echo "3. Or use with virtual environment:"
echo "   source venv/bin/activate && python obs_utils_improved.py"
echo
echo "For help: ./obs_utils_improved.py --help"
echo
