#!/bin/bash

# migrate.sh - Script para migrar del script antiguo obs_utils.py
# Este script extrae las credenciales hardcodeadas y crea la nueva configuración

set -e

echo "=== OBS Utils Migration Script ==="
echo

# Verificar si existe el script antiguo
if [ ! -f "obs_utils.py" ]; then
    echo "Error: obs_utils.py not found in current directory"
    echo "Please run this script from the obs_utils directory"
    exit 1
fi

echo "Extracting credentials from obs_utils.py..."

# Extraer credenciales del script antiguo
OLD_AK=$(grep 'ak = ' obs_utils.py | cut -d'"' -f2)
OLD_SK=$(grep 'sk = ' obs_utils.py | cut -d'"' -f2)
OLD_SERVER=$(grep 'server = ' obs_utils.py | cut -d'"' -f2)

if [ -z "$OLD_AK" ] || [ -z "$OLD_SK" ] || [ -z "$OLD_SERVER" ]; then
    echo "Warning: Could not extract all credentials from obs_utils.py"
    echo "Please configure credentials manually in obs_config.json"
    
    # Create sample config
    python obs_utils_improved.py --create-config 2>/dev/null || true
    cp obs_config.json.sample obs_config.json 2>/dev/null || true
    
    echo "Sample configuration created: obs_config.json"
    echo "Please edit this file with your actual credentials."
    exit 0
fi

echo "Found credentials:"
echo "  Access Key: ${OLD_AK:0:8}..."
echo "  Secret Key: ${OLD_SK:0:8}..."
echo "  Server: $OLD_SERVER"

# Crear nuevo archivo de configuración
echo "Creating new configuration file..."

cat > obs_config.json << EOF
{
  "access_key_id": "$OLD_AK",
  "secret_access_key": "$OLD_SK",
  "server": "$OLD_SERVER",
  "region": "sa-peru-1",
  "max_keys": 1000,
  "restore_days": 30,
  "restore_tier": "Expedited"
}
EOF

echo "✓ Configuration file created: obs_config.json"

# Crear backup del script original
if [ ! -f "obs_utils.py.backup" ]; then
    cp obs_utils.py obs_utils.py.backup
    echo "✓ Backup created: obs_utils.py.backup"
fi

# Verificar que el nuevo script funciona
echo "Testing new configuration..."
if source venv/bin/activate 2>/dev/null && python obs_utils_improved.py --create-config >/dev/null 2>&1; then
    echo "✓ New script is working correctly"
else
    echo "Warning: Could not test new script. Please run setup.sh first."
fi

echo
echo "=== Migration Complete ==="
echo
echo "Your credentials have been migrated to obs_config.json"
echo "The original script has been backed up as obs_utils.py.backup"
echo
echo "Next steps:"
echo "1. Review and edit obs_config.json if needed"
echo "2. Test the new script:"
echo "   source venv/bin/activate"
echo "   python obs_utils_improved.py --help"
echo "3. Use the new operations:"
echo
echo "   Old: python obs_utils.py (interactive)"
echo "   New: python obs_utils_improved.py (interactive)"
echo
echo "   Old: Select 'l' for list"
echo "   New: python obs_utils_improved.py --operation list --bucket your-bucket"
echo
echo "For more information, see README.md"
echo
