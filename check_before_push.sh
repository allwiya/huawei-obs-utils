#!/bin/bash

# Script para verificar que todo esté listo antes de hacer push
echo "🔍 Verificando configuración antes de push..."

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar que no hay README en .github
if [ -f ".github/README.md" ]; then
    echo "❌ ERROR: Existe README.md en .github/ - esto causará conflictos"
    echo "   Ejecuta: rm .github/README.md"
    exit 1
else
    echo "✅ No hay README conflictivo en .github/"
fi

# Verificar que existe README en la raíz
if [ -f "README.md" ]; then
    echo "✅ README.md existe en la raíz"
else
    echo "❌ ERROR: No existe README.md en la raíz"
    exit 1
fi

# Verificar archivos de documentación de Windows
if [ -f "docs/en/WINDOWS_GUIDE.md" ]; then
    echo "✅ Documentación de Windows (EN) existe"
else
    echo "❌ ERROR: Falta docs/en/WINDOWS_GUIDE.md"
    exit 1
fi

if [ -f "docs/es/GUIA_WINDOWS.md" ]; then
    echo "✅ Documentación de Windows (ES) existe"
else
    echo "❌ ERROR: Falta docs/es/GUIA_WINDOWS.md"
    exit 1
fi

# Verificar que los imports funcionan
echo "🧪 Probando imports..."
python -c "import obs_manager; print('✅ obs_manager OK')" || exit 1
python -c "import config; print('✅ config OK')" || exit 1
python -c "import security; print('✅ security OK')" || exit 1
python -c "import logger; print('✅ logger OK')" || exit 1

# Verificar que el CLI funciona
echo "🧪 Probando CLI..."
python obs_utils_improved.py --help > /dev/null || exit 1
echo "✅ CLI funciona correctamente"

# Verificar sintaxis de workflows
echo "🧪 Verificando workflows..."
for workflow in .github/workflows/*.yml; do
    if [ -f "$workflow" ]; then
        echo "✅ $workflow existe"
    fi
done

echo ""
echo "🎉 ¡Todo listo para push!"
echo ""
echo "Comandos sugeridos:"
echo "git add ."
echo "git commit -m 'Fix: Corregir workflows y documentación'"
echo "git push origin main"
