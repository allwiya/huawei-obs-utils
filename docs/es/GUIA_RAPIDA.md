# 🚀 Guía Rápida de Usuario - OBS Utils

**Versión:** 2025  
**Desarrollado por:** [CCVASS](mailto:contact@ccvass.com) - Lima, Perú  
**Licencia:** Apache 2.0

---

## 📋 Índice

1. [Instalación Rápida](#-instalación-rápida)
2. [Configuración Inicial](#-configuración-inicial)
3. [Modos de Uso](#-modos-de-uso)
4. [Parámetros Completos](#-parámetros-completos)
5. [Operaciones Disponibles](#-operaciones-disponibles)
6. [Ejemplos Prácticos](#-ejemplos-prácticos)
7. [Configuración de Seguridad](#-configuración-de-seguridad)
8. [Solución Rápida de Problemas](#-solución-rápida-de-problemas)

---

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone <repository-url>
cd obs_utils

# Instalación automática
./setup.sh      # Linux/macOS
setup.bat       # Windows
```

---

## ⚙️ Configuración Inicial

### Opción 1: Configuración Segura (Recomendada) 🔐
```bash
python obs_utils_improved.py --setup-secure-config
```

### Opción 2: Variables de Entorno 🌍
```bash
export OBS_ACCESS_KEY_ID="tu_access_key"
export OBS_SECRET_ACCESS_KEY="tu_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

### Opción 3: Archivo de Configuración 📁
```bash
python obs_utils_improved.py --create-config
# Editar obs_config.json con tus credenciales
```

---

## 🎯 Modos de Uso

### Modo Interactivo (Principiantes)
```bash
python obs_utils_improved.py
```

### Modo Línea de Comandos (Avanzado)
```bash
python obs_utils_improved.py --operation <operacion> [parámetros]
```

---

## 📝 Parámetros Completos

### Parámetros Principales

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `--config` | string | Ruta del archivo de configuración | `--config mi_config.json` |
| `--operation` | choice | Operación a realizar | `--operation list` |
| `--bucket` | string | Nombre del bucket | `--bucket mi-bucket` |
| `--prefix` | string | Prefijo/ruta de objetos | `--prefix "carpeta/"` |
| `--object-key` | string | Clave específica de objeto | `--object-key "archivo.txt"` |
| `--download-path` | string | Ruta local de descarga | `--download-path "./descargas/"` |
| `--search-text` | string | Texto a buscar en nombres | `--search-text "backup"` |
| `--days` | integer | Días para restauración | `--days 30` |
| `--tier` | choice | Nivel de restauración | `--tier Expedited` |

### Parámetros de Configuración

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `--create-config` | flag | Crear archivo de configuración de ejemplo |
| `--setup-secure-config` | flag | Configuración segura interactiva |
| `--encrypt-config` | flag | Encriptar archivo de configuración existente |
| `--secure-permissions` | flag | Establecer permisos seguros |

### Parámetros de Seguridad Avanzada

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `--setup-security-levels` | flag | Configurar sistema de seguridad multinivel |
| `--list-security-levels` | flag | Listar niveles de seguridad configurados |
| `--enable-security-levels` | flag | Habilitar seguridad multinivel |

---

## 🔧 Operaciones Disponibles

### 1. **list** - Listar Objetos
**Descripción:** Lista objetos en un bucket
```bash
python obs_utils_improved.py --operation list --bucket mi-bucket
python obs_utils_improved.py --operation list --bucket mi-bucket --prefix "carpeta/"
```

### 2. **archive** - Archivar (COLD)
**Descripción:** Mueve objetos a almacenamiento COLD (más económico)
```bash
python obs_utils_improved.py --operation archive --bucket mi-bucket
python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "archivos-viejos/"
```

### 3. **warm** - Almacenamiento WARM
**Descripción:** Mueve objetos a almacenamiento WARM (acceso infrecuente)
```bash
python obs_utils_improved.py --operation warm --bucket mi-bucket
python obs_utils_improved.py --operation warm --bucket mi-bucket --prefix "datos-mensuales/"
```

### 4. **restore** - Restaurar Archivados
**Descripción:** Restaura objetos archivados para acceso temporal
```bash
python obs_utils_improved.py --operation restore --bucket mi-bucket
python obs_utils_improved.py --operation restore --bucket mi-bucket --days 7 --tier Expedited
```

### 5. **download** - Descargar Objetos
**Descripción:** Descarga objetos a directorio local
```bash
python obs_utils_improved.py --operation download --bucket mi-bucket --download-path "./descargas/"
python obs_utils_improved.py --operation download --bucket mi-bucket --prefix "reportes/" --download-path "./reportes/"
```

### 6. **search** - Buscar Objetos
**Descripción:** Busca objetos por nombre o patrón
```bash
python obs_utils_improved.py --operation search --search-text "backup"
python obs_utils_improved.py --operation search --bucket mi-bucket --search-text ".pdf"
```

---

## 💡 Ejemplos Prácticos

### Gestión Básica de Archivos

```bash
# Listar todos los archivos de un bucket
python obs_utils_improved.py --operation list --bucket documentos

# Listar archivos de una carpeta específica
python obs_utils_improved.py --operation list --bucket documentos --prefix "2024/enero/"

# Buscar archivos PDF
python obs_utils_improved.py --operation search --bucket documentos --search-text ".pdf"
```

### Gestión de Almacenamiento

```bash
# Archivar archivos antiguos (mover a COLD)
python obs_utils_improved.py --operation archive --bucket backups --prefix "2023/"

# Mover archivos a almacenamiento WARM
python obs_utils_improved.py --operation warm --bucket logs --prefix "logs-mensuales/"

# Restaurar archivos archivados por 7 días
python obs_utils_improved.py --operation restore --bucket backups --prefix "2023/importante/" --days 7
```

### Descargas Masivas

```bash
# Descargar toda una carpeta
python obs_utils_improved.py --operation download --bucket proyectos --prefix "proyecto-a/" --download-path "./proyecto-a/"

# Descargar archivos específicos
python obs_utils_improved.py --operation download --bucket documentos --object-key "informe-final.pdf" --download-path "./documentos/"
```

### Operaciones con Configuración Personalizada

```bash
# Usar archivo de configuración específico
python obs_utils_improved.py --config ./configs/produccion.json --operation list --bucket prod-data

# Operación con configuración encriptada
python obs_utils_improved.py --config ./configs/secure_config.enc --operation archive --bucket sensitive-data
```

---

## 🔒 Configuración de Seguridad

### Configuración Segura Paso a Paso

```bash
# 1. Configuración inicial segura
python obs_utils_improved.py --setup-secure-config

# 2. Encriptar configuración existente
python obs_utils_improved.py --encrypt-config

# 3. Establecer permisos seguros
python obs_utils_improved.py --secure-permissions

# 4. Configurar niveles de seguridad avanzados
python obs_utils_improved.py --setup-security-levels
```

### Verificación de Seguridad

```bash
# Listar niveles de seguridad configurados
python obs_utils_improved.py --list-security-levels

# Habilitar seguridad multinivel para sesión
python obs_utils_improved.py --enable-security-levels --operation list --bucket secure-bucket
```

---

## 🔍 Clases de Almacenamiento

| Clase | Descripción | Costo | Tiempo de Acceso | Uso Recomendado |
|-------|-------------|-------|------------------|-----------------|
| **STANDARD** | Acceso frecuente | Alto | Inmediato | Archivos activos |
| **WARM** | Acceso infrecuente | Medio | Inmediato | Archivos mensuales |
| **COLD** | Archivo | Bajo | Requiere restauración | Backups, archivos históricos |

### Niveles de Restauración

| Nivel | Tiempo | Costo | Uso |
|-------|--------|-------|-----|
| **Expedited** | 1-5 minutos | Alto | Urgente |
| **Standard** | 3-5 horas | Medio | Normal |
| **Bulk** | 5-12 horas | Bajo | Masivo |

---

## 🛠️ Solución Rápida de Problemas

### Errores Comunes

#### Error de Autenticación
```bash
# Verificar configuración
python obs_utils_improved.py --setup-secure-config

# Verificar variables de entorno
echo $OBS_ACCESS_KEY_ID
echo $OBS_SERVER
```

#### Error de Permisos
```bash
# Establecer permisos seguros
python obs_utils_improved.py --secure-permissions

# Verificar permisos del archivo
ls -la obs_config.json
```

#### Error de Conexión
```bash
# Verificar conectividad
ping obs.sa-peru-1.myhuaweicloud.com

# Verificar configuración de región
python obs_utils_improved.py --operation list --bucket test-bucket
```

### Comandos de Diagnóstico

```bash
# Verificar instalación
python --version
pip list | grep obs

# Verificar logs
tail -f logs/obs_utils.log

# Modo debug (agregar al comando)
python obs_utils_improved.py --operation list --bucket test --verbose
```

---

## 📞 Soporte y Contacto

### **CCVASS - Lima, Perú**
- **Email:** [contact@ccvass.com](mailto:contact@ccvass.com)
- **Año:** 2025
- **Licencia:** Apache 2.0

### Recursos de Ayuda
- **Documentación Completa:** [docs/es/](../es/)
- **Ejemplos Avanzados:** [EJEMPLOS.md](EJEMPLOS.md)
- **Guía de Seguridad:** [SEGURIDAD.md](SEGURIDAD.md)
- **Solución de Problemas:** [SOLUCION_PROBLEMAS.md](SOLUCION_PROBLEMAS.md)

---

## 🎯 Comandos Más Utilizados

```bash
# Top 10 comandos más comunes

# 1. Listar archivos
python obs_utils_improved.py --operation list --bucket mi-bucket

# 2. Buscar archivos
python obs_utils_improved.py --operation search --search-text "backup"

# 3. Descargar carpeta
python obs_utils_improved.py --operation download --bucket datos --prefix "reportes/" --download-path "./reportes/"

# 4. Archivar archivos antiguos
python obs_utils_improved.py --operation archive --bucket backups --prefix "2023/"

# 5. Configuración segura
python obs_utils_improved.py --setup-secure-config

# 6. Restaurar archivos
python obs_utils_improved.py --operation restore --bucket archivos --days 7

# 7. Mover a WARM
python obs_utils_improved.py --operation warm --bucket logs --prefix "logs-antiguos/"

# 8. Listar con filtro
python obs_utils_improved.py --operation list --bucket documentos --prefix "2024/"

# 9. Descargar archivo específico
python obs_utils_improved.py --operation download --bucket docs --object-key "importante.pdf" --download-path "./"

# 10. Modo interactivo
python obs_utils_improved.py
```

---

**Desarrollado con ❤️ por CCVASS - Lima, Perú 🇵🇪**

**¿Necesitas ayuda?** Consulta la [Guía de Solución de Problemas](SOLUCION_PROBLEMAS.md) o contacta [contact@ccvass.com](mailto:contact@ccvass.com).
