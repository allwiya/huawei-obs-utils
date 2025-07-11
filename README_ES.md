# OBS Utils - Utilidades para Huawei Cloud Object Storage

Una herramienta integral y **segura** para gestionar objetos en **Huawei Cloud Object Storage Service (OBS)** con manejo robusto de errores, configuración segura de credenciales y arquitectura modular.

**Compatible con Linux, macOS y Windows** 🐧🍎🪟

---

**Desarrollado por:** [CCVASS](mailto:contact@ccvass.com) - Lima, Perú  
**Año:** 2025  
**Licencia:** Apache 2.0  
**Contacto:** contact@ccvass.com

---

## 🔒 **NUEVO: Características Avanzadas de Seguridad**

- **🔐 Configuración Encriptada**: Credenciales protegidas con encriptación AES-256
- **🛡️ Múltiples Métodos de Autenticación**: Archivos encriptados, variables de entorno, permisos seguros
- **⚠️ Detección de Configuración Insegura**: Alertas automáticas para permisos de archivos
- **🔑 Gestión de Contraseñas**: Cambios seguros de contraseñas de encriptación
- **📋 Guía Completa de Seguridad**: Mejores prácticas y configuración paso a paso

## 🌍 Idiomas de Documentación

- **English**: [Complete Documentation](docs/en/) | [README in English](README.md)
- **Español**: [Documentación Completa](docs/es/)

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd obs_utils

# Ejecutar configuración automática
./setup.sh  # Linux/macOS
setup.bat   # Windows
```

### Configuración

Elige tu método de seguridad preferido:

#### Opción 1: Configuración Encriptada (Más Segura) 🔐
```bash
python obs_utils_improved.py --setup-secure-config
```

#### Opción 2: Variables de Entorno (Recomendado para Servidores) 🌍
```bash
export OBS_ACCESS_KEY_ID="tu_access_key"
export OBS_SECRET_ACCESS_KEY="tu_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

#### Opción 3: Archivo de Configuración (Básico) 📁
```bash
python obs_utils_improved.py --create-config
# Editar obs_config.json con tus credenciales
```

### Uso

#### Modo Interactivo (Principiantes)
```bash
python obs_utils_improved.py
```

#### Modo Línea de Comandos (Avanzado)
```bash
# Listar objetos en un bucket
python obs_utils_improved.py --operation list --bucket mi-bucket

# Archivar archivos antiguos a almacenamiento COLD
python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "archivos-antiguos/"

# Buscar archivos
python obs_utils_improved.py --operation search --search-text "backup"

# Descargar archivos
python obs_utils_improved.py --operation download --bucket mi-bucket --prefix "reportes/"
```

## ✨ Características Principales

- 🔒 **Configuración segura**: Credenciales encriptadas, variables de entorno o permisos de archivo seguros
- 🛡️ **Manejo robusto de errores**: Validación de entrada y manejo integral de excepciones
- 📝 **Registro avanzado**: Logs estructurados en archivos y consola con diferentes niveles
- 🧩 **Código modular**: Separación clara de responsabilidades en múltiples módulos
- 🖥️ **Modo dual**: Modos interactivo y línea de comandos para máxima flexibilidad
- 📄 **Paginación automática**: Manejo eficiente de grandes cantidades de objetos
- ✅ **Validación completa**: Entrada de usuario segura y validada
- 🔄 **Operaciones por lotes**: Procesamiento masivo de archivos
- 📊 **Progreso visual**: Indicadores de progreso y contadores de elementos procesados
- **🔐 Encriptación AES-256**: Máxima protección para credenciales sensibles
- **⚠️ Alertas de Seguridad**: Detección automática de configuraciones inseguras

## 📚 Operaciones Disponibles

| Operación | Descripción | Comando CLI |
|-----------|-------------|-------------|
| **list** | Listar objetos en bucket | `--operation list --bucket mi-bucket` |
| **archive** | Mover a almacenamiento COLD (más barato) | `--operation archive --bucket mi-bucket` |
| **warm** | Mover a almacenamiento WARM (acceso infrecuente) | `--operation warm --bucket mi-bucket` |
| **restore** | Restaurar objetos archivados | `--operation restore --bucket mi-bucket` |
| **download** | Descargar objetos | `--operation download --bucket mi-bucket` |
| **search** | Buscar objetos por nombre | `--operation search --search-text "backup"` |

