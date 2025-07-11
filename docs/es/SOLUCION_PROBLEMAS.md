# Guía de Solución de Problemas

Esta guía te ayuda a resolver problemas comunes al usar OBS Utils.

## Diagnóstico Rápido

### Probar tu Configuración
```bash
python obs_utils_improved.py --test-config
```

### Revisar Logs
```bash
# Ver logs recientes
tail -f logs/obs_utils.log

# Ver solo errores
grep ERROR logs/obs_utils.log
```

### Verificar Instalación
```bash
python obs_utils_improved.py --version
python obs_utils_improved.py --help
```

## Problemas Comunes

### 1. Problemas de Configuración

#### Problema: "Archivo de configuración no encontrado"
```
Error: Configuration file 'obs_config.json' not found
```

**Soluciones:**
```bash
# Crear nueva configuración
python obs_utils_improved.py --create-config

# O usar variables de entorno
export OBS_ACCESS_KEY_ID="tu_clave"
export OBS_SECRET_ACCESS_KEY="tu_secreto"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"

# O especificar ubicación del archivo de configuración
python obs_utils_improved.py --config-file /ruta/a/config.json
```

#### Problema: "Credenciales inválidas"
```
Error: Access denied or invalid credentials
```

**Soluciones:**
1. **Verificar credenciales en la Consola de Huawei Cloud:**
   - Ir a "Mis Credenciales" > "Claves de Acceso"
   - Verificar si la clave de acceso está activa
   - Regenerar si es necesario

2. **Verificar configuración:**
   ```bash
   # Probar configuración
   python obs_utils_improved.py --test-config
   
   # Recrear configuración
   python obs_utils_improved.py --create-config
   ```

3. **Verificar región y endpoint:**
   ```bash
   # Endpoints comunes
   # Perú: https://obs.sa-peru-1.myhuaweicloud.com/
   # Singapur: https://obs.ap-southeast-1.myhuaweicloud.com/
   ```

#### Problema: "Falló al desencriptar configuración"
```
Error: Failed to decrypt configuration file
```

**Soluciones:**
```bash
# Cambiar contraseña de encriptación
python obs_utils_improved.py --change-password

# O recrear configuración encriptada
python obs_utils_improved.py --setup-secure-config
```

### 2. Problemas de Conexión

#### Problema: "Tiempo de conexión agotado"
```
Error: Connection timeout or server not found
```

**Soluciones:**
1. **Verificar conectividad a Internet:**
   ```bash
   ping obs.sa-peru-1.myhuaweicloud.com
   ```

2. **Verificar URL del endpoint:**
   - Asegurar endpoint correcto de la región
   - Verificar errores tipográficos en la URL del servidor
   - Verificar protocolo HTTPS

3. **Verificar firewall/proxy:**
   ```bash
   # Probar con curl
   curl -I https://obs.sa-peru-1.myhuaweicloud.com/
   ```

#### Problema: "Falló la verificación del certificado SSL"
```
Error: SSL certificate verification failed
```

**Soluciones:**
```bash
# Actualizar certificados (Linux)
sudo apt-get update && sudo apt-get install ca-certificates

# Actualizar certificados (macOS)
brew install ca-certificates

# Solo para desarrollo (no recomendado para producción)
export PYTHONHTTPSVERIFY=0
```

### 3. Problemas de Permisos

#### Problema: "Acceso denegado al bucket"
```
Error: Access denied to bucket 'mi-bucket'
```

**Soluciones:**
1. **Verificar permisos del bucket en la Consola OBS:**
   - Verificar que el bucket existe
   - Revisar política del bucket
   - Verificar permisos IAM

2. **Probar con bucket diferente:**
   ```bash
   python obs_utils_improved.py --operation list --bucket bucket-prueba
   ```

#### Problema: "Permiso denegado accediendo al archivo de configuración"
```
Error: Permission denied: obs_config.json
```

**Soluciones:**
```bash
# Corregir permisos de archivo (Linux/macOS)
chmod 600 obs_config.json
chown $USER obs_config.json

# Windows (PowerShell como Administrador)
icacls obs_config.json /inheritance:r /grant:r "%USERNAME%:F"
```

### 4. Problemas del Entorno Python

#### Problema: "ModuleNotFoundError"
```
ModuleNotFoundError: No module named 'obs'
```

**Soluciones:**
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# O instalar módulo específico
pip install esdk-obs-python
```

#### Problema: "Versión de Python no soportada"
```
Error: Python 3.7+ required
```

**Soluciones:**
```bash
# Verificar versión de Python
python --version
python3 --version

# Usar versión correcta de Python
python3 obs_utils_improved.py

# O instalar Python 3.7+
# Ubuntu/Debian
sudo apt-get install python3.8

# macOS
brew install python@3.8

