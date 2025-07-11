# 🚀 GitHub Actions CI/CD Pipeline

Este directorio contiene los workflows de GitHub Actions para OBS Utils, proporcionando integración continua, testing automatizado y deployment.

---

**Desarrollado por:** [CCVASS](mailto:contact@ccvass.com) - Lima, Perú  
**Año:** 2025  
**Licencia:** Apache 2.0  
**Contacto:** contact@ccvass.com

---

## 📋 Workflows Disponibles

### 1. **ci-cd.yml** - Pipeline Principal
**Triggers:**
- Push a `main` y `develop`
- Pull requests a `main`
- Releases publicados

**Jobs:**
- 🔍 **Lint**: Code quality y linting (Black, isort, Flake8)
- 🧪 **Test**: Unit tests en múltiples plataformas y versiones Python
- 🔒 **Security**: Testing de módulos de seguridad
- 📚 **Documentation**: Verificación de documentación
- 📦 **Build**: Construcción de paquetes
- 🔗 **Integration**: Tests de integración
- 🚀 **Release**: Creación automática de releases
- 📢 **Notify**: Notificaciones de estado

### 2. **security.yml** - Testing de Seguridad
**Triggers:**
- Push a `main` y `develop`
- Pull requests a `main`
- Schedule diario (2 AM UTC)

**Jobs:**
- 🛡️ **Security Scan**: Bandit, Safety, Semgrep
- 📦 **Dependency Check**: Snyk vulnerability scanning
- 🔍 **Secrets Scan**: TruffleHog para detectar secretos
- 🧪 **Security Test**: Testing de funciones de seguridad
- ✅ **Compliance**: Verificación de cumplimiento de seguridad
- 📊 **Report**: Reporte consolidado de seguridad

### 3. **cross-platform.yml** - Testing Multiplataforma
**Triggers:**
- Push a `main` y `develop`
- Pull requests a `main`

**Jobs:**
- 🪟 **Windows Testing**: Testing específico para Windows
- 🍎 **macOS Testing**: Testing específico para macOS
- 🐧 **Linux Testing**: Testing específico para Linux
- 🔄 **Compatibility**: Tests de compatibilidad
- 🔗 **Integration**: Tests de integración multiplataforma
- ⚡ **Performance**: Tests de rendimiento

## 🎯 Matriz de Testing

### **Sistemas Operativos**
- Ubuntu Latest
- Windows Latest
- macOS Latest

### **Versiones de Python**
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

### **Combinaciones Totales**
- **12 combinaciones** de OS + Python version
- **Tests paralelos** para máxima eficiencia

## 🔒 Herramientas de Seguridad

### **Análisis Estático**
- **Bandit**: Security linting para Python
- **Safety**: Vulnerabilidades conocidas en dependencias
- **Semgrep**: Análisis de código estático avanzado
- **Snyk**: Scanning de vulnerabilidades

### **Detección de Secretos**
- **TruffleHog**: Detección de credenciales hardcodeadas
- **Custom checks**: Verificaciones personalizadas

### **Testing de Seguridad**
- **Encryption testing**: Verificación de AES-256
- **Password hashing**: Testing de SHA-256
- **Permission testing**: Verificación de permisos de archivos
- **Security levels**: Testing del sistema multinivel

## 📊 Reportes y Artefactos

### **Artefactos Generados**
- `security-reports/`: Reportes de seguridad (Bandit, Safety, Semgrep)
- `dist-packages/`: Paquetes de distribución
- `coverage.xml`: Reporte de cobertura de código
- `htmlcov/`: Reporte HTML de cobertura

### **Integración con Servicios**
- **Codecov**: Cobertura de código
- **Snyk**: Monitoreo de vulnerabilidades
- **GitHub Releases**: Releases automáticos

## 🚀 Proceso de Release

### **Trigger**
```bash
# Crear release en GitHub
git tag v2.0.0
git push origin v2.0.0
# O crear release desde GitHub UI
```

### **Proceso Automático**
1. **Build**: Construcción de paquetes
2. **Test**: Ejecución completa de tests
3. **Security**: Verificación de seguridad
4. **Package**: Creación de distribución
5. **Release**: Publicación automática con:
   - Archivos de distribución
   - Documentación principal
   - Release notes automáticas

## 🔧 Configuración Local

### **Instalar Herramientas de Desarrollo**
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black isort flake8 bandit safety
```

### **Ejecutar Tests Localmente**
```bash
# Tests básicos
pytest

# Tests con cobertura
pytest --cov=. --cov-report=html

# Linting
black --check .
isort --check-only .
flake8 .

# Seguridad
bandit -r .
safety check
```

### **Pre-commit Hooks (Recomendado)**
```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.4
    hooks:
      - id: bandit
        args: ['-r', '.']
EOF

# Instalar hooks
pre-commit install
```

## 📈 Métricas y Monitoreo

### **Métricas Tracked**
- **Code Coverage**: Objetivo >80%
- **Security Score**: Sin vulnerabilidades críticas
- **Performance**: Import time <2s, Memory <50MB
- **Cross-platform**: 100% compatibilidad

### **Badges para README**
```markdown
![CI/CD](https://github.com/your-org/obs-utils/workflows/OBS%20Utils%20CI/CD%20Pipeline/badge.svg)
![Security](https://github.com/your-org/obs-utils/workflows/Security%20Testing/badge.svg)
![Cross-Platform](https://github.com/your-org/obs-utils/workflows/Cross-Platform%20Testing/badge.svg)
[![codecov](https://codecov.io/gh/your-org/obs-utils/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/obs-utils)
```

## 🛠️ Troubleshooting

### **Fallos Comunes**

#### **Import Errors**
```bash
# Verificar dependencias
pip install -r requirements.txt

# Verificar Python version
python --version  # Debe ser >=3.8
```

#### **Permission Errors (Linux/macOS)**
```bash
# Dar permisos a scripts
chmod +x setup.sh setup_secure.sh
```

#### **Windows Path Issues**
```cmd
REM Verificar que Python esté en PATH
python --version

REM Usar rutas absolutas si es necesario
```

### **Debug de Tests**
```bash
# Ejecutar test específico
pytest tests/test_basic.py::TestConfig::test_config_import -v

# Debug con pdb
pytest --pdb tests/test_basic.py

# Solo tests que fallan
pytest --lf
```

## 📞 Soporte

### **Para Desarrolladores**
- Revisar logs de GitHub Actions
- Verificar configuración local
- Ejecutar tests localmente antes de push

### **Para Administradores**
- Configurar secrets en GitHub (SNYK_TOKEN, etc.)
- Revisar permisos de workflows
- Monitorear métricas de seguridad

---

**💡 Tip**: Siempre ejecuta `pytest` y `flake8` localmente antes de hacer push para evitar fallos en CI/CD.

---

**Desarrollado con ❤️ por CCVASS - Lima, Perú 🇵🇪**

**Soporte técnico:** [contact@ccvass.com](mailto:contact@ccvass.com)  
**Licencia:** Apache 2.0 | **Año:** 2025
