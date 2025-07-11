# Guía de Configuración

Esta guía explica cómo configurar OBS Utils con tus credenciales de Huawei Cloud usando diferentes métodos de seguridad.

## Métodos de Configuración

### Método 1: Configuración Encriptada (Más Segura) 🔐

Este método almacena tus credenciales en un archivo encriptado usando encriptación AES-256.

#### Configuración
```bash
python obs_utils_improved.py --setup-secure-config
```

#### Proceso de Configuración Interactiva
1. Ingresa tus credenciales OBS
2. Crea una contraseña de encriptación fuerte
3. Las credenciales se encriptan y almacenan de forma segura
4. Los permisos del archivo se establecen en 600 (solo lectura/escritura del propietario)

#### Beneficios
- ✅ Credenciales encriptadas con AES-256
- ✅ Permisos de archivo seguros
- ✅ Acceso protegido por contraseña
- ✅ Validación automática de seguridad

### Método 2: Variables de Entorno (Recomendado para Servidores) 🌍

Mejor para entornos de servidor y pipelines CI/CD.

#### Configuración Linux/macOS
```bash
export OBS_ACCESS_KEY_ID="tu_access_key"
export OBS_SECRET_ACCESS_KEY="tu_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

#### Configuración Windows
```cmd
set OBS_ACCESS_KEY_ID=tu_access_key
set OBS_SECRET_ACCESS_KEY=tu_secret_key
set OBS_SERVER=https://obs.sa-peru-1.myhuaweicloud.com/
set OBS_REGION=sa-peru-1
```

#### Variables de Entorno Persistentes

**Linux/macOS** (agregar a ~/.bashrc o ~/.zshrc):
```bash
echo 'export OBS_ACCESS_KEY_ID="tu_access_key"' >> ~/.bashrc
echo 'export OBS_SECRET_ACCESS_KEY="tu_secret_key"' >> ~/.bashrc
echo 'export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"' >> ~/.bashrc
echo 'export OBS_REGION="sa-peru-1"' >> ~/.bashrc
source ~/.bashrc
```

**Windows** (Propiedades del Sistema > Variables de Entorno):
1. Abrir Propiedades del Sistema
2. Hacer clic en "Variables de Entorno"
3. Agregar nuevas variables del sistema

### Método 3: Archivo de Configuración (Básico) 📁

Configuración simple basada en archivos.

#### Crear Configuración
```bash
python obs_utils_improved.py --create-config
```

#### Configuración Manual
Crear `obs_config.json`:
```json
{
    "access_key_id": "tu_access_key",
    "secret_access_key": "tu_secret_key",
    "server": "https://obs.sa-peru-1.myhuaweicloud.com/",
    "region": "sa-peru-1"
}
```

#### Permisos de Archivo Seguros
```bash
# Linux/macOS
chmod 600 obs_config.json

# Windows (PowerShell como Administrador)
icacls obs_config.json /inheritance:r /grant:r "%USERNAME%:F"
```

## Regiones de Huawei Cloud

Endpoints OBS comunes por región:

| Región | Endpoint |
|--------|----------|
| **Sudamérica (Perú)** | `https://obs.sa-peru-1.myhuaweicloud.com/` |
| **Asia Pacífico (Singapur)** | `https://obs.ap-southeast-1.myhuaweicloud.com/` |
| **Europa (París)** | `https://obs.eu-west-101.myhuaweicloud.com/` |
| **Norteamérica (México)** | `https://obs.na-mexico-1.myhuaweicloud.com/` |
| **Asia Pacífico (Hong Kong)** | `https://obs.ap-southeast-1.myhuaweicloud.com/` |

## Obtener tus Credenciales

### Paso 1: Acceder a la Consola de Huawei Cloud
1. Ir a [Consola de Huawei Cloud](https://console.huaweicloud.com/)
2. Iniciar sesión en tu cuenta

### Paso 2: Crear Claves de Acceso
1. Hacer clic en tu nombre de usuario (esquina superior derecha)
2. Seleccionar "Mis Credenciales"
3. Ir a la pestaña "Claves de Acceso"
4. Hacer clic en "Crear Clave de Acceso"
5. Descargar el archivo de credenciales

### Paso 3: Anotar tu Región
1. Ir a la Consola OBS
2. Verificar la región en la URL o menú desplegable
3. Usar el endpoint correspondiente

## Prioridad de Configuración

OBS Utils verifica la configuración en este orden:

1. **Argumentos de línea de comandos** (prioridad más alta)
2. **Variables de entorno**
3. **Archivo de configuración encriptado**
4. **Archivo de configuración plano** (prioridad más baja)

## Probar Configuración

### Probar Conexión
```bash
python obs_utils_improved.py --test-config
```

### Listar Buckets (Verificar Acceso)
```bash
python obs_utils_improved.py --operation list
```

### Prueba en Modo Interactivo
```bash
python obs_utils_improved.py
# Seleccionar opción 1 (Listar objetos)
```

## Mejores Prácticas de Seguridad

### ✅ Recomendado
- Usar configuración encriptada para desarrollo local
- Usar variables de entorno para servidores/contenedores
- Establecer permisos de archivo apropiados (600)
- Usar contraseñas de encriptación fuertes
- Rotar regularmente las claves de acceso

### ❌ Evitar
- Almacenar credenciales en código
- Usar archivos de configuración legibles por todos
- Compartir archivos de configuración
- Usar contraseñas de encriptación débiles
- Confirmar credenciales en control de versiones

## Configuración Avanzada

### Ubicación Personalizada del Archivo de Configuración
```bash
python obs_utils_improved.py --config-file /ruta/a/config/personalizado.json
```

### Múltiples Perfiles
Crear diferentes archivos de configuración para diferentes entornos:
```bash
# Desarrollo
python obs_utils_improved.py --config-file config-dev.json

# Producción
python obs_utils_improved.py --config-file config-prod.json
```

### Configuración de Logging
Establecer nivel de logging vía variable de entorno:
```bash
export OBS_LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

## Solución de Problemas

### Problemas Comunes

#### Credenciales Inválidas
```
Error: Acceso denegado o credenciales inválidas
```
**Solución**: Verificar que tu clave de acceso y clave secreta sean correctas.

#### Región/Endpoint Incorrecto
```
Error: Tiempo de conexión agotado o servidor no encontrado
```
**Solución**: Verificar que tu región y endpoint del servidor coincidan con la ubicación de tu bucket.

#### Permiso Denegado
```
Error: Permiso denegado accediendo al archivo de configuración
```
**Solución**: Verificar permisos y propiedad del archivo.

#### Problemas con Contraseña de Encriptación
```
Error: Falló al desencriptar configuración
```
**Solución**: Verificar que tu contraseña de encriptación sea correcta.

### Obtener Ayuda

1. Revisar la [Guía de Solución de Problemas](SOLUCION_PROBLEMAS.md)
2. Revisar logs en el directorio `logs/`
3. Probar con la bandera `--test-config`
4. Contactar [contact@ccvass.com](mailto:contact@ccvass.com)

## Siguientes Pasos

1. [Revisar configuraciones de seguridad](SEGURIDAD.md)
2. [Probar los ejemplos](EJEMPLOS.md)
3. [Leer la referencia API](API.md)
4. [Aprender sobre solución de problemas](SOLUCION_PROBLEMAS.md)

---

**Desarrollado por CCVASS - Lima, Perú 🇵🇪**
