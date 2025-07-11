# 🚀 Inicio Rápido - Windows

## ⚡ Instalación en 5 Minutos

### Paso 1: Verificar Requisitos
```cmd
# Abrir Command Prompt o PowerShell
# Verificar Python (versión 3.8 o superior)
python --version

# Si no tienes Python, descargar desde:
# https://www.python.org/downloads/windows/
```

### Paso 2: Descargar OBS Utils
```cmd
# Opción A: Con Git
git clone https://github.com/ccvass/obs-utils.git
cd obs-utils

# Opción B: Descarga directa
# Descargar ZIP desde GitHub y extraer
cd obs-utils-main
```

### Paso 3: Instalación Automática
```cmd
# Ejecutar script de instalación
setup.bat

# O instalación manual
pip install -r requirements.txt
```

## 🔧 Configuración Rápida

### Configuración Básica (2 minutos)
```cmd
# Crear archivo de configuración
python obs_utils_improved.py --create-config

# Editar obs_config.json con tus credenciales:
{
  "access_key_id": "TU_ACCESS_KEY",
  "secret_access_key": "TU_SECRET_KEY", 
  "server": "https://obs.sa-peru-1.myhuaweicloud.com/",
  "region": "sa-peru-1"
}
```

### Configuración Segura (5 minutos)
```cmd
# Configuración con encriptación AES-256
python obs_utils_improved.py --setup-secure-config

# Seguir las instrucciones para:
# 1. Ingresar credenciales
# 2. Establecer contraseña de encriptación
# 3. Confirmar configuración
```

## 🎯 Primeros Pasos

### Verificar Conexión
```cmd
# Probar conexión
python obs_utils_improved.py --test-connection

# Listar buckets disponibles
python obs_utils_improved.py --list-buckets
```

### Operaciones Básicas

#### 📋 Listar Archivos
```cmd
# Listar objetos en un bucket
python obs_utils_improved.py --operation list --bucket mi-bucket

# Modo interactivo (más fácil para principiantes)
python obs_utils_improved.py
```

#### 🔍 Buscar Archivos
```cmd
# Buscar archivos por nombre
python obs_utils_improved.py --operation search --search-text "backup"

# Buscar en bucket específico
python obs_utils_improved.py --operation search --bucket mi-bucket --search-text "2025"
```

#### ⬇️ Descargar Archivos
```cmd
# Descargar archivo específico
python obs_utils_improved.py --operation download --bucket mi-bucket --key "archivo.pdf"

# Descargar múltiples archivos
python obs_utils_improved.py --operation download --bucket mi-bucket --prefix "reportes/"
```

## 🗄️ Gestión de Almacenamiento

### Archivar Archivos (Ahorro de Costos)
```cmd
# Archivar archivos antiguos a COLD storage (más barato)
python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "archivos-2024/"

# Nota: Requiere contraseña de operador
```

### Restaurar Archivos Archivados
```cmd
# Restaurar archivos desde COLD storage
python obs_utils_improved.py --operation restore --bucket mi-bucket --prefix "archivos-2024/"

# Restauración rápida (más costosa)
python obs_utils_improved.py --operation restore --bucket mi-bucket --key "archivo.pdf" --tier expedited
```

## 🖥️ Modo Interactivo (Recomendado para Principiantes)

### Iniciar Modo Interactivo
```cmd
python obs_utils_improved.py
```

### Menú Principal
```
=== OBS Utils - Huawei Cloud Storage ===

🔧 Configuración:
1. ⚙️  Crear configuración
2. 🔒 Configuración segura
3. 🧪 Probar conexión

📋 Operaciones:
4. 📋 Listar objetos
5. 🔍 Buscar archivos
6. ⬇️  Descargar archivos
7. 🗄️  Archivar archivos
8. 🔄 Restaurar archivos

📊 Información:
9. 📊 Estadísticas de uso
10. 📈 Reporte de costos
11. ❓ Ayuda

12. ❌ Salir

Seleccione una opción (1-12):
```

## 🔒 Configuración de Seguridad

### Niveles de Seguridad Disponibles

#### 🟢 Nivel 1: READ_ONLY (Sin contraseña)
- Listar archivos
- Buscar archivos  
- Descargar archivos

#### 🟡 Nivel 2: STANDARD (Contraseña de operador)
- Archivar archivos
- Restaurar archivos
- Cambiar clase de almacenamiento

#### 🟠 Nivel 3: DESTRUCTIVE (Contraseña de supervisor)
- Eliminar archivos
- Operaciones masivas de eliminación

