# 🔒 Guía de Seguridad - OBS Utils

Esta guía explica cómo implementar y usar las funciones de seguridad en OBS Utils para proteger tus credenciales de Huawei Cloud.

---

**Desarrollado por:** [CCVASS](mailto:contact@ccvass.com) - Lima, Perú  
**Año:** 2025  
**Licencia:** Apache 2.0  
**Contacto:** contact@ccvass.com

---

## 📋 Tabla de Contenidos

- [Opciones de Seguridad](#-opciones-de-seguridad)
- [Configuración Cifrada](#-configuración-cifrada)
- [Variables de Entorno](#-variables-de-entorno)
- [Permisos de Archivos](#-permisos-de-archivos)
- [Mejores Prácticas](#-mejores-prácticas)
- [Solución de Problemas](#-solución-de-problemas)

## 🛡️ Opciones de Seguridad

OBS Utils ofrece **tres niveles de seguridad** para proteger tus credenciales:

### 1. **Configuración Cifrada** (Más Segura) 🔐
- Archivo de configuración cifrado con AES-256
- Protegido por contraseña
- Imposible de leer sin la contraseña correcta

### 2. **Variables de Entorno** (Recomendada) 🌍
- Credenciales almacenadas en variables del sistema
- No persisten en archivos
- Fácil de gestionar en servidores

### 3. **Archivo con Permisos Seguros** (Básica) 📁
- Archivo JSON con permisos restrictivos (600)
- Solo el propietario puede leer/escribir
- Protección a nivel del sistema operativo

## 🔐 Configuración Cifrada

### Configuración Inicial

**Opción 1: Setup Interactivo (Recomendado)**
```bash
# Ejecutar configuración segura interactiva
python obs_utils_improved.py --setup-secure-config

# O usar el script dedicado
python setup_secure_config.py
```

**Opción 2: Cifrar Configuración Existente**
```bash
# Si ya tienes obs_config.json
python obs_utils_improved.py --encrypt-config
```

**Opción 3: Programáticamente**
```python
from security import ConfigSecurity

# Crear configuración cifrada
config_data = {
    "access_key_id": "tu_access_key",
    "secret_access_key": "tu_secret_key",
    "server": "https://obs.sa-peru-1.myhuaweicloud.com/",
    "region": "sa-peru-1"
}

security = ConfigSecurity()
security.create_encrypted_config(config_data)
```

### Archivos Generados

Cuando usas configuración cifrada, se crean dos archivos:
```
obs_config.json.enc  # Configuración cifrada
obs_config.json.salt # Salt para el cifrado
```

**⚠️ IMPORTANTE**: 
- Ambos archivos son necesarios para descifrar
- La contraseña NO se almacena en ningún lugar
- Si pierdes la contraseña, no podrás recuperar la configuración

### Uso de Configuración Cifrada

```bash
# La aplicación detecta automáticamente la configuración cifrada
python obs_utils_improved.py --operation list --bucket mi-bucket

# Te pedirá la contraseña:
# Enter password to decrypt configuration: [contraseña oculta]
```

### Cambiar Contraseña

```python
from security import ConfigSecurity

security = ConfigSecurity()
security.change_password()
# Te pedirá la contraseña actual y la nueva
```

## 🌍 Variables de Entorno

### Configuración

**Linux/macOS:**
```bash
# Agregar a ~/.bashrc, ~/.zshrc, etc.
export OBS_ACCESS_KEY_ID="tu_access_key"
export OBS_SECRET_ACCESS_KEY="tu_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"

# Recargar configuración
source ~/.bashrc
```

**Windows (Command Prompt):**
```cmd
# Configuración temporal (solo para la sesión actual)
set OBS_ACCESS_KEY_ID=tu_access_key
set OBS_SECRET_ACCESS_KEY=tu_secret_key

# Configuración permanente
setx OBS_ACCESS_KEY_ID "tu_access_key"
setx OBS_SECRET_ACCESS_KEY "tu_secret_key"
```

**Windows (PowerShell):**
```powershell
# Configuración temporal
$env:OBS_ACCESS_KEY_ID="tu_access_key"
$env:OBS_SECRET_ACCESS_KEY="tu_secret_key"

# Configuración permanente (requiere reiniciar PowerShell)
[Environment]::SetEnvironmentVariable("OBS_ACCESS_KEY_ID", "tu_access_key", "User")
[Environment]::SetEnvironmentVariable("OBS_SECRET_ACCESS_KEY", "tu_secret_key", "User")
```

### Verificar Variables

```bash
# Linux/macOS
echo $OBS_ACCESS_KEY_ID
env | grep OBS_

# Windows (Command Prompt)
echo %OBS_ACCESS_KEY_ID%
set | findstr OBS_

# Windows (PowerShell)
$env:OBS_ACCESS_KEY_ID
Get-ChildItem Env: | Where-Object Name -like "OBS_*"
```

## 📁 Permisos de Archivos

### Configurar Permisos Seguros

**Automático:**
```bash
python obs_utils_improved.py --secure-permissions
```

**Manual (Linux/macOS):**
```bash
# Solo el propietario puede leer/escribir
chmod 600 obs_config.json

# Verificar permisos
ls -la obs_config.json
# Debería mostrar: -rw------- 1 usuario grupo
```

**Manual (Windows):**
```cmd
# Usar interfaz gráfica:
# 1. Clic derecho en obs_config.json
# 2. Propiedades → Seguridad → Avanzado
# 3. Deshabilitar herencia
# 4. Quitar todos los permisos excepto el propietario
```

### Verificación de Seguridad

La aplicación automáticamente verifica y advierte sobre permisos inseguros:

```
⚠️  Configuration file obs_config.json has insecure permissions!
   Recommended: chmod 600 obs_config.json
   Or consider using encrypted configuration
Fix file permissions now? (y/N):
```

## 🎯 Mejores Prácticas

### 1. **Orden de Prioridad de Configuración**

La aplicación busca configuración en este orden:
1. **Configuración cifrada** (obs_config.json.enc)
2. **Variables de entorno** (OBS_ACCESS_KEY_ID, etc.)
3. **Archivo de configuración** (obs_config.json)

### 2. **Recomendaciones por Entorno**

| Entorno | Método Recomendado | Razón |
|---------|-------------------|-------|
| **Desarrollo Local** | Configuración Cifrada | Máxima seguridad, fácil de usar |
| **Servidores/CI/CD** | Variables de Entorno | Estándar de la industria |
| **Contenedores** | Variables de Entorno | Fácil gestión con Docker/K8s |
| **Equipos Compartidos** | Configuración Cifrada | Cada usuario su propia contraseña |

### 3. **Gestión de Contraseñas**

- **Usa contraseñas fuertes**: Mínimo 12 caracteres, mezcla de letras, números y símbolos
- **No reutilices contraseñas**: Usa una contraseña única para OBS Utils
- **Considera un gestor de contraseñas**: Para almacenar la contraseña de forma segura
- **Documenta la ubicación**: Pero no la contraseña misma

### 4. **Respaldo Seguro**

```bash
# Respaldar configuración cifrada
cp obs_config.json.enc obs_config.json.enc.backup
cp obs_config.json.salt obs_config.json.salt.backup

# Almacenar en ubicación segura (USB cifrado, cloud personal, etc.)
```

### 5. **Rotación de Credenciales**

```bash
# 1. Generar nuevas credenciales en Huawei Cloud Console
# 2. Actualizar configuración
python obs_utils_improved.py --setup-secure-config

# 3. Probar nueva configuración
python obs_utils_improved.py --operation list --bucket test-bucket

# 4. Revocar credenciales antiguas en Huawei Cloud
```

## 🔧 Configuración Avanzada

### Múltiples Configuraciones

```bash
# Configuración para producción
python obs_utils_improved.py --config prod_config.json --operation list --bucket prod-bucket

# Configuración para desarrollo
python obs_utils_improved.py --config dev_config.json --operation list --bucket dev-bucket
```

### Configuración Programática

```python
from config import Config
from obs_manager import OBSManager

# Usar configuración específica
config = Config("mi_config_especial.json", use_encryption=True)
obs_manager = OBSManager(config_file="mi_config_especial.json")

# Verificar si está cifrada
if config.is_encrypted():
    print("Configuración cifrada detectada")
```

### Variables de Entorno Personalizadas

```python
import os

# Definir variables personalizadas
os.environ['OBS_ACCESS_KEY_ID'] = 'mi_access_key'
os.environ['OBS_SECRET_ACCESS_KEY'] = 'mi_secret_key'

# Usar en la aplicación
from config import Config
config = Config()  # Automáticamente usa las variables de entorno
```

## 🚨 Solución de Problemas

### Error: "Security module not available"

```bash
# Instalar dependencia de cifrado
pip install cryptography

# O reinstalar todas las dependencias
pip install -r requirements.txt
```

### Error: "Failed to decrypt configuration"

**Posibles causas:**
1. **Contraseña incorrecta**: Verifica que estés usando la contraseña correcta
2. **Archivos corruptos**: Verifica que ambos archivos (.enc y .salt) existan
3. **Archivos movidos**: Los archivos deben estar en el mismo directorio

**Solución:**
```bash
# Verificar archivos
ls -la obs_config.json.*

# Si tienes respaldo, restaurar
cp obs_config.json.enc.backup obs_config.json.enc
cp obs_config.json.salt.backup obs_config.json.salt

# Si no tienes respaldo, crear nueva configuración
python obs_utils_improved.py --setup-secure-config
```

### Error: "Permission denied"

```bash
# Linux/macOS: Verificar permisos
ls -la obs_config.json*

# Corregir permisos
chmod 600 obs_config.json*

# Windows: Usar interfaz gráfica para ajustar permisos
```

### Configuración no detectada

```bash
# Verificar orden de prioridad
echo "Variables de entorno:"
env | grep OBS_

echo "Archivos de configuración:"
ls -la obs_config.json*

# Forzar uso de archivo específico
python obs_utils_improved.py --config mi_config.json --operation list --bucket test
```

### Migrar de configuración no cifrada a cifrada

```bash
# 1. Respaldar configuración actual
cp obs_config.json obs_config.json.backup

# 2. Cifrar configuración existente
python obs_utils_improved.py --encrypt-config

# 3. Probar configuración cifrada
python obs_utils_improved.py --operation list --bucket test-bucket

# 4. Si funciona, eliminar archivo no cifrado
rm obs_config.json.backup  # Solo si todo funciona correctamente
```

## 📊 Comparación de Métodos de Seguridad

| Característica | Cifrado | Variables Entorno | Permisos Archivo |
|----------------|---------|-------------------|------------------|
| **Seguridad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Facilidad de Uso** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Portabilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **CI/CD Friendly** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Gestión Equipos** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Recuperación** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🔗 Referencias

- [Huawei Cloud OBS Security Best Practices](https://support.huaweicloud.com/intl/en-us/bestpractice-obs/)
- [Python Cryptography Documentation](https://cryptography.io/)
- [OWASP Secure Configuration Guide](https://owasp.org/www-project-secure-configuration-guide/)

---

**⚠️ Recordatorio de Seguridad:**
- Nunca compartas tus credenciales en código fuente
- Usa diferentes credenciales para desarrollo y producción
- Revisa regularmente los permisos de acceso
- Mantén actualizadas las dependencias de seguridad

---

**Desarrollado con ❤️ por CCVASS - Lima, Perú 🇵🇪**

**Soporte técnico:** [contact@ccvass.com](mailto:contact@ccvass.com)  
**Licencia:** Apache 2.0 | **Año:** 2025
