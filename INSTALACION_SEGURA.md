# 🔒 Instalación Segura de OBS Utils

Guía completa para la instalación segura de OBS Utils con configuración encriptada y niveles de usuario.

**Desarrollado por:** [CCVASS](mailto:contact@ccvass.com) - Lima, Peru  
**Año:** 2025  
**Licencia:** Apache 2.0

---

## 📋 Índice

- [🚀 Instalación Rápida](#-instalación-rápida)
- [🔧 Instalación Detallada](#-instalación-detallada)
- [👥 Tipos de Usuario](#-tipos-de-usuario)
- [🔐 Configuración de Seguridad](#-configuración-de-seguridad)
- [✅ Validación](#-validación)
- [🛠️ Solución de Problemas](#️-solución-de-problemas)
- [📞 Soporte](#-soporte)

---

## 🚀 Instalación Rápida

### Linux/macOS
```bash
# Clonar el repositorio
git clone <repository-url>
cd obs_utils

# Ejecutar instalación segura
./install_secure_linux.sh
```

### Windows
```cmd
# Clonar el repositorio
git clone <repository-url>
cd obs_utils

# Ejecutar instalación segura
install_secure_windows.bat
```

---

## 🔧 Instalación Detallada

### Requisitos Previos

#### Linux/macOS
- **Python 3.9+**
- **pip** (gestor de paquetes Python)
- **git** (para clonar el repositorio)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# CentOS/RHEL
sudo yum install python3 python3-pip git

# macOS (con Homebrew)
brew install python git
```

#### Windows
- **Python 3.9+** desde [python.org](https://python.org/downloads/)
  - ✅ Marcar "Add Python to PATH" durante la instalación
- **Git** desde [git-scm.com](https://git-scm.com/download/win)

### Proceso de Instalación

#### 1. Preparación
```bash
# Clonar repositorio
git clone <repository-url>
cd obs_utils

# Verificar archivos de instalación
ls install_secure_*
```

#### 2. Ejecutar Instalador

**Linux/macOS:**
```bash
./install_secure_linux.sh
```

**Windows:**
```cmd
install_secure_windows.bat
```

#### 3. Seguir el Asistente Interactivo

El instalador te guiará a través de:

1. **Verificación de requisitos**
2. **Configuración del entorno virtual**
3. **Selección del tipo de usuario**
4. **Configuración de credenciales OBS**
5. **Configuración de encriptación**
6. **Creación de scripts de acceso**

---

## 👥 Tipos de Usuario

### 1. 👤 Usuario Básico (READ_ONLY)
- **Operaciones permitidas:** Listar, buscar, descargar
- **Seguridad:** Sin contraseñas adicionales
- **Ideal para:** Usuarios que solo necesitan consultar y descargar archivos

### 2. 👨‍💼 Usuario Estándar (STANDARD)
- **Operaciones permitidas:** Archivar, restaurar, cambiar clase de almacenamiento
- **Seguridad:** Contraseña de nivel estándar
- **Ideal para:** Usuarios que gestionan archivos regularmente

### 3. 🔧 Usuario Avanzado (DESTRUCTIVE)
- **Operaciones permitidas:** Eliminar objetos, purgar buckets
- **Seguridad:** Contraseñas de nivel estándar + destructivo
- **Ideal para:** Administradores de contenido

### 4. 👑 Administrador (ADMIN)
- **Operaciones permitidas:** Gestión completa de buckets y permisos
- **Seguridad:** Contraseñas de todos los niveles
- **Ideal para:** Administradores del sistema

### 5. 🏢 Configuración Empresarial
- **Operaciones permitidas:** Todas las operaciones con control granular
- **Seguridad:** Múltiples niveles de contraseñas
- **Ideal para:** Entornos empresariales con múltiples usuarios

---

## 🔐 Configuración de Seguridad

### Archivos de Configuración Creados

| Archivo | Descripción | Seguridad |
|---------|-------------|-----------|
| `obs_config.json.enc` | Credenciales OBS encriptadas | AES-256 |
| `obs_config.json.salt` | Salt para encriptación | Requerido |
| `obs_security_levels.json.enc` | Niveles de seguridad | AES-256 |
| `obs_security_levels.json.salt` | Salt para niveles | Requerido |

### Contraseñas de Seguridad

#### Contraseña Maestra
- **Propósito:** Encripta todas las configuraciones
- **Importancia:** ⚠️ **CRÍTICA** - No se puede recuperar si se pierde
- **Recomendación:** Usar gestor de contraseñas

#### Contraseñas por Nivel
- **Estándar:** Para operaciones de archivo y restauración
- **Destructiva:** Para operaciones de eliminación
- **Administrador:** Para gestión de buckets y permisos

### Mejores Prácticas de Seguridad

1. **Contraseñas Fuertes**
   - Mínimo 12 caracteres
   - Combinación de letras, números y símbolos
   - Diferentes para cada nivel

2. **Almacenamiento Seguro**
   - Usar gestor de contraseñas
   - No almacenar en texto plano
   - Hacer respaldos seguros

3. **Permisos de Archivos**
   - Los archivos `.enc` y `.salt` son críticos
   - Mantener permisos restrictivos (600 en Linux)
   - No compartir estos archivos

---

## ✅ Validación

### Validación Automática
```bash
# Ejecutar validación completa
python validate_secure_installation.py
```

### Validación Manual

#### 1. Verificar Archivos
```bash
# Linux/macOS
ls -la obs_config.json.enc obs_config.json.salt
ls -la obs_security_levels.json.enc obs_security_levels.json.salt

# Windows
dir obs_config.json.enc obs_config.json.salt
dir obs_security_levels.json.enc obs_security_levels.json.salt
```

#### 2. Probar Scripts de Acceso
```bash
# Linux/macOS
./obs --help
./activate_obs.sh

# Windows
obs.bat --help
activate_obs.bat
```

#### 3. Probar Funcionalidad Básica
```bash
# Listar buckets (requiere credenciales válidas)
./obs --operation list --bucket test-bucket
```

---

## 🛠️ Solución de Problemas

### Errores Comunes

#### Error: "Python no encontrado"
**Solución:**
```bash
# Linux
sudo apt install python3

# Windows
# Reinstalar Python desde python.org marcando "Add to PATH"
```

#### Error: "Módulo cryptography no encontrado"
**Solución:**
```bash
# Activar entorno virtual y reinstalar
source venv/bin/activate  # Linux
# o
venv\Scripts\activate.bat  # Windows

pip install --upgrade cryptography
```

#### Error: "Archivo de configuración no encontrado"
**Solución:**
```bash
# Verificar archivos encriptados
ls -la *.enc *.salt

# Si faltan, ejecutar nuevamente el instalador
./install_secure_linux.sh  # Linux
# o
install_secure_windows.bat  # Windows
```

#### Error: "Contraseña incorrecta"
**Solución:**
- Verificar que estás usando la contraseña maestra correcta
- Si perdiste la contraseña, necesitarás reconfigurar:
```bash
# Respaldar datos importantes primero
# Luego ejecutar instalador nuevamente
```

### Logs de Depuración

Los logs se almacenan en:
- **Linux/macOS:** `logs/obs_utils.log`
- **Windows:** `logs\obs_utils.log`

### Reinstalación

Si necesitas reinstalar completamente:

```bash
# 1. Respaldar configuración actual (opcional)
cp obs_config.json.enc obs_config.json.enc.backup
cp obs_security_levels.json.enc obs_security_levels.json.enc.backup

# 2. Limpiar instalación
rm -rf venv/
rm obs_config.json.enc obs_config.json.salt
rm obs_security_levels.json.enc obs_security_levels.json.salt

# 3. Ejecutar instalador nuevamente
./install_secure_linux.sh  # Linux
# o
install_secure_windows.bat  # Windows
```

---

## 📞 Soporte

### Contacto CCVASS
- **Email:** [contact@ccvass.com](mailto:contact@ccvass.com)
- **Empresa:** CCVASS - Lima, Peru
- **Año:** 2025

### Recursos de Ayuda
- **Documentación:** Directorio `docs/`
- **Ejemplos:** Directorio `examples/`
- **Issues:** Repositorio del proyecto
- **Logs:** Directorio `logs/`

### Información para Soporte

Al contactar soporte, incluye:

1. **Sistema Operativo:** (Linux/Windows/macOS + versión)
2. **Versión de Python:** `python --version`
3. **Tipo de Usuario:** Configurado durante instalación
4. **Error Específico:** Mensaje completo de error
5. **Logs:** Contenido de `logs/obs_utils.log`

---

## 📄 Licencia

Este proyecto está licenciado bajo **Apache License 2.0**.

---

**Desarrollado con ❤️ por CCVASS - Lima, Peru 🇵🇪**

**¿Necesitas ayuda?** Contacta [contact@ccvass.com](mailto:contact@ccvass.com)