#### 🔴 Nivel 4: ADMIN (Contraseña de administrador)
- Crear/eliminar buckets
- Configuración del sistema
- Gestión de usuarios

### Habilitar Seguridad Multinivel
```cmd
# Habilitar sistema de seguridad
python obs_utils_improved.py --enable-security-levels

# Configurar contraseñas por nivel
python obs_utils_improved.py --set-operator-password
python obs_utils_improved.py --set-supervisor-password
python obs_utils_improved.py --set-admin-password
```

## 📊 Monitoreo Básico

### Ver Estadísticas
```cmd
# Estadísticas del bucket
python obs_utils_improved.py --operation stats --bucket mi-bucket

# Uso por clase de almacenamiento
python obs_utils_improved.py --operation storage-stats --bucket mi-bucket
```

### Generar Reportes
```cmd
# Reporte diario
python obs_utils_improved.py --generate-report --type daily

# Reporte de costos
python obs_utils_improved.py --generate-report --type costs --period monthly
```

## 🚨 Solución de Problemas Rápida

### Error: "Python no reconocido"
```cmd
# Verificar instalación de Python
where python

# Si no está instalado, descargar desde python.org
# Asegurarse de marcar "Add Python to PATH" durante la instalación
```

### Error: "Módulo no encontrado"
```cmd
# Instalar dependencias
pip install -r requirements.txt

# O instalar individualmente
pip install obs-python-sdk cryptography
```

### Error: "Credenciales inválidas"
```cmd
# Verificar credenciales
python obs_utils_improved.py --test-connection

# Reconfigurar credenciales
python obs_utils_improved.py --create-config
```

### Error: "Acceso denegado"
```cmd
# Verificar permisos del bucket
python obs_utils_improved.py --check-permissions --bucket mi-bucket

# Contactar al administrador si es necesario
```

## 📋 Lista de Verificación Rápida

### Instalación Completa
- [ ] Python 3.8+ instalado
- [ ] OBS Utils descargado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Configuración creada (`--create-config` o `--setup-secure-config`)
- [ ] Conexión probada (`--test-connection`)

### Primera Operación Exitosa
- [ ] Listar buckets (`--list-buckets`)
- [ ] Listar objetos en un bucket (`--operation list --bucket mi-bucket`)
- [ ] Descargar un archivo de prueba
- [ ] Verificar archivo descargado

## 🎓 Próximos Pasos

### Para Usuarios Básicos
1. Explorar el modo interactivo
2. Practicar operaciones de descarga
3. Aprender a buscar archivos eficientemente
4. Configurar notificaciones por email

### Para Usuarios Avanzados
1. Configurar seguridad multinivel
2. Automatizar operaciones con scripts
3. Configurar monitoreo y alertas
4. Implementar estrategias de archivo para ahorro de costos

### Para Administradores
1. Revisar [Guía del Superadministrador](GUIA_SUPERADMIN_WINDOWS.md)
2. Configurar usuarios y permisos
3. Implementar políticas de seguridad
4. Configurar backup y recuperación

## 📚 Documentación Adicional

### Guías Específicas
- [Guía del Operador](GUIA_OPERADOR_WINDOWS.md) - Para uso diario
- [Guía del Superadministrador](GUIA_SUPERADMIN_WINDOWS.md) - Para administradores
- [Guía de Seguridad](SECURITY.md) - Mejores prácticas de seguridad

### Documentación Técnica
- [README Principal](README.md) - Documentación completa
- [Guía de Instalación](docs/es/INSTALACION.md) - Instalación detallada
- [Solución de Problemas](docs/es/SOLUCION_PROBLEMAS.md) - Problemas comunes
- [API Reference](docs/es/API.md) - Referencia técnica

## 💬 Soporte

### Contactos
- **Soporte General**: contact@ccvass.com
- **Soporte Técnico**: support@ccvass.com
- **Emergencias**: +51-xxx-xxx-xxxx

### Recursos de Ayuda
```cmd
# Ayuda integrada
python obs_utils_improved.py --help

# Ejemplos de uso
python obs_utils_improved.py --examples

# Tutorial interactivo
python obs_utils_improved.py --tutorial
```

### Comunidad
- **GitHub Issues**: Para reportar bugs
- **Documentación**: Guías completas en `/docs`
- **Ejemplos**: Casos de uso en `/examples`

---

**¡Listo para empezar! 🎉**

Con esta guía rápida ya puedes comenzar a usar OBS Utils de forma segura y eficiente.

**Desarrollado por**: CCVASS - Lima, Perú 🇵🇪  
**Contacto**: contact@ccvass.com  
**Versión**: 2.0.0  
**Última Actualización**: Julio 2025
