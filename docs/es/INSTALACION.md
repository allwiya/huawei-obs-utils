# Guía de Instalación

Esta guía te ayudará a instalar y configurar OBS Utils en tu sistema.

## Requisitos del Sistema

- **Python**: 3.7 o superior
- **Sistema Operativo**: Linux, macOS, Windows
- **Memoria**: Mínimo 512MB RAM
- **Espacio en Disco**: 100MB para instalación y logs
- **Conectividad**: Acceso a Internet para Huawei Cloud OBS

## Métodos de Instalación

### Método 1: Instalación Automática (Recomendado)

#### Linux/macOS
```bash
# Clonar el repositorio
git clone <repository-url>
cd obs_utils

# Ejecutar configuración automática
chmod +x setup.sh
./setup.sh
```

#### Windows
```cmd
# Clonar el repositorio
git clone <repository-url>
cd obs_utils

# Ejecutar configuración automática
setup.bat
```

### Método 2: Instalación Manual

#### Paso 1: Clonar Repositorio
```bash
git clone <repository-url>
cd obs_utils
```

#### Paso 2: Crear Entorno Virtual
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 4: Verificar Instalación
```bash
python obs_utils_improved.py --help
```

## Configuración Post-Instalación

### 1. Configuración
Elige tu método de configuración preferido:
- [Configuración Encriptada](CONFIGURACION.md#configuración-encriptada) (Más Segura)
- [Variables de Entorno](CONFIGURACION.md#variables-de-entorno) (Recomendado para Servidores)
- [Archivo de Configuración](CONFIGURACION.md#archivo-de-configuración) (Básico)

### 2. Configuración de Seguridad
Sigue la [Guía de Seguridad](SEGURIDAD.md) para asegurar una configuración de seguridad adecuada.

### 3. Probar Instalación
```bash
# Probar funcionalidad básica
python obs_utils_improved.py --operation list --bucket test-bucket
```

## Solución de Problemas

### Problemas Comunes

#### Error de Versión de Python
```bash
# Verificar versión de Python
python --version
python3 --version

# Usar Python 3.7+
python3 obs_utils_improved.py
```

#### Errores de Permisos (Linux/macOS)
```bash
# Corregir permisos de scripts
chmod +x setup.sh
chmod +x obs_utils_improved.py
```

#### Módulo No Encontrado
```bash
# Asegurar que el entorno virtual esté activado
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problemas Específicos de Windows
Consulta la [Guía Windows](GUIA_WINDOWS.md) para instrucciones específicas de instalación en Windows.

## Verificación

Después de la instalación, verifica que todo funcione:

```bash
# Verificar versión
python obs_utils_improved.py --version

# Probar configuración
python obs_utils_improved.py --test-config

# Ejecutar modo interactivo
python obs_utils_improved.py
```

## Siguientes Pasos

1. [Configurar tus credenciales](CONFIGURACION.md)
2. [Revisar configuraciones de seguridad](SEGURIDAD.md)
3. [Probar los ejemplos](EJEMPLOS.md)
4. [Leer la referencia API](API.md)

## Soporte

Si encuentras problemas durante la instalación:
- Revisa la [Guía de Solución de Problemas](SOLUCION_PROBLEMAS.md)
- Revisa los logs en el directorio `logs/`
- Contacta [contact@ccvass.com](mailto:contact@ccvass.com)

---

**Desarrollado por CCVASS - Lima, Perú 🇵🇪**
