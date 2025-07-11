# 🔧 Guía Rápida - Superadministrador Windows

**Para el administrador que instala y configura OBS Utils en Windows**

---

**Desarrollado por:** [CCVASS](mailto:contact@ccvass.com) - Lima, Perú  
**Año:** 2025  
**Licencia:** Apache 2.0  
**Contacto:** contact@ccvass.com

---

## ⚡ Instalación Rápida (5 minutos)

### 1. **Requisitos Previos**
```cmd
REM Verificar Python (mínimo 3.7)
python --version

REM Si no tienes Python, descargar de: https://python.org
REM ✅ IMPORTANTE: Marcar "Add Python to PATH" durante instalación
```

### 2. **Instalación Automática**
```cmd
REM Descargar y extraer OBS Utils
REM Abrir Command Prompt como Administrador
cd C:\ruta\a\obs_utils

REM Ejecutar instalación automática
setup.bat

REM O instalación con seguridad avanzada
setup_secure.bat
```

### 3. **Configuración de Seguridad (Recomendado)**
```cmd
REM Configurar niveles de seguridad
python obs_utils_improved.py --setup-security-levels
```

**Configuración sugerida para empresa:**
- **Contraseña Maestra**: `Admin2024!@#`
- **READ_ONLY**: Sin contraseña (todos pueden ver)
- **STANDARD**: `Ops2024!` (operadores)
- **DESTRUCTIVE**: `Delete2024@` (supervisores)
- **ADMIN**: `SuperAdmin2024#` (solo tú)

## 🔐 Gestión de Usuarios y Permisos

### **Configuración por Roles**

#### **Usuario Básico (Solo Lectura)**
```cmd
REM Crear acceso directo con:
python obs_utils_improved.py --enable-security-levels
REM Solo podrá: listar, buscar, descargar
```

#### **Operador (Cambios de Storage)**
```cmd
REM Dar contraseña STANDARD: "Ops2024!"
REM Podrá: archivar, restaurar, cambiar storage class
```

#### **Supervisor (Eliminaciones)**
```cmd
REM Dar contraseña DESTRUCTIVE: "Delete2024@"
REM Podrá: eliminar objetos (con confirmación)
```

## 📋 Comandos de Administración

### **Ver Configuración Actual**
```cmd
python obs_utils_improved.py --list-security-levels
```

### **Cambiar Contraseñas**
```cmd
python obs_utils_improved.py --setup-security-levels
REM Reconfigurar con nuevas contraseñas
```

### **Verificar Instalación**
```cmd
python obs_utils_improved.py --help
```

### **Crear Usuarios con Diferentes Accesos**
```cmd
REM Crear accesos directos en escritorio:

REM Para usuarios básicos:
python obs_utils_improved.py --enable-security-levels

REM Para operadores (con parámetros específicos):
python obs_utils_improved.py --enable-security-levels --operation archive --bucket produccion

REM Para supervisores:
python obs_utils_improved.py --enable-security-levels --operation delete --bucket temporal
```

## 🛡️ Configuración de Seguridad Empresarial

### **Opción 1: Variables de Entorno (Recomendado para Servidores)**
```cmd
REM Configurar para toda la máquina
setx OBS_ACCESS_KEY_ID "AKIAI..." /M
setx OBS_SECRET_ACCESS_KEY "wJalr..." /M
setx OBS_SERVER "https://obs.sa-peru-1.myhuaweicloud.com/" /M

REM Reiniciar Command Prompt después de esto
```

### **Opción 2: Configuración Cifrada (Recomendado para Equipos)**
```cmd
REM Configurar archivo cifrado
python obs_utils_improved.py --setup-secure-config
REM Elegir opción 1: "Encrypted configuration"
REM Crear contraseña fuerte para el archivo
```

## 📁 Estructura de Archivos Importantes

```
C:\obs_utils\
├── obs_utils_improved.py          # Aplicación principal
├── obs_config.json.enc            # Configuración cifrada (si usas cifrado)
├── obs_config.json.salt           # Salt para cifrado
├── obs_security_levels.json.enc   # Niveles de seguridad cifrados
├── logs\                          # Logs de operaciones
└── run.bat                        # Script de ejecución rápida
```

## 🚨 Comandos de Emergencia

### **Resetear Configuración**
```cmd
REM Si olvidas contraseñas o hay problemas
del obs_config.json.enc
del obs_security_levels.json.enc
python obs_utils_improved.py --setup-security-levels
```

### **Verificar Logs**
```cmd
REM Ver últimas operaciones
type logs\obs_utils_*.log | findstr "ERROR"
```

### **Backup de Configuración**
```cmd
REM Respaldar configuración importante
copy obs_config.json.enc backup_config.enc
copy obs_security_levels.json.enc backup_security.enc
```

## 📊 Monitoreo y Auditoría

### **Ver Operaciones Recientes**
```cmd
REM Ver logs de hoy
powershell "Get-Content logs\obs_utils_*.log | Select-String 'INFO|ERROR' | Select-Object -Last 20"
```

### **Verificar Accesos por Usuario**
```cmd
REM Los logs muestran qué operaciones se realizaron
findstr "Access granted\|Access denied" logs\obs_utils_*.log
```

## 🎯 Distribución a Usuarios

### **Crear Paquete para Usuarios**
```cmd
REM Crear carpeta para distribución
mkdir C:\obs_utils_usuarios
copy obs_utils_improved.py C:\obs_utils_usuarios\
copy obs_config.json.enc C:\obs_utils_usuarios\
copy obs_config.json.salt C:\obs_utils_usuarios\
copy obs_security_levels.json.enc C:\obs_utils_usuarios\
copy run.bat C:\obs_utils_usuarios\

REM Crear acceso directo en escritorio
```

### **Instrucciones para Usuarios**
```cmd
REM Crear archivo de instrucciones
echo "Doble clic en run.bat para usar OBS Utils" > C:\obs_utils_usuarios\INSTRUCCIONES.txt
echo "Contactar al administrador si hay problemas" >> C:\obs_utils_usuarios\INSTRUCCIONES.txt
```

## 🔧 Solución de Problemas Comunes

### **Error: "Python no reconocido"**
```cmd
REM Agregar Python al PATH
set PATH=%PATH%;C:\Python39;C:\Python39\Scripts
REM O reinstalar Python marcando "Add to PATH"
```

### **Error: "Módulo no encontrado"**
```cmd
REM Reinstalar dependencias
pip install -r requirements.txt
```

### **Error: "Acceso denegado"**
```cmd
REM Ejecutar como administrador
REM Clic derecho en Command Prompt → "Ejecutar como administrador"
```

## 📞 Contacto y Soporte

**Para problemas técnicos:**
1. Revisar logs en carpeta `logs\`
2. Ejecutar: `python obs_utils_improved.py --help`
3. Verificar configuración: `python obs_utils_improved.py --list-security-levels`

**Archivos importantes a respaldar:**
- `obs_config.json.enc`
- `obs_security_levels.json.enc`
- `obs_config.json.salt`
- `obs_security_levels.json.salt`

---
**⚠️ IMPORTANTE:** Mantén seguras las contraseñas maestras y haz backups regulares de la configuración.

---

**Desarrollado con ❤️ por CCVASS - Lima, Perú 🇵🇪**

**Soporte técnico:** [contact@ccvass.com](mailto:contact@ccvass.com)  
**Licencia:** Apache 2.0 | **Año:** 2025