# Windows: Descargar desde python.org
```

### 5. Problemas de Clases de Almacenamiento

#### Problema: "No se puede restaurar objeto"
```
Error: Object is not in COLD storage class
```

**Soluciones:**
- Solo objetos en almacenamiento COLD pueden ser restaurados
- Verificar clase de almacenamiento del objeto primero:
  ```bash
  python obs_utils_improved.py --operation list --bucket mi-bucket
  ```

#### Problema: "Falló operación de archivo"
```
Error: Failed to change storage class
```

**Soluciones:**
1. **Verificar edad del objeto:**
   - Los objetos deben cumplir duración mínima de almacenamiento
   - WARM: 30 días mínimo
   - COLD: 90 días mínimo

2. **Verificar permisos:**
   - Asegurar permisos de escritura al bucket
   - Verificar políticas IAM

### 6. Problemas de Rendimiento

#### Problema: "La operación es muy lenta"

**Soluciones:**
1. **Usar filtrado por prefijo:**
   ```bash
   # En lugar de listar todos los objetos
   python obs_utils_improved.py --operation list --bucket bucket-enorme
   
   # Usar prefijo para limitar alcance
   python obs_utils_improved.py --operation list --bucket bucket-enorme --prefix "2024/"
   ```

2. **Ajustar max-keys:**
   ```bash
   # Reducir tamaño de lote para buckets grandes
   python obs_utils_improved.py --operation list --bucket mi-bucket --max-keys 100
   ```

3. **Verificar conectividad de red:**
   ```bash
   # Probar velocidad de descarga
   speedtest-cli
   ```

#### Problema: "Uso de memoria muy alto"

**Soluciones:**
1. **Procesar en lotes más pequeños:**
   ```bash
   # Usar prefijo para procesar carpetas por separado
   python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "carpeta1/"
   python obs_utils_improved.py --operation archive --bucket mi-bucket --prefix "carpeta2/"
   ```

2. **Aumentar memoria del sistema o usar una máquina con más RAM**

### 7. Problemas Específicos de Windows

#### Problema: "Error de política de ejecución de scripts"
```
Error: Execution of scripts is disabled on this system
```

**Soluciones:**
```powershell
# Ejecutar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# O ejecutar directamente
python obs_utils_improved.py
```

#### Problema: "Error de ruta demasiado larga"
```
Error: The filename or extension is too long
```

**Soluciones:**
1. **Habilitar soporte para rutas largas:**
   - Ejecutar `gpedit.msc` como Administrador
   - Navegar a: Configuración del Equipo > Plantillas Administrativas > Sistema > Sistema de Archivos
   - Habilitar "Habilitar rutas largas de Win32"

2. **Usar rutas más cortas:**
   ```bash
   # Usar rutas de descarga local más cortas
   python obs_utils_improved.py --operation download --local-path C:\temp
   ```

## Pasos de Depuración

### 1. Habilitar Logging de Debug
```bash
python obs_utils_improved.py --log-level DEBUG --operation list --bucket mi-bucket
```

### 2. Revisar Archivos de Log
```bash
# Ver todos los logs
cat logs/obs_utils.log

# Ver solo errores
grep ERROR logs/obs_utils.log

# Ver actividad reciente
tail -20 logs/obs_utils.log
```

### 3. Probar Componentes Individuales

#### Probar Carga de Configuración
```bash
python -c "from config import load_config; print(load_config())"
```

#### Probar Conexión OBS
```bash
python -c "from obs_manager import OBSManager; m = OBSManager(); print('Conexión OK')"
```

#### Probar Credenciales
```bash
python obs_utils_improved.py --test-config
```

### 4. Validar Entorno

#### Verificar Entorno Python
```bash
python --version
pip list | grep obs
which python
```

#### Verificar Permisos de Archivos
```bash
ls -la obs_config.json*
ls -la logs/
```

#### Verificar Red
```bash
nslookup obs.sa-peru-1.myhuaweicloud.com
telnet obs.sa-peru-1.myhuaweicloud.com 443
```

## Obtener Ayuda

### 1. Recopilar Información
Antes de buscar ayuda, recopila esta información:
- Versión de Python: `python --version`
- Versión del SO: `uname -a` (Linux/macOS) o `systeminfo` (Windows)
- Mensaje de error (texto completo)
- Archivos de log del directorio `logs/`
- Método de configuración usado

### 2. Revisar Documentación
- [Guía de Instalación](INSTALACION.md)
- [Guía de Configuración](CONFIGURACION.md)
- [Guía de Seguridad](SEGURIDAD.md)
- [Ejemplos](EJEMPLOS.md)

### 3. Contactar Soporte
- **Email**: [contact@ccvass.com](mailto:contact@ccvass.com)
- **Incluir**: Detalles del error, logs, información del sistema
- **Asunto**: "Soporte OBS Utils - [Descripción Breve]"

### 4. Recursos de la Comunidad
- Revisar issues existentes en el repositorio
- Revisar documentación de Huawei Cloud OBS
- Buscar problemas similares en línea

## Consejos de Prevención

### 1. Mantenimiento Regular
```bash
# Probar configuración mensualmente
python obs_utils_improved.py --test-config

# Verificar tamaños de archivos de log
du -h logs/

# Rotar logs si es necesario
mv logs/obs_utils.log logs/obs_utils.log.old
```

### 2. Mejores Prácticas de Seguridad
- Rotar regularmente las claves de acceso
- Usar configuración encriptada
- Establecer permisos de archivo apropiados
- Monitorear logs de acceso

### 3. Optimización de Rendimiento
- Usar tamaños de lote apropiados
- Filtrar operaciones con prefijos
- Monitorear conectividad de red
- Mantener Python y dependencias actualizadas

### 4. Respaldar Configuración
```bash
# Respaldar configuración (encriptada)
cp obs_config.json.enc obs_config.json.enc.backup

# Respaldar variables de entorno
env | grep OBS > obs_env_backup.txt
```

## Referencia de Códigos de Error

| Código de Salida | Descripción | Causas Comunes |
|------------------|-------------|----------------|
| 0 | Éxito | Operación completada exitosamente |
| 1 | Error general | Varios errores de tiempo de ejecución |
| 2 | Error de configuración | Configuración faltante o inválida |
| 3 | Error de autenticación | Credenciales inválidas |
| 4 | Error de red | Problemas de conexión |
| 5 | Error de permisos | Acceso denegado |

---

**¿Sigues teniendo problemas?** Contacta [contact@ccvass.com](mailto:contact@ccvass.com) con información detallada del error.

**Desarrollado por CCVASS - Lima, Perú 🇵🇪**