## 🔧 Clases de Almacenamiento

| Clase | Descripción | Costo | Tiempo de Acceso |
|-------|-------------|-------|------------------|
| **STANDARD** | Acceso frecuente | Alto | Inmediato |
| **WARM** | Acceso infrecuente | Medio | Inmediato |
| **COLD** | Archivo | Bajo | Requiere restauración |

## 📖 Documentación

### Documentación en Español
- **[📚 Guía Rápida de Usuario](docs/es/GUIA_RAPIDA.md)** - Parámetros completos y ejemplos
- [Guía de Instalación](docs/es/INSTALACION.md)
- [Guía de Configuración](docs/es/CONFIGURACION.md)
- [Guía de Seguridad](docs/es/SEGURIDAD.md)
- [Referencia API](docs/es/API.md)
- [Ejemplos](docs/es/EJEMPLOS.md)
- [Solución de Problemas](docs/es/SOLUCION_PROBLEMAS.md)
- [Guía Windows](docs/es/GUIA_WINDOWS.md)

### Documentación en Inglés
- **[📚 Quick User Guide](docs/en/QUICK_GUIDE.md)** - Complete parameters and examples
- [Installation Guide](docs/en/INSTALLATION.md)
- [Configuration Guide](docs/en/CONFIGURATION.md)
- [Security Guide](docs/en/SECURITY.md)
- [API Reference](docs/en/API.md)
- [Examples](docs/en/EXAMPLES.md)
- [Troubleshooting](docs/en/TROUBLESHOOTING.md)
- [Windows Guide](docs/en/WINDOWS_GUIDE.md)

## 🖥️ Requisitos del Sistema

- **Python**: 3.7 o superior
- **Sistema Operativo**: Linux, macOS, Windows
- **Memoria**: Mínimo 512MB RAM
- **Espacio en Disco**: 100MB para instalación y logs
- **Conectividad**: Acceso a Internet para Huawei Cloud OBS

## 🛠️ Desarrollo

### Estructura del Proyecto
```
obs_utils/
├── obs_utils_improved.py    # Script principal con CLI
├── obs_manager.py          # Clase principal OBSManager
├── config.py              # Gestión de configuración
├── logger.py              # Sistema de logging
├── security.py            # Utilidades de seguridad
├── requirements.txt       # Dependencias de Python
├── setup.sh              # Script de instalación
├── README.md             # Documentación principal (Inglés)
├── README_ES.md          # Esta documentación (Español)
├── LICENSE               # Licencia Apache 2.0
└── docs/                 # Directorio de documentación
    ├── en/              # Documentación en inglés
    └── es/              # Documentación en español
```

### Contribuir

1. Hacer fork del repositorio
2. Crear una rama de característica: `git checkout -b feature/nueva-caracteristica`
3. Confirmar cambios: `git commit -am 'Agregar nueva característica'`
4. Push a la rama: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia Apache 2.0**. Ver el archivo [`LICENSE`](LICENSE) para detalles.

## 🆘 Soporte

### **Contacto CCVASS**
- **Email**: [contact@ccvass.com](mailto:contact@ccvass.com)
- **Empresa**: CCVASS - Lima, Perú
- **Año**: 2025

### **Recursos de Ayuda**
- **Issues**: Reportar problemas en el repositorio
- **Documentación**: Guías completas en el directorio [docs/](docs/)
- **Logs**: Revisar archivos en `logs/` para depuración
- **Huawei Cloud**: Documentación oficial de OBS

---

**Desarrollado con ❤️ por CCVASS - Lima, Perú 🇵🇪**

**¿Necesitas ayuda?** Revisa la [Guía de Solución de Problemas](docs/es/SOLUCION_PROBLEMAS.md) o contacta [contact@ccvass.com](mailto:contact@ccvass.com).
